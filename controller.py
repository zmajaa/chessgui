from configurations import *
import model
import piece

class Controller():
    def __init__(self):
        self.init_model()

    def init_model(self):
        self.model=model.Model()

    def get_all_peices_on_chess_board(self):
        return self.model.items()

    def reset_game_data(self):
        self.model.reset_game_data()

    def reset_to_initial_locations(self):
        self.model.reset_to_initial_locations()

    def get_numeric_notation(self, position):
        return piece.get_numeric_notation(position)
    #added methods
    def get_alphanumeric_position(self, rowcol):
        if self.is_on_board(rowcol):
            row, col = rowcol
            return "{}{}".format(X_AXIS_LABELS[col],Y_AXIS_LABELS[row])
    def is_on_board(self, rowcol):
        row, col = rowcol
        return 0 <= row <= 7 and 0 <= col <= 7