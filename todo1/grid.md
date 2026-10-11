# Decision grid

| | Latency | Total cost | Energy | Processing mode | Deployment and sovereignty | Robustness | Explainability | Confidentiality | Maintainability | Human control | Weighted score |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Closed grammar** | 1 | 2 | 3 | 0 | 3 | -3 | 3 | 3 | 3 | 0 | **56** |
| **Pre-trained recogniser + rules** | 3 | 2 | -1 | -2 | 3 | 2 | 1 | 3 | -1 | 1 | **48** |
| **Hosted API** | 2 | -1 | -3 | 1 | -3 | 3 | -2 | -3 | -2 | -3 | **-30** |
| **Weights** | 4 | 5 | 3 | 4 | 4 | 5 | 5 | 4 | 3 | 1 | — |

---

## Justification of each criterion

### Latency

- Closed grammar : almost instant no human changes possible -> 1
- Pre-trained recogniser + rules : inference time should be pretty quick for a simple sentence -> 3
- Hosted API : the network adds a few hundred ms of latency but inference is still quick -> 2

Since the robot works with humans, having a low latency is important : weight = 4

### Total cost

- Closed grammar : as cheap as it gets but not free -> 2
- Pre-trained recogniser + rules : an open-source model is free but there is a setup cost for rules -> 2
- Hosted API : requires constant network access + fees paid to the provider -> -1

Cost isn't specified but it is often heavily weighted : weight = 5

### Energy

- Closed grammar : the most energy efficient -> 3
- Pre-trained recogniser + rules : required a lot of computing to create and costs energy at every inference -> -1
- Hosted API : requires a data-center, longer training and constant network accessibility -> -3

I assume public buildings are somewhat conscious about energy usage : weight = 3

### Processing mode

- Closed grammar : needs the entire audio but can be modified to work word by word on a stream -> 0
- Pre-trained recogniser + rules : the pre-trained models used are trained to recognise whole sentences, not word by word -> -2
- Hosted API : a hosted API is usually flexible from the get-go -> 1

People expect acknowledgment from the robot so a stream helps : weight = 4

### Deployment and sovereignty

- Closed grammar : runs on the robot -> 3
- Pre-trained recogniser + rules : downloaded once and then runs locally -> 3
- Hosted API : requires a 1-month delay to approve outbound traffic plus the data leaves the confines of the building -> -3

The location of data is important for public buildings: weight = 4

### Robustness

- Closed grammar : fails almost instantly when there is noise -> -3
- Pre-trained recogniser + rules : actually works quite well with noise but isn't perfect -> 2
- Hosted API : large models trained on a lot of data are the most robust to noise -> 3

The hall has a lot of noise with the glass ceiling ring and the coffee machine : weight = 5

### Explainability

- Closed grammar : can show every step of the decision process -> 3
- Pre-trained recogniser + rules : we can't tell in a human legible way why the robot heard what it heard but rules can be explained and logs can be made -> 1
- Hosted API : There is no access to the models used by the hosting company -> -2

Humans expect explanations from the robot for error explaining : weight = 5

### Confidentiality

- Closed grammar : keeps the voice on the robot -> 3
- Pre-trained recogniser + rules : keeps the voice on the robot -> 3
- Hosted API : the voice leaves the robot and goes to a third party -> -3

The microphone can pick up other conversations that may be private : weight = 4

### Maintainability

- Closed grammar : very easily updated -> 3
- Pre-trained recogniser + rules : we can't change anything about the model, we can only change models or some parameters -> -1
- Hosted API : changes are easily monitored but problems can arise from the host company and can't be fixed -> -2

The system needs to work but the possible answers are very limited : weight = 3

### Human control

- Closed grammar : A human can't change anything about the answer as it is almost instantaneous but it also can't go out of control -> 0
- Pre-trained recogniser + rules : the robot could be stopped in its thoughts with a trigger word -> 1
- Hosted API : The situation is fully automated -> -3

There is no real danger or emergencies that would require the robot to be rectified quickly by a human : weight = 1

---


## Criterion that works against its value
Latency works against the value of human agency and oversight as an AI that decides and answers before the choice could be examinated doesn't allow for human agency over what happens.

## Knock-put 

The robot should be able to understand what the people say with a very high success rate (>95%).

Option 1 has the best score but is eliminated because a closed grammar becomes very bad at detecting things in a high noise environment.

## The context moves

1.  Cost would probably the first weight to change as a million users is a million customers that pay in a way or another for a service compared to a public building. Other changed weights would be robustness, explainability and sovereignty 

2. The Host API would probably be the winner as the advantages of the locally run recognizer become less important. Or if we assume the same weights for most things, but there is little to no noise, the closed grammar would become the winner as the knock-out criterion isn't applicable anymore.

3. The App still has to show it has heard the user in under a second
   The App probably doesn't need to always fetch a person for support as the cost of a single user is often minimal compared to the cost of support
   The need for explainability is still there if the mobile application deals with money or other sensitive things.