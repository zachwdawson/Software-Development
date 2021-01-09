# pleasantvalley

The puprose of this directory is to handle all remote interactions for Fish.com. This includes a server component that accepts client connections and facilitates tournaments and the necessary components to handle client communication. There is also an example client implementation that uses our basic strategy to demonstrate functionality. 

## Directory Structure

The main server component is within `server.py`. This aligns with how previous code was organized since all components
are included in files with self-explanatory names. It is also included within a directory thathints towards its function of enabling remote interactions.

The other main component is in `client.py` which is an example implementation of how a player would connect to our server and process requests. It uses our basic fish strategy to decide its moves. Unfortunately it only looks 1 ahead because the implementation of game tree is too slow to look 2 ahead. We ran a profile on the strategy and 90% of the computing time is spent making deep copies of game states that cannot be removed without making all previous components immutable. We were able to remove some extraneous deep copies but not enough to make looking ahead 2 quick enough. It processes requests acoording to https://www.ccs.neu.edu/home/matthias/4500-f20/remote.html. This file does not exactly make sense to be in this directory as it is not an integral part of the system as much as it is an example of a client implementation but this is the best place for it.

The final component we had to create was the `player_proxy.py` which bridges the gap between the tournament manager and referee to the player with remote interactions. As it implements `PlayerInterface`, it would likely be better suited in the `Player` directory but must be here as it also is part of the Remote task.

## Modification to Code

We had to make 3 relatively major changes to the old codebase in order to function properly. 

1. We had to add new functionality to the tournament manager to keep track of cheaters. Before we simply removed everyone from the player pool that lost or cheated but the server wanted to know how many people were removed for cheating. 

2. We also had to add the ability for the referee to kick players for not responding in time. This required a change to the Player Interface that makes all functions return False if they are not fulfilled quickly enough.

3. Lastly and least importantly, we had to add some functionality to convert states to the proper json representation that we would transmit to clients.