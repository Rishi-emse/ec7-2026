# Notes step by step of lab2

---

## Step 2 :

I named the first function to name "highpass_filter" because this is what it seems to do. it removes the sliding average at the cutoff_hz specified.

I named the 2nd function "energy_frame" because it seems to calculate the average of the squared values of x for each frame.

For MARGIN_DB, I first started off with 20DB but there was clipping all across the board, same for 10DB and 5DB. Trying all integers between 1 and 5 showed that at 2DB there was a bit of clipping on 2 files, the highest value with no clipping is 1DB.

---

## Step 3 :

The first TODOs were pretty easy to do, although some steps were hard to understand due to the language being english and being unfamiliar with english signal processing terms.

when running with

```sh
python engine.py --input files --set all
```

the results are completely wrong with near 0 accuracy everywhere
because the function recognise needs one word per segment of voice

so we run with base parameters `SEGMENT_FLOOR_DB = 14` and `UNPARSED_BELOW = 0.45`

```sh
python engine.py --input files --set all --speech words
```

```text
>>>
step4.py: MODEL_SIZE is still None. Give it a value.
step7.py: BARGE_IN_DB is still None. Give it a value.
step7.py: ROBOT_PERCENTILE is still None. Give it a value.
420 file(s), clean, snr30, snr20, snr10, snr5, snr0, snrm5, corpus spoken by chatterbox, words speech, intonation order

condition           n  intent acc     WER   med ms   p90 ms  stops
clean              60       0.583    0.26     4.49     6.14    0/8
snr30              60       0.267   0.575      4.1     5.32    0/8
snr20              60       0.083   0.764     4.12     5.84    0/8
snr10              60       0.017   1.824     4.79     7.32    0/8
snr5               60         0.0   3.015     5.69     7.86    0/8
snr0               60         0.0   3.765     6.16     8.16    0/8
snrm5              60         0.0    4.03     6.23      8.3    0/8

results/baseline-words-order.csv, results.csv and trace.jsonl written.
```

### with `UNPARSED_BELOW = 0.45` :

segment_floor_db going from 14 to 6 doesn't change results and for 5 and under results gradually become worse as we pick up less and less of the signal
from 14 to 17 the results don't change at all
going above we start seeing decrease in accuracy for snr10, then 20 then 30 as we start allowing more and more noise. Doing this the accuracy for clean signal never changes as it is in fact a clean signal

### with `SEGMENT_FLOOR_DB = 14` :

unparsed_below doesn't affect accuracy that much except at extreme values like 0.95 and of course at low values unparsed_below changes nothing. But it would change drastically the way the robot acts as with too low values the robot could misunderstand completely things.

The way the closed grammar was implemented in step 3, the user must mark a pause between each words when giving an order otherwise the robot could try to interpret the whole order as a single or a few words depending on the pause duration we choose to detect and the way users speak.

---

## Step 4 :

```python
model = "base.en"
device = "cpu"
compute_type = "int8"
beam_size = 5
```

```text
model loaded in 1.0 s (not counted)

condition           n  intent acc     WER   med ms   p90 ms  stops
clean              60       0.983    0.83   353.76   376.43    0/8
snr30              60       0.983   0.832   359.35   378.32    0/8
snr20              60         1.0    0.83   356.82   380.16    0/8
snr10              60        0.95   0.837   360.18   377.05    0/8
snr5               60       0.883   0.834    360.0    378.0    0/8
snr0               60       0.717   0.959   361.87   1194.9    0/8
snrm5              60       0.217   1.076   373.01  1360.82    0/8

real time factor  0.17 here, 1.90 on the robot's class of CPU (stated figure)
```

this here gives very good intent accuracy with a higher than baseline WER for low noise signals. Latency really spikes with very noisy signals snr0 and snrm5. The problem here is the real time factor as the robot will lag behind on understanding orders 1.90 is the stated figure for the tiny.en model so we can assume it is 3 or even 4 for base.en. May be fine if the robot doesn't get a lot of orders at once, would need special measures for emergency stops. For the P90 latency, around 380ms is a bit too slow to feel real time but still allows for pretty fast answers.

### Trying the lighter model :

```python
model = "tiny.en"
device = "cpu"
compute_type = "int8"
beam_size = 5
```

```text
condition           n  intent acc     WER   med ms   p90 ms  stops
clean              60        0.95   0.906   175.12   195.79    0/8
snr30              60        0.95   0.881   177.84   195.19    0/8
snr20              60       0.983   0.859   176.23   194.17    0/8
snr10              60       0.883   0.843   174.45   196.69    0/8
snr5               60       0.733   0.851   175.98   197.76    0/8
snr0               60         0.5   1.081   184.19   643.89    0/8
snrm5              60         0.1   1.248   435.54    682.1    0/8

real time factor  0.09 here, 1.90 on the robot's class of CPU (stated figure)
```

