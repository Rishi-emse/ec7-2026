Generative AI :

tool : Claude Code Sonnet 5.5 free plan
items : grid.md and report.md
how : For grid.md I asked it to generate the outline of the file where I only had to fill in the numbers and my sentences
    For report.md I gave it my finished report and asked it to make it prettier without changing any of what I wrote
what you checked : I reread diagonally report.md to make sure nothing was changed
what the AI got wrong : nothing 
conversation : 

make me a md table with these 10 columns and 3 rows : weight, closed grammar, pre-trained model
Figuring out a table layout with specific rows and columns.
Figuring out a table layout with specific rows and columns.

I don’t know your 10 columns, so I used 10 criteria taken from your lab as placeholders. Rename them to match your own. The first column holds the row labels, so the table is 11 wide.
markdown

| | Clean accuracy | Accuracy at snr5 | Collapse rung | Median latency | Real-time factor on robot | Natural speech | Stop reliability | Vocabulary flexibility | Model size | Setup effort |
|---|---|---|---|---|---|---|---|---|---|---|
| **Weight** | | | | | | | | | | |
| **Closed grammar** | | | | | | | | | | |
| **Pre-trained model** | | | | | | | | | | |

It renders as:
	Clean accuracy	Accuracy at snr5	Collapse rung	Median latency	Real-time factor on robot	Natural speech	Stop reliability	Vocabulary flexibility	Model size	Setup effort
Weight										
Closed grammar										
Pre-trained model										

I left the cells empty on purpose. The Weight row is your own judgement of how much each criterion matters, for example 1 to 5. The other two rows can come from your runs, but only if the cell is a single value. For instance:

    Clean accuracy: 0.583 (closed grammar, --speech words) and 0.983 (base.en).
    Accuracy at snr5: 0.0 and 0.883.
    Median latency: about 4.5 ms and about 354 ms on your machine.
    Real-time factor on robot: a stated figure, 1.90 for tiny.en, so mark any base.en value as your estimate.
    Natural speech: closed grammar needs pauses between words, and the pre-trained model doesn’t.

If you tell me your real 10 columns, I’ll rebuild the table with them. If you want a weighted score, I can add a total column that multiplies each score by its weight.

    Latency — end-to-end response time for the target interaction: the whole chain, not only the model.
    Total cost — development + operation + licences + infrastructure.
    Energy — consumption for training, inference and deployment, and the hardware it needs.
    Processing mode (streaming vs complete information) — the option processes a stream and emits incremental output, or it needs all the data to decide.
    Deployment and sovereignty — fit to the network (bandwidth, stability, network latency), operation without a network, location of data and processing (local, EU, non-EU), dependence on an external API.


and for report.md my prompt was : "make this into a neat md file where you don't change any of the text or numbers"

Collaboration :
Alone

Your part : 
I did pretty much everything alone 
It took 4 hours in total with some good breaks sprinkled in
I understood the way to write and run a closed grammar although it wasn't very accurate. I also understood how to use an open-source model for a task.