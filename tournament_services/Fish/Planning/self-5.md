## Self-Evaluation Form for Milestone 5

Under each of the following elements below, indicate below where your
TAs can find:

- the data definition, including interpretation, of penguin placements for setups 
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/2624ea6ba0db731d44e9794d698e32b039b2ac0b/Fish/Player/strategy.py#L17-L18
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/2624ea6ba0db731d44e9794d698e32b039b2ac0b/Fish/Player/strategy.py#L122-L128
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/2624ea6ba0db731d44e9794d698e32b039b2ac0b/Fish/Common/representations/types.py#L3-L8
    - The first two links point to places in our strategy file where we note the
    strategy and data involved in our penguin placements. The last link notes
    to our actual data definition for the coordinates in our game.

- the data definition, including interpretation, of penguin movements for turns
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/2624ea6ba0db731d44e9794d698e32b039b2ac0b/Fish/Player/strategy.py#L20-L21
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/2624ea6ba0db731d44e9794d698e32b039b2ac0b/Fish/Player/strategy.py#L29-L41
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/2624ea6ba0db731d44e9794d698e32b039b2ac0b/Fish/Common/game_tree.py#L11-L15
    - The first two links note our how we interpreted the player strategy for moving penguins.
      The last link notes our definition overall for penguin movements for turns.    

- the unit tests for the penguin placement strategy 
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/2624ea6ba0db731d44e9794d698e32b039b2ac0b/Fish/Player/unit_test/strategy_test.py#L16-L56

- the unit tests for the penguin movement strategy; 
  given that the exploration depth is a parameter `N`, there should be at least two unit tests for different depths 
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/2624ea6ba0db731d44e9794d698e32b039b2ac0b/Fish/Player/unit_test/strategy_test.py#L75-L148
  
- any game-tree functionality you had to add to create the `xtest` test harness:
  - where the functionality is defined in `game-tree.PP`
    - We did not have to add any new code to create the `xtree` test harness. We used
      existing methods in the game tree and defined some code in `xtree` using that
      functionality. We reworked our game tree for other reasons, but worked on the
      test harness with our existing game tree.
  - where the functionality is used in `xtree`
    - Answered by above bullet.
  - you may wish to submit a `git-diff` for `game-tree` and any auxiliary modules 

**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**

  WARNING: all perma-links must point to your commit "2624ea6ba0db731d44e9794d698e32b039b2ac0b".
  Any bad links will result in a zero score for this self-evaluation.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/annettasouth/tree/2624ea6ba0db731d44e9794d698e32b039b2ac0b/Fish>

