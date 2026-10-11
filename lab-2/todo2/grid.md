A company makes and delivers products. The workspace has workshops with conveyors (four, shared between groups), storage areas, and shared traffic lanes with road signs that every robot obeys. Each group has one mobile robot: TurtleBot3, Pi camera, microphone. All robots share the same physical space, so the other groups see and suffer what your robot does. Humans delegate goals, take back control, and expect explanations.

We have 2 options : a closed grammar and a pre-trained model running locally on robots

| | Latency | Total cost | Energy | Processing mode | Deployment and sovereignty | Robustness | Explainability | Confidentiality | Maintainability | Human control | Weighted score |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Closed grammar** | 3 | 2 | 3 | 1 | 3 | -3 | 3 | 3 | 3 | -3 | 38 |
| **Pre-trained model** | -2 | 3 | -1 | -3 | 3 | 2 | 1 | 3 | -1 | 2 | 23 |
| **Weights** | 4 | 5 | 3 | 4 | 2 | 5 | 5 | 1 | 3 | 5 | — |



latency :
a closed grammar is almost instant -> 3
a pre-trained model takes a few to a dozen seconds to run -> -2
Since the robots work with humans, having a low latency is important : weight = 4

total cost :
a closed grammar is as cheap as it gets but not free -> 2
an open-source model is free and the robots can already run the models -> 3
cost matter a lot for a company : weight = 5

energy :
a closed grammar is the most energy efficient -> 3
a pre-trained model required a lot of computing to create and costs energy at every inference on the robot's CPU, even if the training was paid by someone else -> -1
The robot is battery powered but cpu energy costs are very low compared to moving : weight = 3

processing mode :
the closed grammar needs the entire audio but can be modified to work word by word on a stream -> 1
the pre-trained models used are trained to recognise whole sentences not word by word -> -3
stops should quickly stop the robot : weight = 4

deployment and sovereignty :
a closed grammar runs on the robot -> 3
a pre-trained model is downloaded once and then runs locally  -> 3
the factory data isn't sensitive: weight = 2

robustness :
the closed grammar fails almost instantly when there is noise -> -3
the pre-trained model actually works quite well with noies but isn't perfect -> 2
The workshop is noisy with machines and humans : weight = 5

explainability :
a closed grammar can show every step of the decision process -> 3
we can't tell in a human legible way why the robot heard what it heard -> 1
Humans expect explanations from the robot : weight = 5

confidentiality :
a closed grammar keeps the voice on the robot -> 3
a pre-trained model keeps the voice on the robot  -> 3
robot orders are not something confidential here : weight = 1

maintainability :
closed grammars are very easily updated -> 3
we can't change anything about the model, we can only change models or some parameters -> -1
the system needs to work but there are only a handful of possible orders : weight = 3

human control :
the human has to speak one word at a time and the robot has a hard time understanding things with noise -> -3
in most cases the robot can listen and recongize the word stop but it has latency -> 2
factory incidents are dangerous and have to be avoided at all cost : weight = 5

Based on the scores, the closed grammar seem to win except for the fact that the closed grammar doesn't work at all in a noise environment.