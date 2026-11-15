"""Step 2 — The grammar.

You write one function here: `interpret(text)`. It reads one order, as text,
and returns (intent, arguments, confidence). Run it with:

    python engine.py --set valid

Read this file from top to bottom. Do what each TODO asks.
"""

# The type hints below (`text: str`, `-> float`…) say what each function takes
# and returns. Python does not check them, but your editor uses them to help
# you. This line lets us write them in the modern way.
from __future__ import annotations

# difflib compares two texts. We use it below to measure how close an order is
# to a sentence the robot knows. https://docs.python.org/3/library/difflib.html
import difflib

# re is the module of "regular expressions": a pattern that describes a family
# of texts, for example "the word robot, a space, then one digit". Each pattern
# below is explained piece by piece.
# https://docs.python.org/3/library/re.html
import re


# -----------------------------------------------------------------------------
# What interpret can answer
# -----------------------------------------------------------------------------

# The intents the engine knows (slide 11). The orders of scenario.md §3.3, the
# assertion of §3.2 ("conveyor 2 is out of service"), the question "why?" of
# §3.5, and two more outcomes: an order for another robot, and "unparsed".
INTENTS = ["forward", "stop", "turn_left", "turn_right", "carry", "make",
           "assert_conveyor", "why", "not_for_me", "unparsed"]

# The four products of the workshop. Open data/world.json: they are under
# "products".
# TODO: copy them here, as a list of texts. PRODUCTS[0] is "blue pallet".
PRODUCTS = ["blue pallet","red pallet","green crate","grey box"]

# The sentences the robot accepts after its wake word, as they look once the
# text is cleaned: lower case, no punctuation. The confidence of an order is
# how close it is to the nearest of these sentences.
#   - `[f"carry {p}" for p in ...]` is a "list comprehension": it builds a list
#     with one text per product: "carry blue pallet", "carry red pallet"…
#   - `f"carry {p}"` is an f-string: Python puts the value of `p` in the text.
#   - `PRODUCTS or []` is PRODUCTS, or an empty list while PRODUCTS is still
#     None. So this file loads before you fill PRODUCTS.
#   - `+` puts two lists end to end.
ACCEPTED = (
    ["forward", "go forward", "move forward", "forward please",
     "stop", "stop now", "turn left", "left", "turn right", "right",
     "why", "why not"]
    + [f"carry {p}" for p in PRODUCTS or []]
    + [f"carry the {p}" for p in PRODUCTS or []]
    # TODO: the same two lines for "make": "make blue pallet",
    # "make the blue pallet"…
    + [f"make {p}" for p in PRODUCTS or []]
    + [f"make the {p}" for p in PRODUCTS or []]

)

# Words that carry no order: "keep going forward" means "forward", "turn to the
# left" means "left". We remove them before we look at the words that count.
# This is a "set", between { }: like a list, but `word in FILLER` is instant,
# and the order does not count.
FILLER = {"go", "going", "keep", "move", "moving", "please", "could", "would",
          "you", "to", "the", "a", "an", "now", "turn", "just", "one", "it"}


# -----------------------------------------------------------------------------
# Two patterns
# -----------------------------------------------------------------------------

# The wake word: "robot", then one digit. As a regular expression, piece by
# piece:
#   ^        the start of the text: the wake word comes first
#   \s*      zero or more spaces (\s is a space, * is "zero or more")
#   robot    the letters r, o, b, o, t
#   \s+      one or more spaces (+ is "one or more")
#   (\d)     one digit (\d). The brackets "capture" it: match.group(1) gives
#            it back, as a text
#   \b       the end of a word: "robot 35" does not match
#   [\s,]*   zero or more spaces or commas, after the wake word
# The `r` before the quotes keeps each backslash as it is. re.IGNORECASE:
# "Robot" matches too.
# https://docs.python.org/3/library/re.html#regular-expression-syntax
WAKE = re.compile(r"^\s*robot\s+(\d)\b[\s,]*", re.IGNORECASE)

