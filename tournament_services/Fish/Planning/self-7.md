## Self-Evaluation Form for Milestone 7

Please respond to the following items with

1. the item in your `todo` file that addresses the points below.
    It is possible that you had "perfect" data definitions/interpretations
    (purpose statement, unit tests, etc) and/or responded to feedback in a 
    timely manner. In that case, explain why you didn't have to add this to
    your `todo` list.

2. a link to a git commit (or set of commits) and/or git diffs the resolve
   bugs/implement rewrites: 

These questions are taken from the rubric and represent some of the most
critical elements of the project, though by no means all of them.

(No, not even your sw arch. delivers perfect code.)

### Board

- a data definition and an interpretation for the game _board_

TODO: [X]insufficient interpretation of the board, no explaination of what holes mean? how the data definition represents a real game board. The comments on FishBoardModel class should have all these explanations.

Fix: https://github.ccs.neu.edu/CS4500-F20/dish/commit/2cfff53c333f43a48c7c8c42784f2c9dbddb5656

- a purpose statement for the "reachable tiles" functionality on the board representation

The reachable tiles functionality already had a purpose statement that was sufficient so we did not have to rewrite it.

https://github.ccs.neu.edu/CS4500-F20/dish/blob/de939d26dc585c4daa0b2f0068494a4c5634f550/Fish/Common/representations/fish_board.py#L197


- two unit tests for the "reachable tiles" functionality

We already had the proper amount of unit tests so we did not have to add any for reachable tiles.

https://github.ccs.neu.edu/CS4500-F20/dish/blob/de939d26dc585c4daa0b2f0068494a4c5634f550/Fish/Common/unit_test/board_test.py#L95-L132


### Game States 


- a data definition and an interpretation for the game _state_

TODO: [X]insufficient interpretation of the game state- no explanation on how players are related to penguins and how penguins' locations are tracked, how player turn is tracked

Fix: https://github.ccs.neu.edu/CS4500-F20/dish/commit/2cfff53c333f43a48c7c8c42784f2c9dbddb5656


- a purpose statement for the "take turn" functionality on states

TODO: [X]data definition or interpretation for game states. - can_any_player_move - little unclear implementation of current player turn - maybe return the id of player who can play??

Fix: https://github.ccs.neu.edu/CS4500-F20/dish/commit/bb12ea7c2831bbe2a7bc6ad59594364d554aeaf4


- two unit tests for the "take turn" functionality 

TODO: [X]sufficient coverage of unit tests for turn-taking functionality, coverage for player turns changing isnt there

Fix: https://github.ccs.neu.edu/CS4500-F20/dish/commit/a9dcb796e4085c6f002b5ccbb8f49a796081faac


### Trees and Strategies


- a data definition including an interpretation for _tree_ that represent entire games

TODO: [X]it is unclear that the generation of a tree is suspended, no explaination for usage of yield

[X]it is unclear if the game tree node can represent all two kinds of nodes: game-is-over, current-player-is-stuck

[X]no explanation of a lazy ("caching") scheme of the game tree generation or documentation

All fixed in: https://github.ccs.neu.edu/CS4500-F20/dish/commit/f7ca0ca48279be5bd931a76255658fd970ba2555


- a purpose statement for the "maximin strategy" functionality on trees

We did not have to add a purpose statement for the maximin strategy since we already had a sufficient one.

https://github.ccs.neu.edu/CS4500-F20/dish/blob/de939d26dc585c4daa0b2f0068494a4c5634f550/Fish/Player/strategy.py#L103-L105


- two unit tests for the "maximin" functionality 

We had two tests for the maximin functionality so we did not have to add any.

https://github.ccs.neu.edu/CS4500-F20/dish/blob/de939d26dc585c4daa0b2f0068494a4c5634f550/Fish/Player/unit_test/strategy_test.py#L126-L131


### General Issues

Point to at least two of the following three points of remediation: 


- the replacement of `null` for the representation of holes with an actual representation 


- one name refactoring that replaces a misleading name with a self-explanatory name

We have not made a lot of changes to names but one can be found at https://github.ccs.neu.edu/CS4500-F20/dish/commit/1b5867c579fc9637ca697703fe956864701ca873. This rename made sense as originally it said coords_with_holes which was misleading as it is actually coords without holes.


- a "debugging session" starting from a failed integration test:
  - the failed integration test
  - its translation into a unit test (or several unit tests)
  - its fix
  - bonus: deriving additional unit tests from the initial ones 
  
  https://github.ccs.neu.edu/CS4500-F20/dish/commit/5703d1779b5f0156122c2467dbea18e11c9c6f24
  
  No unit tests just a fix.


### Bonus

Explain your favorite "debt removal" action via a paragraph with
supporting evidence (i.e. citations to git commit links, todo, `bug.md`
and/or `reworked.md`).

Our favorite debt removal was adding turns because it was the most major debt removal that we had. Besides this one we did not have many that were more complex than elaborating on data definitions or adding tests. The change can be found here https://github.ccs.neu.edu/CS4500-F20/dish/commit/bb12ea7c2831bbe2a7bc6ad59594364d554aeaf4. It was an especially interresting refactor because it was a pretty massive oversight for a game state to not take care of turns and required quite a bit of thinking to make the current design work with the new design.



