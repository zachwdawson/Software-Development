# Software-Development

In this semester long project in our capstone software development class myself and my partners were tasked with building a service for playing games of [FISH](https://images-cdn.fantasyflightgames.com/ffg_content/hey-thats-my-fish-board-game/hey-thats-my-fish-rulebook.pdf).
This required development of game logic, user interface, tournament management, and remote interactions for users. This class had an interesting component 
in that we would switch code bases with other groups throughout the class. Together with my first partner we built the game play service before being moved to a
different code base to build the tournament management system and remote interactions. I chose to include both because there was technical debt that could not
be reasonably fixed in the new code base, resulting in subpar performance. In order to store game states we build a game tree that stores current game state as a node
and successor states as children. We then used a mini-max algorithm to build competent bots that could play against users. This game tree necessitated immutable
game states which were not provided in the code base I inherited. I am confident that our intital design would have run much faster because our game states did not require deep copies
of nodes to be made for each child.


[First Project]https://github.com/zachwdawson/Software-Development/tree/main/game_play/Fish

[Inherited Project]https://github.com/zachwdawson/Software-Development/tree/main/tournament_services/Fish
