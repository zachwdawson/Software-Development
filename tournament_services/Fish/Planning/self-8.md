## Self-Evaluation Form for Milestone 8

Indicate below where your TAs can find the following elements in your strategy and/or player-interface modules:

1. did you organize the main function/method for the manager around
the 3 parts of its specifications --- point to the main function

https://github.ccs.neu.edu/CS4500-F20/dish/blob/8005d7b2c871914a963aa9b91223be676d3b6e7a/Fish/Admin/manager.py#L36-L59

We broke the main method into the 3 main section of notifying players before and after the game, allocating players, determining when the game is over. We us the method inform_players() to tell players the game is starting and finished, the method is_tournament_over() to check if the game is over, and assign_players() to allocate players to each round of the tournament.


2. did you factor out a function/method for informing players about
the beginning and the end of the tournament? Does this function catch
players that fail to communicate? --- point to the respective pieces

inform_players: https://github.ccs.neu.edu/CS4500-F20/dish/blob/8005d7b2c871914a963aa9b91223be676d3b6e7a/Fish/Admin/manager.py#L116-L132

player_interface: https://github.ccs.neu.edu/CS4500-F20/dish/blob/8005d7b2c871914a963aa9b91223be676d3b6e7a/Fish/Player/player.py#L49-L52

This function does catch players who fail to communicate by accepting a boolean from the function call to the player interface. The internal player component is set to always accept messages, but this will work differently once network connections are added.


3. did you factor out the main loop for running the (possibly 10s of
thousands of) games until the tournament is over? --- point to this
function.

https://github.ccs.neu.edu/CS4500-F20/dish/blob/8005d7b2c871914a963aa9b91223be676d3b6e7a/Fish/Admin/manager.py#L45-L52

As the functionality for the main loop was rather short, we did not factor it our into another method but have provided a link to it. We will be sure to factor it out for the next assignment.

**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**


  WARNING: all perma-links must point to your commit "8005d7b2c871914a963aa9b91223be676d3b6e7a".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/dish/tree/8005d7b2c871914a963aa9b91223be676d3b6e7a/Fish>

