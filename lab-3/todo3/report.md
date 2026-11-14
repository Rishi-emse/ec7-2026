# Assignment 3 — report

<!-- Fill every ___ . Copy the numbers from the files named in each section:
     do not round them, do not retype a table by hand from memory.
     Write one or two short sentences where a line asks for one. -->

## 1. The markers (step 2)

Copy the `marker` rows of `results/detect-all.csv`:

| condition | accuracy | distance_mae_m |
|---|---|---|
| even | 0.971 | 0.037 |
| low-sun |0.893 | 0.021 |
| shadow | 0.811 | 0.016 |
| mixed | 0.848 | 0.013 |

- `CLOSE_HEIGHT_PX` I kept: 81 px.
- Sheets 3 and 4: both read? no (yes / no)
- Success image: `todo3/even-040-marker-mask.png`

## 2. The signs (step 3)

Copy the `sign` rows of `results/detect-all.csv`:

| condition | family_accuracy | accuracy | distance_mae_m |
|---|---|---|---|
| even | 0.75 | 0.562 | 0.071 |
| low-sun | 0.591 | 0.591 | 0.075 |
| shadow | 0.846 | 0.692 | 0.05 |
| mixed | 0.0 | 0.0 | |

- The arrows: which ones does it confuse? for even if confused sign-up with sign-right twice and sign-up with sign-left once, for shadow it confused sign-up with sign-right once and sign-right with sign-down once (see `results/confusions-all.csv`)

## 3. The distance

| | real size (m) | mask ratio | `distance_mae_m` (even) |
|---|---|---|---|
| marker | 0.2015 | 1 | 0.037 |
| stop sign (red octagon) | 0.070 | 57/70 | 0.071 |
| direction sign (blue disc) | 0.070 | 67.9/70 | 0.071 |

- One sentence: what happens to the distance if the mask ratio is wrong? distance = f*(real_size*ratio)/h so the distance would be off proportionately with the ratio (e.g. a ratio 20% off would make the distance 20%off)

## 4. Where it breaks (step 4)

The change I made: 's>100' to 's>60' (for example: `s > 100` to `s > 60` in `blue = …`).

| condition | detector | accuracy before | accuracy after |
|---|---|---|---|
| shadow | marker | 0.811 | 0.811 |
| mixed | marker | 0.848 | 0.848 |
| shadow | sign | 0.692 | 0.615 |
| mixed | sign | 0.0 | 0.529 |

"Before" is `results/detect-all.csv`, "after" is `results/detect-all-change.csv`.

- Shadow image: `todo3/shadow-002-marker-mask.png`. Which band does the shadow add? the shadow add a black band and makes it go from "kwkwk" to "kwkwkwk"
- Was the change worth it? the change was worth it the detection for sign went from 0 accuracy to 0.529 for signs at a small cost for shadow sign from 0.692 to 0.615(one line, with one number)

## 5. The false positive rate (step 5)

| detector | `fp_per_minute` before (`detect-absent.csv`) | after the stricter test |
|---|---|---|
| marker | 48.0 | 48.0 |
| sign | 48.0 | 0.0 |

- Taken for what (`confusions-absent.csv`): sheet-9, 4 times
- What the stricter test costs on the other sets (`detect-all-tuned.csv` against `detect-all.csv`): shadow fammily accuracy 0.846 -> 0.692, even family accuracy 0.75 -> 0.688, even accuracy 0.562 -> 0.5, no changes on other accuracies 
- False positive image: `todo3/absent-001-marker-mask.png`

## 6. The action policy (step 6)

- `results/policy.csv`: forbidden outcomes left: 0 (0 is the goal)
- `STOP_FROM_M` = 0.7m, because there are no forbidden outcomes and it gives it leeway to brake before 0.3m
- Not sure of a close stop sign, the robot does: stop
- Confidence threshold for a person: 0, For a stop sign: 0.5 Why they differ: hitting a person is the worst possible outcome for the robot, for a stop sign, putting no confidence threshold would give false positives that would delay the robot too much
- Privacy, one line: where the frames are stored, for how long, who sees them: frames stored in robot's memory, deleted after decision taken, nobody sees them unless code is changed for debugging 