# The assertion of scenario.md §3.2: "conveyor 2 is out of service". The human
# gives information. It changes what the robot knows about the world: it is not
# an order (slide 15). The pattern: "conveyor", spaces, one digit (captured),
# spaces, "is", spaces, then the state of the conveyor (captured).
# A conveyor has three states: "out of service", "busy", "free". In a regular
# expression, a|b|c means a, or b, or c.
# TODO: replace None, inside the brackets, with the three states.
CONVEYOR = re.compile(r"conveyor\s+(\d)\s+is\s+(out of service|busy|free)", re.IGNORECASE)

# Your robot is robot number 3: see "wake_word" in data/world.json.
# match.group(1) gives the digit as a text, not as a number: "3", not 3.
# TODO: the number of your robot, as a text.
MY_NUMBER = "3"


# -----------------------------------------------------------------------------
# Two functions are given. Read them line by line. Then give each one a name
# that says what it does.
# -----------------------------------------------------------------------------

# TODO: this function prepares a text before we compare it. Give it a name in
# one word, a verb. Rename it here, and in `interpret` below.
def normalize(text: str) -> str:
    # Three things, from the inside out:
    #   1. `text.lower()`: all in lower case. "Carry" becomes "carry".
    #   2. `re.sub(pattern, " ", ...)` replaces each piece that matches the
    #      pattern with a space. [^a-z0-9 ]+ means: one or more characters that
    #      are NOT (^) a letter from a to z, a digit, or a space. So ",", "."
    #      and "?" become spaces.
    #      https://docs.python.org/3/library/re.html#re.sub
    #   3. `.strip()`: no space at the start or at the end.
    return re.sub(r"[^a-z0-9 ]+", " ", text.lower()).strip()


# TODO: this function gives one number between 0 and 1 for two texts. What does
# it measure? Give it a name in one word. Rename it here, and in `interpret`.
def similarity(a: str, b: str) -> float:
    # SequenceMatcher finds the blocks of letters that `a` and `b` share, in
    # the same order. `.ratio()` is 2 x (letters shared) / (letters of a +
    # letters of b): 1.0 when the two texts are the same, 0.0 when they share
    # nothing. It plays the role of the normalised edit distance of slide 12.
    # https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.ratio
    return difflib.SequenceMatcher(None, a, b).ratio()


# -----------------------------------------------------------------------------
# Your function.
# -----------------------------------------------------------------------------

# "carry the pallet": the verb is known, the product is not. It is a known
# intent with a bad argument (slide 13), not "not understood at all". We keep
# its confidence low: at most a little above the default threshold of the
# engine, 0.5. Then a threshold a little higher refuses it.
UNKNOWN_ARGUMENT_CAP = 0.55  # TODO: a number a little above 0.5. Try 0.55.


