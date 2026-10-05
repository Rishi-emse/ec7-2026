Notes step by step of lab2

Step 2 :
I named the first function to name "highpass_filter" because this is what it seems to do. it removes the sliding average at the cutoff_hz specified.

I named the 2nd function "energy_frame" because it seems to calculate the average of the squared values of x for each frame.

For MARGIN_DB, I first started off with 20DB but there was clipping all across the board, same for 10DB and 5DB. Trying all integers between 1 and 5 showed that at 2DB there was a bit of clipping on 2 files, the highest value with no clipping is 1DB.