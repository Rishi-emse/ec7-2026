# Lab 4 — the order, and the refusal

EC7, session 4. The lab statement is assignment 4, on the course site. Fork
this project and work in your fork.

New to Python, Git or VS Code? Follow *Getting started* on the course site
first: https://ci.mines-stetienne.fr/courses/interacting-humans-real-world/getting-started.html

```sh
git clone https://gitlab.emse.fr/<you>/lab-4.git
cd lab-4
. <your ec7>/.venv/bin/activate     # the course environment, from assignment 1
                                    # Windows: <your ec7>\.venv\Scripts\activate
python engine.py --set valid --limit 5 --verbose
```

Nothing to install: the lab runs on the Python standard library alone.

## What is here

| | |
|---|---|
| `engine.py` | holds the world, times and scores your code, writes one file per run in `results/`. Do not modify it |
| `step2.py`, `step3.py`, `step5.py` | one file per step, which guides you. This is all you write. Step 4 has no code |
| `data/valid.csv` | 40 orders that mean something, each with the state it arrives in |
| `data/adversarial.csv` | 40 orders in five families. None must lead to an action |
| `data/states.json` | six states of the world |
| `data/world.json` | the wake word, the products, and the conveyor each product needs |

## The world decides too

The engine owns the state: which conveyor is busy, if someone is in the lane,
if the robot moves, what it carries. The same words arrive in different states.
`stop` while idle, while moving, and with a person ahead: three decisions.

Your threshold is in `state["threshold"]`. `--sweep` moves it.

## Running it

```sh
python engine.py --set valid                          # steps 2 and 3
python engine.py --set adversarial                    # step 4
python engine.py --set both --sweep 0.0:1.0:0.05      # step 4, writes sweep.csv
python engine.py --set both                           # step 5
```

Each run writes `results/<set>.csv` (one row per family) and
`results/why-<set>.csv` (your answer to "why?" for each refusal). It also
writes `results.csv` and `trace.jsonl`: one line per order, with what arrived,
in which state, what you understood, what you decided and why. Your `explain`
of step 5 reads one of these lines.
