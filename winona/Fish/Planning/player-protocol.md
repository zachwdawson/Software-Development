# A Specification of Player Protol

Author: Zachary Dawson, Raique Pereira

Repo: Winona

## Introduction

The Fish API functions using the TCP protocol. All incoming and outgoing messages will be in the format of JSON. Each endpoint will represent a common game action. Game participants will be able to use the API to query about the state of game as well as check the validity and make moves. All requests must come with the "action" field to decide which action should be taken. The messages will then be routed to their corresponding function accordingly.

## Authentication

The join tournament request enables users to join a specific tournament based on the tournaments ID 
which will be created in the tournament user-interface. They will also need to provide a credit card in 
order to pay the entry fee. In return they will receive their color for the game, the SHA token that 
will be used to validate further user requests.

Authentication will be handled using SHA tokens sent to players upon entering a tournament. 
All of these requests must be sent to port 45678 on the host "fish.game.com". 
the SHA token must be used in all further to authenticate player identity within games.

join_request:
```
{
    "action": "join_tournament"
    "tournament_id": xxxxxxx,
    "credit_card": xxxx-xxxx-xxxx-xxxx
}
```

join_response:
```
{
    "user_token": XXXXXXXXXXXXX,
    "color": str
}
```
## Game-Play Requests and Responses

### check_placement
Check_placement requires the action "check_placement". The user specifies the desired row and column for the placement. The API will return a boolean "is_valid" that is True if the placement will not return an error, otherwise it will return false.

request format:
```
{
    "action": "check_placement",
    "user_token": XXXXXXXXXXXXX,
    "row": int,
    "col": int
}
```

response format:
```
{
    "is_valid": boolean,
}
```

### place_penguin
Place_penguin requires the "action" "place_penguin". The user will specify the row and column at which the penguin will be placed. Place_penguin will return Invalid_Coordinate errors if a coordinate is not in the board, is a hole, or already has a penguin on it. The place_penguin action will return a Invalid_Token error if it not this players turn to place the penguin. On any error, this players penguin will be removed from the game. On success, place_penguin returns the resulting STATE of the penguin placement.

request format:
```
{
    "action": "place_penguin",
    "user_token": XXXXXXXXXXXXX,
    "row": int,
    "col": int
}
```

response format:
```
{
    "result_state": STATE,
}
```
### check_move
Check_move requires the "action" "check_move". The user will specify
 the start and end locations of the movement as "start_row", "start_col", "end_row", "end_col".
 If the move is valid, the response will be true and false if it is not valid.

request format:
```
{
    "action": "check_move",
    "user_token": XXXXXXXXXXXXX,
    "start_row": int,
    "start_col": int,
    "end_row": int,
    "end_col": int
}
```

response format:
```
{
    "is_valid": boolean
}
```
### move_penguin

Move_penguin requires the "action" "move_penguin". The user will specify
 the start and end locations of the movement as "start_row", "start_col", "end_row", "end_col".
 If the move is valid, the request will return the state of the game after this move has been performed.
 If the start coordinate or end coordinate is outside the bounds of the board or is a hole, the function will return 
 Invalid_Coordinate error. If the move is illegal because it attempts to jump another penguin or a hole it will 
 return an Invalid_Action error. If the player plays out of turn, this call will return and Invalid_Token error.
 On any error, this players penguin will be kicked from the game.

request format:
```
{
    "action": "move_penguin",
    "user_token": XXXXXXXXXXXXX,
    "start_row": int,
    "start_col": int,
    "end_row": int,
    "end_col": int
}
```

response format:
```
{
    "result_state": STATE
}
```
### check_turn

Check_turn requires the "action" "check_turn". This API call will return the player's whose turn it currently is to either place a penguin or move a penguin.

request format:
```
{
    "action": "check_turn",
    "user_token": XXXXXXXXXXXXX
}
```

response format:
```
{
    "color": str
}
```

### get_state

Check_turn requires the "action" "get_state". This API call will return the current STATE of the game.


request format:
```
{
    "action": "get_state",
    "user_token": XXXXXXXXXXXXX
}
```

response format:
```
{
    "current_state": STATE 
}
```

### get_moves_for_color

Check_turn requires the "action" "get_moves_for_color". The other argument required is the "color" of the penguin whose moves are being checked.
 This API call will return an array of ACTION that represent possible moves for the given player. This call will return an Unknown_Color error
 if the given color is not in the current game.


request format:
```
{
    "action": "get_moves_for_color",
    "user_token": XXXXXXXXXXXXX,
    "color": str
}
```

response format:
```
{
    "reachable_locations": [ACTION] 
}
```

### get_moves_for_location

Check_turn requires the "action" "get_moves_for_location". The other arguments required are the "row" and "col" of the location whose moves will be checked.
 This API call will return an array of ACTION that represent possible moves from the given location. 
 This API call will return an Invalid_Coordinate error if the row and column is out of bounds on the board or is a hole.

request format:
```
{
    "action": "get_moves_for_location",
    "user_token": XXXXXXXXXXXXX,
    "row": int,
    "col": int
}
```

response format:
```
{
    "reachable_locations": [ACTION] 
}
```

### is_game_over
Check_turn requires the "action" "is_game_over". This API call will return true if the game has no more possible moves for any player and false if any player has a move.


request format:
```
{
    "action": "is_game_over",
    "user_token": XXXXXXXXXXXXX
}
```

response format:
```
{
    "is_game_over": boolean
}
```

## JSON Representations

### STATE
STATE is a JSON object of "players" and "board". Players is a list of PLAYER.

    { 
        "players" : [PLAYER, ..., PLAYER],
        "board" : BOARD 
    }
        
### PLAYER
Player is a JSON object that holds the relevant information for a player in the game.
It holds the players color, score, and the locations of its penguins.

    { 
        "color" : str,
    
        "score" : int,
    
        "places" : [COORDINATE, ..., COORDINATE] 
    }

### COORDINATE
A coordinate is a JSON object that represents a location on the board as a row and column.

    { 
        "row" : int,
        "col" : int,
    }
    
### ACTION
An action represents a penguin movement as two COORDINATE, start and end.

    {
        "start": COORDINATE,
        "end": COORDINATE
    }

### BOARD
A board is a two dimensional array of integers. Each of the first order arrays represents a row and each
integer within the row represents the number of fish on the tile in that location.

    [
        [int],
        [int],
        [int]
    ]

## Errors

If an error occurs during an endpoint call. An error message will be returned in the following format:
```
{
    "error_type": Invalid_Coordinate|Invalid_Action|Incorrect_Token|Unknown_Action|Unknown_Color|Tournament_Error
    "error_message": str
}
```

Each type represents a specific type of error. Each error will come with a helpful error message corresponding that tells
users what caused the error.

### Potential Causes

Invalid_Coordinate
- Coordinate out of bounds
- Coordinate is a hole
- Coordinate is already occupied

Invalid_Action
- Attempt to move to hole
- Attempt to move to occupied tile
- Attempt to jump hole
- Attempt to jump occupied tile
- Attempt to move out of turn

Incorrect_Token
- Use token that was not administered by server

Unknown_Action
- Attempt to use endpoint that does not exist

Unknown_Color
- Color does not exist in this game

Tournament_Error
- General tournament failure/ server failure