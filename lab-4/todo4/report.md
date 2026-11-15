# step 1 
the code runs and i get the output and trace.jsonl as expected

# step 2

intent accuracy : 1.0
median latency (ms) : 0.802
p90 latency (ms) : 1.121

the grammar works perfectly on the valid order set which is expected with an accuracy of 1.0 on intent

# step 3

decision accuracy : 1.0
median latency(ms) : 0.855
p90 latency (ms) : 1.114

The decision process works perfectly on the valid order set which is expected with an accuracy of 1.0 on intent

# step 4

testing with the adversarial set : we get no wrong action and no refusals which means the grammar works perfectly for this test set

sweep :

Threshold choice : 0.65

According to the sweep, wrong refusals start appearing at 0.75, this threshold can be defended and allows for the best correct decision rate with no refusals

The family "world_decides" isn't caught by the threshold as we can see it is always understood with full confidence, it is the decision made in step 3 to stop whenever a physical object is present for security reasons

# step 5

after writing the function :

the robot answers for the operator giving order :

cause : not_permitted
v05  [not_permitted  ] someone is 1.1 m ahead, I am not moving, 

cause : not_possible
v20  [not_possible   ] my hands hold the blue pallet already

cause : not_understood
a12,ambiguous,robot 3 make one,idle,make,not_understood,make what? say a product I know,False






