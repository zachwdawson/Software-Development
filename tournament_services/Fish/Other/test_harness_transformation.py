import fileinput

from Fish.Common.representations.enumerations.directions_enum import HexDirection
from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Common.representations.fish_board import FishBoardModel
from Fish.Common.representations.game_state import FishGameStateFactory, FishGameState


class TestHarnessTransformationHelper(object):
    """
    Class to help us transform the given JSON representations for test harnesses
    into our internal representation
    """

    @staticmethod
    def read_from_stdin():
        """
        Purpose: Reads a given file from the stdin line-by-line
        Signature: Void -> String
        :return: String with parsed line-by-line input
        """
        stdin_str = ""
        for line in fileinput.input():
            stdin_str += line
        return stdin_str

    @staticmethod
    def parse_board(board_json):
        """
        Purpose: Parse the board representation into our internal representation
        Signature: JSONArray of JSONArrays -> FishBoardModel
        :param board_json: Parsed JSON array representation of a Fish game board
        :return: An instance of our board model
        """
        coords_to_holes = []
        for i, row in enumerate(board_json):
            for j, val in enumerate(row):
                y_coord = i
                x_coord = 2 * j if i % 2 == 0 else 1 + 2 * j
                coords_to_holes.append(((x_coord, y_coord), val))
        amount_rows = len(board_json)
        amount_cols = max([len(row) for row in board_json])
        board = FishBoardModel.create_with_coords_to_fish(amount_rows, amount_cols, coords_to_holes)
        return board

    @staticmethod
    def convert_board_to_json(board):
        """
        Purpose: Convert our board representation back to JSON
        Signature: FishBoardModel -> Board
        :param board: Our internal representation of a board
        """
        overall_board = []
        current_row = []
        current_row_y = 0
        for x, y in board.get_coords_sorted_by_row():
            if y != current_row_y:
                overall_board.append(current_row)
                current_row = []
                current_row_y = y
            tile = board.get_tile_at_coord(x, y)
            if tile:
                num_fish = tile.num_fish
            else:
                num_fish = 0
            current_row.append(num_fish)
        overall_board.append(current_row)
        return overall_board

    @staticmethod
    def convert_to_double_height(row_pos, column_pos):
        """
        Purpose: Turn point from integration test representation into double-height coordinates
        used by our internal representation
        Signature: Int Int -> Coordinate
        :param row_pos: Row position in integration test representation
        :param column_pos: Column position in integration test representation
        :return: Our double height
        """
        y_coord = row_pos
        x_coord = 2 * column_pos if row_pos % 2 == 0 else 1 + 2 * column_pos
        return x_coord, y_coord

    @staticmethod
    def convert_back_to_posn(x, y):
        """
        Purpose: Convert our double_height coordinates to Posn coordinate system of
        [row position, column position]
        Signature: Int Int -> Posn
        :param x: x position of our double height coordinate
        :param y: y position of our double height coordinate
        """
        row_pos = y
        col_pos = int(x / 2)
        return [row_pos, col_pos]

    @staticmethod
    def convert_action_to_json_rep(action):
        """
        Purpose: Convert our action representation to JSON representation which
                 contains two posns
        Signature: Action -> [Posn, Posn]
        :param action: Action that is our internal representation and not the test harnesses
                       interpretation
        :return: Action in the test harnesses JSON serializable representation
        """
        from_pos, to_pos = action
        return [TestHarnessTransformationHelper.convert_back_to_posn(from_pos[0], from_pos[1]),
                TestHarnessTransformationHelper.convert_back_to_posn(to_pos[0], to_pos[1])]

    @staticmethod
    def create_state(state_json):
        """
        Purpose: Create the state_json based on the passed in JSON object representation
        Signature: State -> FishGameState
        :param state_json: Object of players as specified containing ordering and player information
        :return: Our internal representation of a game state_json
        """
        board = TestHarnessTransformationHelper.parse_board(state_json['board'])
        player_info_list = TestHarnessTransformationHelper.create_player_info_list(state_json['players'])
        game_state = FishGameStateFactory.create_move_penguins_state(board, player_info_list,
                                                                     check_penguin_amount=False)
        return game_state

    @staticmethod
    def convert_state_to_json(state: FishGameState):
        board = TestHarnessTransformationHelper.convert_board_to_json(state.get_board())
        player_order = state.get_player_order()
        current_player_index = player_order.index(state.get_current_turn())
        players = [{
            "color": color.value,
            "score": state.get_fish_for_player(color),
            "places": [TestHarnessTransformationHelper.convert_back_to_posn(coordinate[0], coordinate[1]) for coordinate in state.get_penguins_for_player(color)]
        } for color in player_order[current_player_index:] + player_order[:current_player_index]]
        return {"players": players, "board": board}

    @staticmethod
    def create_player_info_list(players_list):
        """
        Purpose: Turn information from unit test into a player information tuple
        that can be used by our game state creation methods
        Signature: [Dictionary] -> (int, Coordinate, int)
        :param players_list: Specified well-formed list of players that we are parsing and turning into
        something usable by our internal representation
        :return: List of players converted into something usable by our internal representation
        """
        ret_list = []
        for player in players_list:
            # turn into our representation
            penguins = [TestHarnessTransformationHelper.convert_to_double_height(pos[0], pos[1])
                        for pos in player['places']]
            player_color = None
            for color in PlayerColor:
                if color.value == player['color']:
                    player_color = color
                    break
            fish = player['score']
            player_tuple = (player_color, penguins, fish)
            ret_list.append(player_tuple)
        return ret_list

    @staticmethod
    def find_coord_neighbors(coord):
        """
        Purpose: Find all the neighbors from a specific coordinates
        Signature: Coordinate -> List[Coordinate
        :param coord: Coordinate that we want to find neighbors for
        :return: boolean representing whether a move happened or not
        """
        move_list = []
        direction_list = [HexDirection.NORTH, HexDirection.NORTHEAST, HexDirection.SOUTHEAST,
                          HexDirection.SOUTH, HexDirection.SOUTHWEST, HexDirection.NORTHWEST]
        for direction in direction_list:
            move_to_pos = coord[0] + direction.value[0], \
                          coord[1] + direction.value[1]
            move_list.append(move_to_pos)
        return move_list
