## Self-Evaluation Form for Milestone 2

A fundamental guideline of Fundamentals I, II, and OOD is to design
methods and functions systematically, starting with a signature, a
clear purpose statement (possibly illustrated with examples), and
unit tests.

Under each of the following elements below, indicate below where your
TAs can find:

- the data description of tiles, including an interpretation:
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/e61cfad5aa7523f0b6dae05ed1f0d7d0ca2e337b/Fish/Common/fish_tile.py#L2-L16
    - We could have more clearly written our data description of what a tile contains, but
    with a single constructor and interpretation of the parameters this is the closest thing we have.

- the data description of boards, include an interpretation:
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/e61cfad5aa7523f0b6dae05ed1f0d7d0ca2e337b/Fish/Common/fish_board.py#L8-L17
    - We should have been a lot more clear about our representation of boards, including things about
    it being a collection of tiles, but this point onwards in the file shows our representation of boards
    and describes some of the parameters in the constructor.

- the functionality for removing a tile:
  
  - purpose:
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/e61cfad5aa7523f0b6dae05ed1f0d7d0ca2e337b/Fish/Common/fish_board.py#L198
  
  - signature:
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/e61cfad5aa7523f0b6dae05ed1f0d7d0ca2e337b/Fish/Common/fish_board.py#L199
  
  - unit tests:
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/e61cfad5aa7523f0b6dae05ed1f0d7d0ca2e337b/Fish/Common/unit_test/board_test.py#L125-L155

- the functiinality for reaching other tiles on the board:
  - purpose:
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/e61cfad5aa7523f0b6dae05ed1f0d7d0ca2e337b/Fish/Common/fish_board.py#L161
  
  - signature:
    - https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/e61cfad5aa7523f0b6dae05ed1f0d7d0ca2e337b/Fish/Common/fish_board.py#L162
  
  - unit tests:
    -  https://github.ccs.neu.edu/CS4500-F20/annettasouth/blob/e61cfad5aa7523f0b6dae05ed1f0d7d0ca2e337b/Fish/Common/unit_test/board_test.py#L98-L123

The ideal feedback is a GitHub perma-link to the range of lines in specific
file or a collection of files for each of the above bullet points.

  WARNING: all such links must point to your commit "e61cfad5aa7523f0b6dae05ed1f0d7d0ca2e337b".
  Any bad links will result in a zero score for this self-evaluation.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/annettasouth/tree/e61cfad5aa7523f0b6dae05ed1f0d7d0ca2e337b/Fish>

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

In either case you may wish to, beneath each snippet of code you
indicate, add a line or two of commentary that explains how you think
the specified code snippets answers the request.
