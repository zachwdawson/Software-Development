# README

## Common
Common is the base directory within the Fish broject in which all directories go. It also stores some project wide files like const.py and structure.py.

### const.py
Const stores important global constants for rendering the game as well as and important numbers or strings for game rules like maximum fish.

### main.py
Main currently createes a board and renders it to the screen. It does nothing else as of 10/8/20.

### structures.py
Structures stores the important data structures of our system like Tile, Coordinate, and Hexagon. Each of these allows for easy data representation of an important game piece and will allow for linting in the future.

### state.py
State maintains the state of the game including the board and the players locations and other important attributes like score and age of players.

## Controllers

### fish_game_controller.py
The fish controller takes the board representation from the model and passes it off to the model to be rendered.

## Model
Model stores files that include game logic currently and will include any other data representations and logic in the future.

### fish_game_model.py
The fish game model controls all the internal logic for maintaing a game board with tiles being the only current functionality. In the future it will also store players.

## Resources
Holds pictures.

### fish.png
Fish image used for rendering.

### penguin'X'.png
6 penguin images, one for each player.

## unit_test
Unit_test holds all the unit tetss and the scripts necessary to run them.

### fish_game_model_test.py
This tests the functionality of the game model.

### milestone_2_game_pieces_tests.py
This runs all the unit tests written for milestone 2.

### game_state_test.py
This tests the functionality of state.py

### milestone_2_game_pieces_tests.py
This runs all the unit tests written for milestone 3.

## Views
Views stores the GUIs that the users will eventually see.

### hexgrid_view.py
This view creates a board window with tiles, fish, and penguins.

# Tests
- To run the test harness for each milestone, you need to run .test/milestone_x_... from the Common directory with no arguments.
- To run the entire unit test harness run ./xtest in Common
- To run integration tests, see directory winona/'x' where x is the milestone number and run corresponding script.
  * To run for milestone 3 run ./xboard in directory 3
