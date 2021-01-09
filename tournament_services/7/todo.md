# **To Do:**

# Test failures:

[X] Inspect test failures at:
* /home/vagrant/4500/repo/6/annetta/Tests/5-in.json (local: Tests/6-in.json)
* /home/vagrant/4500/repo/6/oakwood/Tests/4-in.json (local: Tests/7-in.json)
* /home/vagrant/4500/repo/6/westmountain/Tests/4-in.json (local: Tests/8-in.json)

# Milestone 6:

[ ] Add additional unit tests addressing abnormal conditions.

[ ] In Referee documentation, document that we are protecting the referee by making a deep copy 
before calling on the player 

# **Milestone 5:**

**Code Inspection:**

[X]file/folder structure could have been organized better in the README

**Design Inspection:**

[X]the document mentions that the referee runs the game according to the age of players, but the document doesn&#39;t specify how that order is determined


# **Milestone 4:**

**Refactoring**

[X]insufficient interpretation of the board, no explaination of what holes mean? how the data definition represents a real game board. The comments on FishBoardModel class should have all these explanations.

[X]insufficient interpretation of the game state- no explanation on how players are related to penguins and how penguins&#39; locations are tracked, how player turn is tracked

**Code Inspection**

[X]it is unclear that the generation of a tree is suspended, no explaination for usage of yield

[X]it is unclear if the game tree node can represent all two kinds of nodes: game-is-over, current-player-is-stuck

[X]no explanation of a lazy (&quot;caching&quot;) scheme of the game tree generation or documentation

**Design Inspection**

[X]insufficient description of the player&#39;s API wrt to a referee no way to check end game status

[X]the description of the protocol does mention order in which functionality can be used start-up (this mentioned in beginning of game), (not mentioned when called) rounds, and end of game (which isnt there)

[X]the description of the protocol does not mention that placing and taking turns

are often-used functionalities, unlike starting and ending a game

# **Milestone 3:**

**Code Inspection**

[X]data definition or interpretation for game states. - can\_any\_player\_move - little unclear implementation of current player turn - maybe return the id of player who can play??

[X]sufficient coverage of unit tests for turn-taking functionality, coverage for player turns changing isnt there

# **Milestone 2:**

**Design Inspection**

[X]no &quot;interface&quot; specification that connects game-state to players and referees

[X]construction of an intermediate game-state is not accounted for in the interface



