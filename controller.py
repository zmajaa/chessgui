from configurations import *
import model
import piece

class Controller():
    def __init__(self):
        self.init_model()

    def init_model(self):
        self.model=model.Model()

    def reset_game_data(self):
        self.model.reset_game_data()

    def reset_to_initial_locations(self):
        self.model.reset_to_initial_locations()

    def get_numeric_notation(self, position):
        return piece.get_numeric_notation(position)

    def get_alphanumeric_position(self, rowcol):
        return self.model.get_alphanumeric_position(rowcol)
        # if self.is_on_board(rowcol):
        #     row, col = rowcol
        #     return "{}{}".format(X_AXIS_LABELS[col],Y_AXIS_LABELS[row])
        # def is_on_board(self, rowcol):
        #     row, col = rowcol
        #     return 0 <= row <= 7 and 0 <= col <= 7

    def get_piece_at(self, position_of_click):
        return self.model.get_piece_at(position_of_click)

    def pre_move_validation(self, start_pos, end_pos):
        return self.model.pre_move_validation(start_pos, end_pos)

    def get_all_peices_on_chess_board(self):
        return self.model.items()

    def player_turn(self):
        return self.model.player_turn

    def moves_available(self, position):
        return self.model.moves_available(position)
