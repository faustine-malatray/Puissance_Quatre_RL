# Puissance_Quatre_RL

The assignment is to develop an agent for Connect4, as implemented in the PettingZoo library, using Reinforcement Learning methods.

https://pettingzoo.farama.org/environments/classic/connect_four/

Students need to form groups of 2 or 3 students, and will deliver a zip containing the code and a short report on the methods used. Deadline: April 14th.

The report should contain a description of the methods used and a description of the results. Here are a few questions that should be adressed in some way in the report
What design choices did you make in the development of your algorithm?
Describe the training procedure, the structure of the code.
Describe how you chose important hyperparameters, what you understand from their impact.
How did you assess the quality of your agent?
Do you think the approach you implemented would fare well on more complex environments, like backgammon, chess, go, Starcraft?
How would you improve it if given more time or computational power?
Describe also the workflow and how you split the work in the group.


The code should be clear and legible, variables well-named, and commented when helpful for comprehension. The final code should implement a class Player, with a method get_action that takes a state as specified in the PettingZoo environment and returns an integer between 0 and 6.

Performance is not the main point: better to show understanding of the methods you used and their limits.  

Ideas to get started: 
MCTS : https://sites.ualberta.ca/~szepesva/papers/CACM-MCTS.pdf

Eligibility Traces:
https://www.bkgm.com/articles/tesauro/tdl.html
https://www.ai.rug.nl/~mwiering/GROUP/ARTICLES/learning-chess.pdf