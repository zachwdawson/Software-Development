# **Milestone 5:**

**Code Inspection:**

file/folder structure could have been organized better in the README

We updated the directory structure formatting in the README to be more readable.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/251e40dcd9ee689122520c5235ed1438a7b2f3a0#diff-f4923aab63564278027a266fe91df7a4R11

**Design Inspection:**

the document mentions that the referee runs the game according to the age of players, but the document doesn&#39;t specify how that order is determined

Update referee to store age as number of years?

https://github.ccs.neu.edu/CS4500-F20/dish/commit/7a4b8ebaf062884d80ff1c58c2e3f189a25154d9

# **Milestone 4:**

**Refactoring**

insufficient interpretation of the board, no explaination of what holes mean? how the data definition represents a real game board. The comments on FishBoardModel class should have all these explanations.

Expand upon the interpretation of our board to explain how it maps to the standard json board.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/2cfff53c333f43a48c7c8c42784f2c9dbddb5656

insufficient interpretation of the game state- no explanation on how players are related to penguins and how penguins&#39; locations are tracked, how player turn is tracked

Expand upon state representation to explain how players and their penguins are tracked and how player order is kept.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/2cfff53c333f43a48c7c8c42784f2c9dbddb5656

**Code Inspection**

it is unclear that the generation of a tree is suspended, no explaination for usage of yield

Add note in class interpretation to explain how yield works and why it is used.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/f7ca0ca48279be5bd931a76255658fd970ba2555

it is unclear if the game tree node can represent all two kinds of nodes: game-is-over, current-player-is-stuck

Add _create_next_color_child to account for skipping players if they have no moves and check if the game is in end state before trying to generate children at all.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/f7ca0ca48279be5bd931a76255658fd970ba2555

no explanation of a lazy (&quot;caching&quot;) scheme of the game tree generation or documentation

Update generate_children documentation to explain "lazy" retrieval of children.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/f7ca0ca48279be5bd931a76255658fd970ba2555

**Design Inspection**

insufficient description of the player&#39;s API wrt to a referee no way to check end game status

Add inform_of_winners to tell the tournament manager who won at the end of the game.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/af89808a9fe4ef743153fc884939492410152e63

the description of the protocol does mention order in which functionality can be used start-up (this mentioned in beginning of game), (not mentioned when called) rounds, and end of game (which isnt there)

Add inform_of_winners to tell the tournament manager who won at the end of the game.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/af89808a9fe4ef743153fc884939492410152e63

the description of the protocol does not mention that placing and taking turns

are often-used functionalities, unlike starting and ending a game

Note that pacing penguins and moving penguins are more commonly used than start and end game.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/af89808a9fe4ef743153fc884939492410152e63

# **Milestone 3:**

**Code Inspection**

data definition or interpretation for game states. - can\_any\_player\_move - little unclear implementation of current player turn - maybe return the id of player who can play??

Add a field to the state that keeps track of the current playing turn.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/bb12ea7c2831bbe2a7bc6ad59594364d554aeaf4

sufficient coverage of unit tests for turn-taking functionality, coverage for player turns changing isnt there

Add test that explicitely tests turn taking functionality

https://github.ccs.neu.edu/CS4500-F20/dish/commit/a9dcb796e4085c6f002b5ccbb8f49a796081faac

# **Milestone 2:**

**Design Inspection**

no &quot;interface&quot; specification that connects game-state to players and referees

Explain that game referee controls player placement and movement.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/a9dcb796e4085c6f002b5ccbb8f49a796081faac

construction of an intermediate game-state is not accounted for in the interface

Explain 4 states of game state that include initialization, placement, movement, and over.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/a9dcb796e4085c6f002b5ccbb8f49a796081faac
