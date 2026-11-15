
Context: Interpretation of spoken/written natural language orders for a workshop robot operating near humans and conveyors.
option 1 : Hand-written grammar 
option 2 (Alternative): LLM interpreter.

# Decision grid

| Criterion | weight | option 1 : hand-written grammar | option 2 : LLM interpreter |
| --- | --- | --- | --- |
| Latency | 3 | +3 | -2 |
| Total cost | 4 | +2 | -2 |
| Energy | 2 | +3 | -3 |
| Processing mode | 2 | +1 | -1 |
| Deployment and sovereignty | 4 | +3 | 0 |
| Robustness | 5 | +1 | +3 |
| Explainability | 4 | +3 | -2 |
| Confidentiality | 2 | +2 | -1 |
| Maintainability | 3 | -2 | +1 |
| Human control | 5 | +3 | +1 |
| Total (weighted) | | +67 | -9 |

# Explaination

**Latency**
weight : 3 The robot needs to be able to slow down or stop quickly
option 1 : +3 The grammar has a p90 decision time of less than 1.2ms
option 2 : -2 An LLM call takes hundreds of milliseconds

**Total cost**
weight : 4 Cost is a big factor for a factory needing to profit
option 1 : +2 The grammar requires a small upfront cost and basically no inference cost 
option 2 : -2 LLM call prices can rack up expenses quickly

**Energy**
weight : 2 Energy is not a problem onboard the robot as the cpu has negligible power usage
option 1 : +3 The grammar is very quick and efficient
option 2 : -3 LLM inference energy cost is the most expensive option possible for this task

**Processing mode : stream or complete data**
weight : 2 in the setting, processing mode allows for faster reaction time and makes it allows for decision even if the speech to text algorithm isn't finished or mistakenly adds too much
option 1 : +1 The grammar can work on a stream of words as the decision process can take information word by word (although it isn't actually the case in the code)
option 2 : -1 An LLM needs a whole sentence to be sent

**Deployment and sovereignty**
weight : 4 Data must stay in the factory
option 1 : +3 The grammar is fully offline and only runs on the cpu
option 2 : 0 The LLM needs either cloud computing or a dedicated machine on the factory network

**Robustness**
weight : 5 Orders will often not be completely translated to text or the operator might not say the exact same sentence each time
option 1 : +1 The grammar has a limited set of sentences that it understands but can reject and ask for clarifications on orders 
option 2 : +3 The LLM can understand pretty much any human sentence and decide with high precision what the order was                          

**Explainability**
weight : 4 In case of a problem or accident we should be able to pinpoint the mistake made
option 1 : +3 The grammar has strict rules that can be understood and explained 
option 2 : -2 We have access to the inputs and outputs of the LLM but the decision process is unknown, we can explain an action made because of a wrong order but can't explain why the LLM misunderstood or greenlit an impossible order

**Confidentiality**
weight : 2 The factory doesn't have confidentiality issues but other discussions can be picked up and interpreted by the robots
option 1 : +2 Everything is processed on the robot cpu, no data leaves, there may only be logs only accessible by the technical team
option 2 : -1 The data would either be sent to the cloud or processed on a local machine but data leaves the robot and can be accessed by other people

**Maintainability**
weight : 3 The environment and rule set can change but not often
option 1 : -2 A dev team needs to manually think of, update and bug test all of the phrasings 
option 2 : +1 New order can be updated by updating the prompt given to the LLM but still needs testing

**Human control**
weight : 5 Operators need to have the final word on robot actions unless it is a strictly forbidden order (running over someone for exemple)
option 1 : +3 The Operator has feedback on the order given and can stop the robot like through the use of the word "stop"
option 2 : +1 Same as option 1 but the extra decision time and the feedback may not be consistent with what the LLM gave back to the robot

**Total (weighted)**
option 1 : +67
option 2 : -9

# Conclusion

**Option kept :** Option 1 seems better for our factory environment according to the scores of the grid*
**Trade-off:** I accept a lot less robustness and more difficult maintenance to get lower overall costs, easier deployment and better confidentiality
