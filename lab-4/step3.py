"""Step 3 — The decision, on top of the parse.

You write one function here: `decide(intent, arguments, confidence, state)`.
It returns (action, reason). Run it with:

    python engine.py --set valid

The engine replays the same orders in six states of the world. `stop` while
idle, `stop` while moving, `stop` while a person is ahead: the same words,
three decisions (slide 14).

Read this file from top to bottom. Do what each TODO asks.
"""

# Type hints, as in step 2.
from __future__ import annotations

# This line imports everything from step2.py: your interpret, your two renamed
# functions, PRODUCTS, INTENTS… You do not copy them again.
from step2 import *


# -----------------------------------------------------------------------------
# What decide can answer
# -----------------------------------------------------------------------------

# What the robot does. The first six are orders it executes. "note": it writes
# down an assertion. "explain": it answers "why?". "refuse": it says no.
# "ignore": the order was for another robot.
ACTIONS = ["forward", "stop", "turn_left", "turn_right", "carry", "make",
           "note", "explain", "refuse", "ignore"]

# Why. "ok" when the robot acts. Then the three causes of a refusal (slide 29),
# each with the next move of the human: "not_understood" (they repeat),
# "not_permitted" (they escalate), "not_possible" (they wait). And
# "not_for_me": the order was for another robot.
REASONS = ["ok", "not_understood", "not_permitted", "not_possible", "not_for_me"]


# -----------------------------------------------------------------------------
# Your function.
# -----------------------------------------------------------------------------

def decide(intent: str, arguments: str | None, confidence: float,
           state: dict) -> tuple[str, str]:
    # `intent`, `arguments` and `confidence` come from your interpret of
    # step 2. `state` is a dictionary given by the engine. Open
    # data/states.json to see the six states. Its keys:
    #   state["moving"]            True or False
    #   state["person_ahead"]      True when someone is in the lane
    #   state["person_distance_m"] how far, in metres, or None
    #   state["carrying"]          the product in the robot's hands, or None
    #   state["conveyors"]         a dictionary: conveyor -> its state, for
    #                              example state["conveyors"]["2"] is "free",
    #                              "busy with robot 1, 40 s" or "out of service"
    #   state["product_conveyor"]  a dictionary: product -> the conveyor it
    #                              needs. state["product_conveyor"]["green crate"]
    #                              is "2"
    #   state["threshold"]         the confidence below which the robot
    #                              refuses. The sweep of step 4 changes it:
    #                              read it here, do not write a number.
    #
    # `state.get(key, default)` reads a key, and gives `default` when the key
    # is missing, where state[key] would crash.
    # https://docs.python.org/3/library/stdtypes.html#dict.get
    #
    # The ORDER of the checks is the lesson. Each check returns at once, so a
    # check placed too early swallows everything after it. Read them all
    # before you write. The first one is written for you.

    # 1. An order for another robot: you neither execute it nor refuse it.
    #    It is not yours.
    if intent == "not_for_me":
        return "ignore", "not_for_me"

    # TODO 2. "stop": always ("stop", "ok"), whatever the state and the
    # confidence. A refused stop is a forbidden outcome: the engine names it.
    if intent == "stop":
        return ("stop", "ok")

    # TODO 3. "unparsed": ("refuse", "not_understood").
    if intent == "unparsed":
        return ("refuse", "not_understood")

    # TODO 4. "why": ("explain", "ok"). Answering is never dangerous. This
    # check comes before the safety check of point 6: placed after it, the
    # safety check would swallow the question too.
    if intent == "why":
        return ("explain", "ok")

    # TODO 5. "assert_conveyor": ("note", "ok"). The robot writes it down.
    if intent == "assert_conveyor":
        return ("note","ok")

    # TODO 6. Safety. If a person is ahead (state.get("person_ahead")), no
    # order moves the robot: ("refuse", "not_permitted").
    # `if state.get("person_ahead"):` is enough: in a condition, True passes,
    # and False, None, 0 and an empty text do not.

    if state.get("person_ahead"):
        return ("refuse","not_permitted")

    # TODO 7. "carry" or "make" with no product: ("refuse", "not_understood").
    # The human must name a product. `intent in ("carry", "make")` checks the
    # first part; `not arguments` is True when `arguments` is None.

    if intent in ("carry", "make") and not arguments:
        return ("refuse", "not_understood")

    # TODO 8. The guardrail. If the confidence is below
    # state.get("threshold", 0.5): ("refuse", "not_understood").

    if confidence < state.get("threshold", 0.5):
        return ("refuse","not_understood")

    # TODO 9. "carry". If the robot's hands already hold something
    # (state.get("carrying")): ("refuse", "not_possible"). Otherwise
    # ("carry", "ok").

    if intent == "carry":
        if state.get("carrying"):
            return ("refuse", "not_possible")
        else:
            return ("carry","ok")

    # TODO 10. "make". The product needs one conveyor, and the conveyor must be
    # free. In words:
    #   - the conveyor of the product: state["product_conveyor"].get(arguments);
    #   - its state: state["conveyors"].get(conveyor, "free");
    #   - if that state is not "free": ("refuse", "not_possible");
    #   - otherwise: ("make", "ok").

    if intent == "make":
        conveyor = state["product_conveyor"].get(arguments)
        conveyor_state = state["conveyors"].get(conveyor, "free")
        if  conveyor_state != "free":
            return "refuse", "not_possible"
        return ("make", "ok")


    # TODO 11. "forward", "turn_left" or "turn_right": (intent, "ok"). One
    # condition with `in`, as in point 7.

    if intent in ("forward", "turn_left", "turn_right"):
        return (intent, "ok")


    # 12. Anything else: not understood.
    return "refuse", "not_understood"