Here the results for low noise signals are almost as good as the base model but there is a significant drop in accuracy for snr10 and snr5. I assume these signal to noise ratio would be frequent in a factory environment. The P90 value is more appealing than with the base model but the better accuracy outweighs the faster response time in this case.

changing compute_type and beam_size affect the response time by less than 10% and the accuracy by one more sample recognized or less so I decided to keep them on compute_type = "int8" and beam_size = 5

### Finally testing out the small model :

```python
model = "small.en"
device = "cpu"
compute_type = "int8"
beam_size = 5
```

```text
condition           n  intent acc     WER   med ms   p90 ms  stops
clean              60       0.967   0.854   948.38   977.96    0/8
snr30              60       0.967   0.835   943.91   974.51    0/8
snr20              60       0.983   0.859   942.81   973.64    0/8
snr10              60       0.983   0.849   943.72   973.35    0/8
snr5               60       0.933   0.861   943.12   975.44    0/8
snr0               60       0.817   0.862   945.35   982.95    0/8
snrm5              60       0.417   0.969   953.92  2204.17    0/8

real time factor  0.38 here, 1.90 on the robot's class of CPU (stated figure)
```

There is a significant accuracy gain for snr5 and snr0 signals at the cost of being almost 3 times as slow on median times. Comparing with the real time factor from the tiny model we could expect the real time factor to be 20 times what my computer produces and a response time of 20 seconds is way too long.

**Chosen model : base.en** because if we were to use a pretrained model running on the robot, all models would have a real time factor that is too high. And while the p90 latency is alright when ran on my computer it would be a lot longer on the robot. The base model seems to be a good compromise between speed and accuracy, with the same assumptions as before we could expect the base.en model to have an 8s p90 latency when run on the robot which would probably be very frustrating but functional for the snr10 region. ALl models are too slow for an emergency stop anyways.

---

## Step 5 :

By deciding to always accept a stop even with low confidence the thing that mattered was maximising following correct orders while not doing any wrong orders. Fortunately in my test the robot never did something wrong so the best threshold i nthis case would be at 0.5 confidence with 53 correct decisions and 7 refusals.

Trying with refusing low confidence stops I get the exact same results for the sweep except for 1 where it refuses everything obviously and the best threshold is at 0.5 again

```text
threshold  correct  wrong  refused  stops refused
      0.0       53      0        7              0
     0.05       53      0        7              0
      0.1       53      0        7              0
     0.15       53      0        7              0
      0.2       53      0        7              0
     0.25       53      0        7              0
      0.3       53      0        7              0
     0.35       53      0        7              0
      0.4       53      0        7              0
     0.45       53      0        7              0
      0.5       53      0        7              0
     0.55       52      0        8              0
      0.6       52      0        8              0
     0.65       49      0       11              0
      0.7       49      0       11              0
     0.75       49      0       11              0
      0.8       47      0       13              0
     0.85       46      0       14              0
      0.9       45      0       15              0
     0.95       40      0       20              0
      1.0        0      0       60              8
```

With the model I chose in step 4 it seems that the best threshold is at 0.5 and that in case of low confidence stops its better to follow them although there haven't been any in the test set, better be safe than sorry.

---

## Step 6 :

The closed grammar completely fails once intonations are taken into account.

```text
condition           n  intent acc     WER   med ms   p90 ms  stops
clean/order        60       0.983    0.83   384.11   412.41    8/8
clean/cheerful     60       0.983   0.854   398.89   425.03    8/8
clean/alarmed      60       0.983   0.825   379.73   417.28    8/8
snr5/order         60       0.883   0.834    383.0   413.17    8/8
snr5/cheerful      60        0.95    0.84   392.98   421.01    8/8
snr5/alarmed       60       0.683   0.866   378.91   422.26    4/8
```

even accepting low confidence stops we are not able to catch all the stops. It would be best to have it run on another channel and maybe even for better confidence have it run on multiple ones. As with our current solution, voice activation isn't fast enough nor precise enough for a stop in an alarmed voice in a noisy environment.

---

## step 7 :

the recorded voice would oubviously be almost instant
the onboard voice has a small latency but it's pretty much instant too (20ms)
the hosted voice has a 600ms latency which is a bit high

with the --loopback on the human can interrupt the robot while it's speaking as the robot takes into account what is said while it is speaking if it has a much higher volume.