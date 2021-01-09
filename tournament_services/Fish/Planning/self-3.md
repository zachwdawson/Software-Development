## Self-Evaluation Form for Milestone 3

Under each of the following elements below, indicate below where your
TAs can find:

- the data description of states, including an interpretation
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/6cd9814bb0a303349e0b7294de33ebe7a3daa4ba/Fish/Common/representations/game_state.py#L21-L46
    - This describes our state object and includes an interpretation so we thought this explained what a "state" was
      in our representation
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/6cd9814bb0a303349e0b7294de33ebe7a3daa4ba/Fish/Common/representations/game_state.py#L21-L46
    - This is where we describe the different phases inside a game, so we also thought this showed a data
      description of what the different "states" could be.

- a signature/purpose statement of functionality that creates states 
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/6cd9814bb0a303349e0b7294de33ebe7a3daa4ba/Fish/Common/representations/game_state.py#L288-L299
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/6cd9814bb0a303349e0b7294de33ebe7a3daa4ba/Fish/Common/representations/game_state.py#L288-L299
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/6cd9814bb0a303349e0b7294de33ebe7a3daa4ba/Fish/Common/representations/game_state.py#L332-L334
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/6cd9814bb0a303349e0b7294de33ebe7a3daa4ba/Fish/Common/representations/game_state.py#L381-L383
    - We broke out our creation of states into different factory methods that could create states at different points, so
      these links show all of the different signatures/purpose statements.

- unit tests for functionality of taking a turn
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/6cd9814bb0a303349e0b7294de33ebe7a3daa4ba/Fish/Common/unit_test/game_state_test.py#L39-L93
    - This is all the lines where we test moving a penguin, which we interpreted as taking a turn. 

- unit tests for functionality of placing an avatar 
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/6cd9814bb0a303349e0b7294de33ebe7a3daa4ba/Fish/Common/unit_test/game_state_test.py#L95-L132

- unit tests for functionality of final-state test
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/6cd9814bb0a303349e0b7294de33ebe7a3daa4ba/Fish/Common/unit_test/game_state_test.py#L134-L154
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/6cd9814bb0a303349e0b7294de33ebe7a3daa4ba/Fish/Common/unit_test/create_state_test.py#L137-L147
    - For this second link, we made the end-game coded into our game so this test checks that constructing an
      end-game state means constructing a state where players can't move (i.e. a final-state).

The ideal feedback is a GitHub perma-link to the range of lines in specific
file or a collection of files for each of the above bullet points.

  WARNING: all such links must point to your commit "6cd9814bb0a303349e0b7294de33ebe7a3daa4ba".
  Any bad links will result in a zero score for this self-evaluation.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/annettasouth/tree/6cd9814bb0a303349e0b7294de33ebe7a3daa4ba/Fish>

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

In either case you may wish to, beneath each snippet of code you
indicate, add a line or two of commentary that explains how you think
the specified code snippets answers the request.

## Partnership Eval 

Select ONE of the following choices by deleting the other two options.

B) My partner and I contributed not *exactly* equally, but *roughly*
   equally to this assignment.
  
Explanation: Jason has been in the driver seat more often than Vlad.
Vlad is newer to computer science (coming to it a year ago) while Jason is a 5th-year who
has been on multiple co-ops. Despite this Vlad has been getting up to speed well and we
have been working well together. We are trying to put Vlad in the driver seat more often and hope
to move to more and more equality in contribution as the semester goes on.