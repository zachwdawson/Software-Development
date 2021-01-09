## Self-Evaluation Form for Milestone 6

Indicate below where your TAs can find the following elements in your strategy and/or player-interface modules:

The implementation of the "steady state" phase of a board game
typically calls for several different pieces: playing a *complete
game*, the *start up* phase, playing one *round* of the game, playing a *turn*, 
each with different demands. The design recipe from the prerequisite courses call
for at least three pieces of functionality implemented as separate
functions or methods:

- the functionality for "place all penguins"
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/referee.py#L98-L116
    - This runs our placement phase for placing penguins overall, and calls sub-methods for each round and turn
    of placing penguins

- a unit test for the "place all penguins" funtionality 
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/unit_test/ref_test.py#L110-L156
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/unit_test/ref_test.py#L226-L259
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/unit_test/ref_test.py#L295-L306
    - The first link has our unit-tests for individual placement turns, then the second link has tests for running a whole round
    of placement. The third link tests running our overall game which includes running the place-all penguins phase

- the "loop till final game state"  function
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/referee.py#L118-L132
    
- this function must initialize the game tree for the players that survived the start-up phase
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/referee.py#L111-L116
    - Here we initialize the game tree at the end of the placement phase.

- a unit test for the "loop till final game state"  function
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/unit_test/ref_test.py#L261-L318
    - Here we test running one-round loops of turns and running whole games and so together we felt that that tested
    running the whole "looping till final game state"

- the "one-round loop" function
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/referee.py#L239-L248


- a unit test for the "one-round loop" function
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/unit_test/ref_test.py#L261-L293

- the "one-turn" per player function
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/referee.py#L250-L273


- a unit test for the "one-turn per player" function with a well-behaved player 
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/unit_test/ref_test.py#L158-L170


- a unit test for the "one-turn" function with a cheating player
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/unit_test/ref_test.py#L190-L199
    


- a unit test for the "one-turn" function with an failing player 
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/unit_test/ref_test.py#L201-L224


- for documenting which abnormal conditions the referee addresses 
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/referee.py#L43-L52
    


- the place where the referee re-initializes the game tree when a player is kicked out for cheating and/or failing
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish/Admin/referee.py#L181-L183
    - Here the player is kicked from the game and the game tree is re-initialized by re-calling the constructor.



**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**

  WARNING: all perma-links must point to your commit "251e40dcd9ee689122520c5235ed1438a7b2f3a0".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/annettasouth/tree/251e40dcd9ee689122520c5235ed1438a7b2f3a0/Fish>

