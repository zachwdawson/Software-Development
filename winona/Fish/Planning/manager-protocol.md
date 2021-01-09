# A Specification of Tournament Manager Protocol

Author: Zachary Dawson, Raique Pereira

Repo: Winona

## Introduction

The tournament manager will interact with the referee component of our software
to manage the running of individual games within a broader tournament. 
A tournament manager stores a Tournament_Structure that is independent of the Tournament Manager.
A Tournament structure must contain the logic for allocating a list of players for the Tournament Manager.
This will allow for any tournament fashion that we could choose to implement later (ie. round robin, knockout, etc.).
The tournament manager will run each round to completion before starting the next, constantly checking to see if 
the tournament is over. It will also collect tournament statistics and broadcast tournament information to observers.


### Signup
Signup component will handle tournament signups and allocating players to a tournament manager.

### Player and Referee Allocation to Games
Once the players have been added to a tournament manager, the tournament manager will allocate each player to its
first round game and create referees for each of these games. The Tournament_Structure will be invoked to 
determine how players will be allocated to their games. 

### Management of Rounds
Once each round starts the the tournament manager waits 
until all the games in the current round to finish before allocating players to their next round. This
process continues until there is one player left, who wins the tournament.

### Collect Tournament Statistic
For each game, the winners and the winning score will be visible to all players. There will be game timer
that will be displayed when the game is done to show how long the game took. The final state of the game will 
be available. The tournament will keep track of the amount of players remaining and record how many rounds have 
been played.

### Interact with Participants/Observers
After each game the winners must be notified that they are moving on to the next round and the losers must be 
notified that they lost. Observers will have the opportunity to receive a ongoing game actions. These actions 
will include placements, movements, and relevant game information to all observers.


