# Assignment 3 — one row of the grid

<!-- What you score: the pipeline you built in steps 2 and 3, with no learning.
     Against what: the need of scenario.md §4, the robot that reads markers
     and signs while it moves in a lane where people walk.
     Scale: grille.md, from −3 (strong inadequacy) to +3 (strong adequacy).
     For cost and energy, +3 is cheap and frugal. Latency is a band: +3 is
     the time the robot needs, not the fastest time.
     Each sentence gives a number from results/ or a fact from scenario.md.
     The third column says where the number comes from: keep it. -->

| Criterion | Score | One sentence, with a number or a fact | Where it comes from |
|---|---|---|---|
| Latency | +3 | median latency between 1.91 and 4.46ms which allows for real time decision making | `latency_ms_median` in `results/detect-all.csv` |
| Total cost | +3 | this is the cheapest possible way to process images | what it needs: a CPU, no GPU, no training data |
| Energy | +2 | low cpu loads but processing onboard of robot which can drain extra battery | same as cost: what runs on the robot |
| Processing mode | +2 | processes one image at a time, it allows it to keep up with the video stream  | one image at a time, or several? |
| Deployment and sovereignty | +3 | runs locally on the robot independently of network or external services | does it need a network or a service? |
| Robustness | -2 | even marker accuracy is great at 0.971 and shadow marker accuracy at 0.811 and mixed marker at 0.848 but sign accuracy is way off with 0 for mixed and only 0.5 for even | `accuracy` per condition: `even` against `shadow` and `mixed` |
| Explainability | +3 | with the mask it's possible to see exactly what was seen by the algorithm and see why it failed | the images in `out/`: can you say why it failed? |
| Confidentiality | +2 | People can be filmed but data doesn't leave the robot | the camera films the lane, and people walk in it |
| Maintainability | +1 | changes are really easy to make but requires to have read the codebase and not forgotten what was in it, sometimes changes are made through constants, sometimes inside function declarations | steps 4 and 5: how hard was one change? |
| Human control | +3 | The robot either reports or stops when unsure which is the least risky thing to do in our scenario | step 6: what the robot does when it is not sure |
