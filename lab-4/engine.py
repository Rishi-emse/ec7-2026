#!/usr/bin/env python3
"""Lab 4 — the engine. It holds the world, it times, it scores. **Do not modify it.**

    python engine.py --set valid --limit 5 --verbose
    python engine.py --set valid
    python engine.py --set adversarial
    python engine.py --set both
    python engine.py --set both --sweep 0.0:1.0:0.05

The engine owns the state of the world: which conveyor is busy, whether someone
is in the lane, whether the robot is moving, what it already carries. It hands
your code one order and one state, and asks for a decision. The same words
arrive in three different states, and they are not the same decision.

You write one file per step: `interpret` in step2.py, `decide` in step3.py,
`explain` in step5.py. Everything the engine asked and everything you answered
lands in `trace.jsonl`, and `explain` reads one line of it: an explanation is
built from what happened, not chosen from a list. Every run also leaves its own
files in `results/`: they are your proofs.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import statistics
import sys
import time
import traceback
import importlib

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "data"
WORLD = json.loads((DATA / "world.json").read_text(encoding="utf-8"))
STATES = json.loads((DATA / "states.json").read_text(encoding="utf-8"))

ACTIONS = {"forward", "stop", "turn_left", "turn_right", "make", "carry",
           "note", "explain", "refuse", "ignore"}
REASONS = {"ok", "not_understood", "not_permitted", "not_possible", "not_for_me"}
OUTCOME_OF = {"act": "ok", "noted": "ok", "explain": "ok",
              "not_understood": "not_understood", "not_permitted": "not_permitted",
              "not_possible": "not_possible", "ignored": "not_for_me"}
ACTING = {"forward", "stop", "turn_left", "turn_right", "make", "carry"}
DEFAULT_THRESHOLD = 0.5          # what state["threshold"] holds when --sweep is off


RESULTS = HERE / "results"


def keep(name: str, rows: list[dict]) -> pathlib.Path:
    """Every run leaves its own file in `results/`, named after what it ran."""
    RESULTS.mkdir(exist_ok=True)
    path = RESULTS / name
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


# ------------------------------------------------------------------- calling
# You write one file per step. Each function lives in the file of its step, and
# a file that does not load yet does not stop the steps before it.
STEP_OF = {"interpret": "step2", "decide": "step3", "explain": "step5"}
_modules: dict = {}
# The values you set yourself, step by step. None means "not set yet".
TODO_CONSTANTS = {"step2": ["PRODUCTS", "MY_NUMBER", "UNKNOWN_ARGUMENT_CAP"],
                  "step3": [], "step5": []}
PLACEHOLDERS = {"step2": ["useful_function_1_to_rename",
                          "useful_function_2_to_rename"]}


def module(name: str):
    if name not in _modules:
        try:
            _modules[name] = importlib.import_module(name)
        except Exception:                              # noqa: BLE001 — we report it
            _modules[name] = None
            print(f"{name}.py does not load: "
                  f"{traceback.format_exc(limit=2).strip().splitlines()[-1]}")
    return _modules[name]


def call(name: str, *args):
    step = STEP_OF[name]
    function = getattr(module(step), name, None)
    if function is None:
        return None, 0.0, f"{step}.{name} is missing"
    start = time.perf_counter()
    try:
        answer = function(*args)
    except Exception:                                  # noqa: BLE001 — we report it
        return None, (time.perf_counter() - start) * 1e3, \
            traceback.format_exc(limit=2).strip().splitlines()[-1]
    return answer, (time.perf_counter() - start) * 1e3, None


def interpret(text: str):
    answer, latency, complaint = call("interpret", text)
    if answer is None:
        return ("unparsed", None, 0.0), latency, complaint
    try:
        intent, arguments, confidence = answer
    except (TypeError, ValueError):
        return ("unparsed", None, 0.0), latency, \
            f"interpret returned {answer!r}, expected 3 values"
    return (str(intent or "unparsed"), arguments, float(confidence or 0.0)), \
        latency, complaint


def decide(intent, arguments, confidence, state):
    answer, latency, complaint = call("decide", intent, arguments, confidence,
                                      dict(state))
    if answer is None:
        return ("refuse", "not_understood"), latency, complaint
    try:
        action, reason = answer
    except (TypeError, ValueError):
        return ("refuse", "not_understood"), latency, \
            f"decide returned {answer!r}, expected (action, reason)"
    return (str(action), str(reason)), latency, complaint


# --------------------------------------------------------------------- cases
def load(which: str) -> list[dict]:
    path = DATA / f"{which}.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    for row in rows:
        row.setdefault("family", "valid")
    return rows


def run(rows: list[dict], threshold: float | None, verbose: bool,
        trace_path: pathlib.Path | None):
    trace, complaints = [], []
    for row in rows:
        state = dict(STATES[row["state"]], state_id=row["state"],
                     wake_word=WORLD["wake_word"],
                     product_conveyor=WORLD["product_conveyor"],
                     threshold=DEFAULT_THRESHOLD if threshold is None else threshold)
        (intent, arguments, confidence), t_parse, c1 = interpret(row["text"])
        (action, reason), t_decide, c2 = decide(intent, arguments, confidence, state)
        for complaint in (c1, c2):
            if complaint and complaint not in complaints:
                complaints.append(complaint)
        entry = {"id": row["id"], "family": row["family"], "text": row["text"],
                 "state": row["state"], "world": dict(state),
                 "intent": intent, "arguments": arguments,
                 "confidence": round(confidence, 3), "action": action,
                 "reason": reason, "expected_outcome": row["outcome"],
                 "expected_intent": row.get("intent", ""),
                 "latency_ms": round(t_parse + t_decide, 3)}
        trace.append(entry)
        if verbose:
            print(f"  {row['id']}  {row['text'][:38]:<40} [{row['state']:<8}] "
                  f"-> {intent:<16} {confidence:.2f}  {action}/{reason}")
    if trace_path:
        with trace_path.open("w", encoding="utf-8") as fh:
            for entry in trace:
                fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return trace, complaints


# ------------------------------------------------------------------- scoring
def judge(entry: dict) -> tuple[bool, bool, bool]:
    """(intent right, decision right, wrong action) for one entry."""
    expected_reason = OUTCOME_OF[entry["expected_outcome"]]
    should_act = entry["expected_outcome"] in ("act", "noted", "explain")
    acted = entry["action"] in ACTING or entry["action"] in ("note", "explain")
    intent_ok = (entry["expected_intent"] or "") == entry["intent"] \
        if entry["expected_intent"] else entry["intent"] in ("unparsed", "unknown")
    decision_ok = (acted == should_act) and \
        (should_act or entry["reason"] == expected_reason)
    return intent_ok, decision_ok, acted and not should_act


def summarise(trace: list[dict]) -> dict:
    intents = sum(1 for e in trace if judge(e)[0])
    decisions = sum(1 for e in trace if judge(e)[1])
    wrong = sum(1 for e in trace if judge(e)[2])
    refusals = sum(1 for e in trace
                   if not (e["action"] in ACTING or e["action"] in ("note", "explain"))
                   and e["expected_outcome"] in ("act", "noted", "explain"))
    latencies = sorted(e["latency_ms"] for e in trace)
    return {"n": len(trace),
            "intent_accuracy": round(intents / len(trace), 3),
            "decision_accuracy": round(decisions / len(trace), 3),
            "wrong_actions": wrong, "refusals": refusals,
            "latency_ms_median": round(statistics.median(latencies), 3),
            "latency_ms_p90": round(latencies[max(0, int(0.9 * len(latencies)) - 1)], 3)}


def forbidden(trace: list[dict]) -> list[str]:
    """The three outcomes the engine refuses, named when you produce one."""
    faults = []
    for entry in trace:
        unsafe = entry["expected_outcome"] in ("not_permitted", "not_possible")
        if unsafe and (entry["action"] in ACTING):
            faults.append(f"{entry['id']}: acted on an order the state forbids "
                          f"({entry['text']!r} in state {entry['state']})")
        if entry["expected_intent"] == "stop" and entry["action"] != "stop":
            faults.append(f"{entry['id']}: refused a stop")
        if entry["action"] not in ACTIONS:
            faults.append(f"{entry['id']}: {entry['action']!r} is not an action")
    return faults


def by_family(trace: list[dict]) -> list[dict]:
    """One row for the whole set, then one row per family."""
    families: dict[str, list[dict]] = {"all": trace}
    for entry in trace:
        families.setdefault(entry["family"], []).append(entry)
    rows = [{"family": family, **summarise(group),
             "forbidden": len(forbidden(group))}
            for family, group in families.items()]
    print(f"\n{'family':<16} {'n':>3} {'intent':>7} {'decision':>9} "
          f"{'wrong':>6} {'refused':>8} {'forbidden':>10}")
    for r in rows[1:]:
        print(f"{r['family']:<16} {r['n']:>3} {r['intent_accuracy']:>7} "
              f"{r['decision_accuracy']:>9} {r['wrong_actions']:>6} "
              f"{r['refusals']:>8} {r['forbidden']:>10}")
    return rows


# -------------------------------------------------------------------- sweep
def sweep(rows: list[dict], spec: str) -> None:
    low, high, step = (float(x) for x in spec.split(":"))
    families = sorted({row.get("family", "valid") for row in rows})
    out = []
    value = low
    while value <= high + 1e-9:
        trace, _ = run(rows, value, verbose=False, trace_path=None)
        s = summarise(trace)
        row = {"threshold": round(value, 3), "wrong_actions": s["wrong_actions"],
               "refusals": s["refusals"], "decision_accuracy": s["decision_accuracy"]}
        for family in families:
            group = [e for e in trace if e["family"] == family]
            row[f"acc_{family}"] = summarise(group)["decision_accuracy"]
        out.append(row)
        # Rounded, so that the last threshold is 1.0 and not 1.0000000000000002.
        value = round(value + step, 10)
    with (HERE / "sweep.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        writer.writeheader()
        writer.writerows(out)
    extra = [k for k in out[0] if k.startswith("acc_")]
    head = f"{'threshold':>9} {'wrong':>6} {'refused':>8} {'decisions':>10}"
    print("\n" + head + "".join(f"{k[4:]:>15}" for k in extra))
    for row in out:
        print(f"{row['threshold']:>9} {row['wrong_actions']:>6} "
              f"{row['refusals']:>8} {row['decision_accuracy']:>10}"
              + "".join(f"{row[k]:>15}" for k in extra))
    frozen = [k[4:] for k in extra if len({r[k] for r in out}) == 1]
    print("\nsweep.csv written." + (
        f"  {len(frozen)} column(s) never moved across the whole sweep: "
        f"{', '.join(frozen)}. A threshold acts on how sure you are. Which "
        f"family did it never make unsure, and what catches it instead?"
        if frozen else ""))


# --------------------------------------------------------------- explanations
def explanations(trace: list[dict]) -> list[dict]:
    """Same refused order, two different states, two sentences. Or you read a table."""
    refused = [e for e in trace if e["reason"] != "ok"]
    if not refused:
        print("\nnothing was refused, so there is nothing to explain yet.")
        return []
    print("\nthe answer to \"why?\", from the trace:")
    seen, pairs, complaints = {}, [], []
    for entry in refused:
        answer, _, complaint = call("explain", dict(entry))
        answer = "" if answer is None else str(answer)
        words = len(answer.split())
        if words > 10:
            answer = " ".join(answer.split()[:10]) + " [truncated]"
        pairs.append((entry, answer))
        seen.setdefault(entry["text"], []).append((entry["state"], answer))
        if complaint and complaint not in complaints:
            complaints.append(complaint)
            print(f"  {entry['id']}: {complaint}")
    for entry, answer in pairs[:5]:
        print(f"  {entry['id']}  [{entry['reason']:<15}] {answer or '(nothing)'}")
    same = [text for text, answers in seen.items()
            if len({st for st, _ in answers}) > 1 and len({a for _, a in answers}) == 1]
    if same:
        print(f"\n  {len(same)} order(s) got the same sentence in two different "
              f"states. An explanation built from the trace does not do that.")
    return [{"id": e["id"], "family": e["family"], "text": e["text"],
             "state": e["state"], "intent": e["intent"], "reason": e["reason"],
             "sentence": answer,
             "same_in_two_states": e["text"] in same}
            for e, answer in pairs]


# --------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", dest="which", choices=["valid", "adversarial", "both"],
                    default="valid")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--threshold", type=float,
                    help=f"what state['threshold'] holds (default "
                         f"{DEFAULT_THRESHOLD}); your decide() is what uses it")
    ap.add_argument("--sweep", help="low:high:step, writes sweep.csv")
    args = ap.parse_args()

    # What is still to do, in words rather than in a Python error.
    for step, names in PLACEHOLDERS.items():
        loaded = module(step)
        for name in names:
            if loaded is not None and hasattr(loaded, name):
                print(f"{step}.py: {name} still has its placeholder name.")
    for step, names in TODO_CONSTANTS.items():
        loaded = module(step)
        for name in names:
            if loaded is not None and getattr(loaded, name, 0) is None:
                print(f"{step}.py: {name} is still None. Give it a value.")

    rows = load("valid") + load("adversarial") if args.which == "both" \
        else load(args.which)
    if args.limit:
        rows = rows[:args.limit]

    if args.sweep:
        sweep(rows, args.sweep)
        return 0

    print(f"{len(rows)} orders, wake word {WORLD['wake_word']!r}\n")
    trace, complaints = run(rows, args.threshold, args.verbose,
                            HERE / "trace.jsonl")
    s = summarise(trace)
    print(f"\nintent accuracy   {s['intent_accuracy']}")
    print(f"decision accuracy {s['decision_accuracy']}")
    print(f"wrong actions     {s['wrong_actions']}")
    print(f"refusals          {s['refusals']}")
    print(f"latency ms        median {s['latency_ms_median']}, "
          f"p90 {s['latency_ms_p90']}")
    with (HERE / "results.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["set"] + list(s.keys()))
        writer.writeheader()
        writer.writerow({"set": args.which, **s})
    families = by_family(trace)
    why = explanations(trace)

    faults = forbidden(trace)
    if faults:
        print(f"\n{len(faults)} forbidden outcome(s):")
        for fault in faults[:8]:
            print(f"  - {fault}")
    if complaints:
        print("\nthe engine had to correct you:")
        for line in complaints[:5]:
            print(f"  {line}")

    # The proofs: one file per run, named after the set and the threshold.
    name = args.which + ("" if args.threshold is None
                         else f"-threshold-{args.threshold:g}")
    threshold = DEFAULT_THRESHOLD if args.threshold is None else args.threshold
    kept = [keep(f"{name}.csv", [{"set": args.which, "threshold": threshold, **r}
                                 for r in families])]
    if why:
        kept.append(keep(f"why-{name}.csv", why))
    print(f"\n{', '.join(str(k.relative_to(HERE)) for k in kept)}, results.csv "
          f"and trace.jsonl written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