def interpret(text: str) -> tuple[str, str | None, float]:
    # Return a tuple of three values: (intent, arguments, confidence), for
    # example ("carry", "blue pallet", 1.0). Four outcomes (slide 11):
    #   - a known intent, with its arguments;
    #   - a known intent with a missing or unknown argument:
    #     ("carry", None, a low confidence);
    #   - ("not_for_me", "robot 5", ...): an order for another robot;
    #   - ("unparsed", None, confidence): not understood. No crash, no guess.
    raw = text.strip()

    # 1. The wake word gates everything: an order without it never reaches the
    #    grammar. WAKE.match(raw) tries the pattern at the start of `raw`. It
    #    returns a "match", or None when `raw` does not start with the wake
    #    word. https://docs.python.org/3/library/re.html#re.Pattern.match
    match = WAKE.match(raw)
    # TODO: replace False with the condition "there is no match".
    # `match is None` does it.
    if match is None:
        return "unparsed", None, 0.0

    # 2. Another robot. match.group(1) is the digit after "robot".
    # TODO: if it is not MY_NUMBER, return ("not_for_me", "robot <digit>", 0.95).
    # `!=` means "is not equal to". Build "robot <digit>" with an f-string.
    # 0.95: the pattern matched exactly, so we are sure. Not 1.0: we may have
    # misheard the digit.
    if match.group(1) != MY_NUMBER:
        return "not_for_me", f"robot {match.group(1)}", 0.95

    # 3. The text after the wake word. match.end() is the position just after
    #    the wake word, and raw[n:] is the text from position n on. Then we
    #    prepare it with your first function.
    rest = normalize(raw[match.end():])
    # TODO: if `rest` is empty (the human said "robot 3" and nothing more),
    # return ("unparsed", None, 0.0). An empty text counts as False:
    # `if not rest:` does it.
    if not rest:
        return "unparsed", None, 0.0

    # 4. An assertion. CONVEYOR.search(rest) looks for the pattern anywhere in
    #    `rest` (match looks only at the start). It returns a match, or None.
    conveyor = CONVEYOR.search(rest)
    # TODO: if `conveyor` is not None, return
    # ("assert_conveyor", "<digit> <state>", 0.95). The digit is
    # conveyor.group(1), the state conveyor.group(2). Example: "2 out of service".
    if conveyor is not None :
        return ("assert_conveyor", f"{conveyor.group(1)} {conveyor.group(2)}", 0.95)


    # 5. The confidence: the similarity of `rest` to the nearest sentence of
    #    ACCEPTED.
    best, confidence = None, 0.0
    # TODO: in words: for each sentence of ACCEPTED, if its similarity to
    # `rest` (your second function) is higher than `confidence`, it becomes
    # `best`, and its similarity becomes `confidence`.
    for sentence in ACCEPTED:
        sim = similarity(sentence,rest)
        if sim > confidence:
            best = sentence
            confidence = sim

    # 6. The words of `rest`. `.split()` cuts a text at the spaces: a list of
    #    words. `rest` is not empty (point 3 above), so words[0] exists.
    words = rest.split()

    # 6a. The orders with a product. "carry", "take" and "bring" mean carry;
    #     "make" and "build" mean make. `in` checks if a value is in a tuple.
    if words[0] in ("carry", "make", "take", "bring", "build"):
        # TODO: "carry" when words[0] is "carry", "take" or "bring";
        # "make" otherwise.
        intent = "carry" if words[0] in ("carry","take","bring") else "make"
        # The words after the verb, without the filler words, glued back with
        # one space: "the blue pallet" -> "blue pallet". Inside join(...), a
        # comprehension with a condition: it keeps w only if w is not in FILLER.
        tail = " ".join(w for w in words[1:] if w not in FILLER)
        # The product whose name is exactly `tail`, or None. next(..., None)
        # gives the first value that the comprehension produces, or None if it
        # produces nothing.
        # https://docs.python.org/3/library/functions.html#next
        product = next((p for p in PRODUCTS if p == tail), None)
        # TODO: return (intent, product, confidence). But when `product` is
        # None, the confidence is at most UNKNOWN_ARGUMENT_CAP:
        # min(confidence, UNKNOWN_ARGUMENT_CAP).
        if product is None:
            return (intent, None, min(confidence,UNKNOWN_ARGUMENT_CAP))
        else:
            return (intent,product,confidence)

    # 6b. The orders without a product. The filler words go, the word that
    #     carries the order stays: "keep going forward" -> ["forward"].
    core = [w for w in words if w not in FILLER]
    # TODO: when `core` has exactly one word (len(core) == 1):
    #   "forward"          -> ("forward", None, confidence)
    #   "stop"             -> ("stop", None, confidence)
    #   "left" or "right"  -> ("turn_left" or "turn_right", None, confidence).
    #                         f"turn_{core[0]}" builds it in one line.
    if len(core) == 1:
        word = core[0]
        if word == "forward":
            return ("forward", None, confidence)
        elif word == "stop":
            return ("stop", None, confidence)
        elif word in ["left","right"]:
            return (f"turn_{core[0]}", None, confidence)
    # TODO: when `core` is not empty and its first word is "why":
    # ("why", None, confidence).

    if len(core) !=0 and core[0]=="why":
        return ("why",None,confidence)

    # 7. Nothing matched: not understood. We still return the confidence of
    #    step 5: the sweep of step 4 reads it.
    return "unparsed", None, confidence
