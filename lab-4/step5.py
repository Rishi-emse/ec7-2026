"""Step 5 — "Why?", from the trace.

You write one function here: `explain(entry)`. The human asks "why?" after a
refusal, and the robot answers in at most ten words. Run it with:

    python engine.py --set both

(Step 4 has no code: you run the engine and write your report.)

Read this file from top to bottom. Do what each TODO asks.
"""

# Type hints, as in step 2.
from __future__ import annotations

# Everything from step 3, and so from step 2.
from step3 import *


# -----------------------------------------------------------------------------
# What the engine gives you
# -----------------------------------------------------------------------------
# After each run, the engine calls `explain` once per refused order. It gives
# it one line of trace.jsonl, as a dictionary. Open trace.jsonl in your editor
# and look at one line. Its keys:
#   entry["text"]       the order, as it arrived: "robot 3 make green crate"
#   entry["state"]      the name of the state: "busy2"
#   entry["world"]      the state itself, the same dictionary as `state` in
#                       step 3: entry["world"]["conveyors"]["2"] is
#                       "busy with robot 1, 40 s"
#   entry["intent"], entry["arguments"], entry["confidence"]
#                       what your interpret answered
#   entry["action"], entry["reason"]
#                       what your decide answered
#
# The engine checks your sentences the cheap way. The same refused order comes
# twice, in two different states ("make green crate" with conveyor 2 busy, then
# out of service). Two identical sentences mean you read a table, not the
# trace (slide 30). So each sentence must hold a fact of this run: the
# distance of the person, the product in the hands, the state of the conveyor.
#
# At most ten words: the engine cuts the rest. The operator needs one short
# sentence; the confidence and the rule that fired are for the engineer who
# reads the log (slide 31).


# -----------------------------------------------------------------------------
# Your function.
# -----------------------------------------------------------------------------

def explain(entry: dict) -> str:
    # `entry.get(key, default)` reads a key, and gives `default` when it is
    # missing, as in step 3.
    # https://docs.python.org/3/library/stdtypes.html#dict.get
    world = entry.get("world", {})
    reason = entry.get("reason")

    # 1. Not understood: the human repeats. The first case is written for you.
    if reason == "not_understood":
        intent = entry.get("intent")
        # TODO: a known verb without a product (intent "carry" or "make", see
        # step 3, point 7). Then the human must name a product. Return an
        # f-string with the intent in it, for example "carry what? say a
        # product I know".
        if intent in ("carry","make"):
            return f"{intent} what? say a product I know"
        return "I did not catch that, say it again"

    # TODO 2. Not permitted (reason "not_permitted"): someone is ahead, and the
    # human escalates. The fact: world.get("person_distance_m"), the distance
    # in metres. Return an f-string with it, for example
    # "someone is 1.1 m ahead, I am not moving".

    if reason == "not_permitted":
        dist = world.get("person_distance_m")
        return f"someone is {dist} m ahead, I am not moving"


    # TODO 3. Not possible right now (reason "not_possible"): the human waits.
    # Two cases, in words:
    #   - the robot's hands already hold something, world.get("carrying"):
    #     say which product, for example "my hands hold the blue pallet already";
    #   - otherwise, the conveyor of the product is not free. The product is
    #     entry.get("arguments"). Its conveyor is
    #     world["product_conveyor"].get(<the product>), and the state of that
    #     conveyor is world["conveyors"].get(<the conveyor>). Say both, for
    #     example "conveyor 2 busy with robot 1, 40 s".

    if reason=="not_possible":
        if world.get("carrying"):
            return f"my hands hold the {world.get("carrying")} already"
        
        product = entry.get("arguments")
        conveyor = world["product_conveyor"].get(product)
        conveyor_status = world["conveyors"].get(conveyor)
        return f"conveyor {conveyor} is {conveyor_status}"


    # TODO 4. Not for me (reason "not_for_me"): entry.get("arguments") says
    # which robot the order was for ("robot 5"). Say it, for example
    # "that was for robot 5, not me".

    if reason == "not_for_me":
        dest = entry.get("arguments")
        return f"that was for {dest}, not me"

    # 5. Any other reason: nothing to explain.
    return ""
