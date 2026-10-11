Notes step by step of lab2

Step 2 :


I named the first function to name "highpass_filter" because this is what it seems to do. it removes the sliding average at the cutoff_hz specified.

I named the 2nd function "energy_frame" because it seems to calculate the average of the squared values of x for each frame.

For MARGIN_DB, I first started off with 20DB but there was clipping all across the board, same for 10DB and 5DB. Trying all integers between 1 and 5 showed that at 2DB there was a bit of clipping on 2 files, the highest value with no clipping is 1DB.



Step 3 : 


The first TODOs were pretty easy to do, although some steps were hard to understand due to the language being english and being unfamiliar with english signal processing terms.

when running with python engine.py --input files --set all 
the results are completely wrong with near 0 accuracy everywhere 
because the function recognise needs one word per segment of voice

so we run with base parameters SEGMENT_FLOOR_DB = 14 and UNPARSED_BELOW = 0.45
python engine.py --input files --set all --speech words 

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

with UNPARSED_BELOW = 0.45 :
segment_floor_db going from 14 to 6 doesn't change results and for 5 and under results gradually become worse as we pick up less and less of the signal
from 14 to 17 the results don't change at all
going above we start seeing decrease in accuracy for snr10, then 20 then 30 as we start allowing more and more noise. Doing this the accuracy for clean signal never changes as it is in fact a clean signal 

with SEGMENT_FLOOR_DB = 14 :
unparsed_below doesn't affect accuracy that much except at extreme values like 0.95 and of course at low values unparsed_below changes nothing. But it would change drastically the way the robot acts as with too low values the robot could misunderstand completely things.


The way the closed grammar was implemented in step 3, the user must mark a pause between each words when giving an order otherwise the robot could try to interpret the whole order as a single or a few words depending on the pause duration we choose to detect and the way users speak.