## Self-Evaluation Form for Milestone 2

A fundamental guideline of Fundamentals I, II, and OOD is to design
methods and functions systematically, starting with a signature, a
clear purpose statement (possibly illustrated with examples), and
unit tests.

Under each of the following elements below, indicate below where your
TAs can find:

- the data description of tiles, including an interpretation:
/Fish/Common/structures.py lines 11-57
The tile is represented by a Python NamedTuple that stores its row and column location, the row and column of its six neighbors (None if no neighbor in that direction exists), whether or not it is a tile or a hole, and the number of fish.

- the data description of boards, include an interpretation:
/Fish/Common/model/fish_game_model.py lines 7-41
The board is represented by a 2 dimensional list of Tile Tuples as well as the number or rows and columns.

- the functionality for removing a tile:
  - purpose:
  /Fish/Common/model/fish_game_model.py line 82
  provides purpose of removing tile from board.
  
  - signature:
  /Fish/Common/model/fish_game_model.py line 81
  provides representation fo input for add_hole()
  
  - unit tests:
  /Fish/Common/test/fish_game_model_test.py lines 109-113
  Test to see that removing a tile from a board modifies the correct attribute of the hole that is being removed.

- the functiinality for reaching other tiles on the board:
  - purpose:
  /Fish/Common/model/fish_game_model.py line 63
  provides purpose of finding reachable tiles from given tile coordinates.
  
  - signature:
  /Fish/Common/model/fish_game_model.py line 62
  provides input descriptions for the function.
 
  - unit tests:
  /Fish/Common/test/fish_game_model_test.py lines 78-107
  Test to see that correct tiles are found for boards with and without holes.
  

The ideal feedback is a GitHub perma-link to the range of lines in specific
file or a collection of files for each of the above bullet points.

  WARNING: all such links must point to your commit "a3e9634a0ed5f089b3a6eade74ce6ac84651accb".
  Any bad links will result in a zero score for this self-evaluation.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/winona/tree/a3e9634a0ed5f089b3a6eade74ce6ac84651accb/Fish>

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

In either case you may wish to, beneath each snippet of code you
indicate, add a line or two of commentary that explains how you think
the specified code snippets answers the request.
