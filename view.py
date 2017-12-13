from tkinter import *
from configurations import *
import tkinter.messagebox
from controller import *
from PIL import Image, ImageTk
import exceptions


class View:
    selected_piece_position = None
    def __init__(self, root, kontroler):
        self.root=root
        self.all_squares_to_be_highlighted=[]
        self.images = dict()
        self.controller = kontroler
        self.board_color_1=BOARD_COLOR_1
        self.board_color_2=BOARD_COLOR_2
        self.create_chess_base()
        #creating bottom frame
        self.btmfrm = Frame(root, height=64)
        self.info_label = Label(self.btmfrm, text="   White to Start the Game  ", fg=self.board_color_2)
        self.info_label.pack(side=RIGHT, padx=8, pady=5)
        self.btmfrm.pack(fill="x", side=BOTTOM)
        #starting game
        self.start_new_game()
        self.canvas.bind("<Button-1>", self.on_square_clicked)





    def create_chess_base(self):
        self.create_top_menu()
        self.create_canvas()
        self.draw_board()
        self.create_bottom_frame()

    def create_top_menu(self):
        self.menu_bar = Menu(self.root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        # everything added to meni is here
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu=Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.file_menu)

        self.about_menu=Menu(self.menu_bar, tearoff=0)
        self.about_menu.add_command(label="About",command=self.show_about)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)
        self.root.configure(menu=self.menu_bar)

    def show_about(self):
        tkinter.messagebox.showinfo(PROGRAM_NAME, "Tkinter GUI Application\nDevelopment Blueprints")

    def create_bottom_frame(self):
        pass

    def create_canvas(self):
        canvas_width = NUMBER_OF_COLUMNS *DIMENSION_OF_EACH_SQUARE
        canvas_height = NUMBER_OF_ROWS * DIMENSION_OF_EACH_SQUARE
        self.canvas = Canvas(self.root, width=canvas_width, height=canvas_height)
        self.canvas.pack(padx=8, pady=8)


    def draw_board(self):
        current_color = BOARD_COLOR_2
        for row in range(NUMBER_OF_ROWS):
            current_color = self.get_alternate_color(current_color)
            for col in range(NUMBER_OF_COLUMNS):
                x1, y1 = self.get_x_y_coordinate(row, col)
                x2, y2 = x1 + DIMENSION_OF_EACH_SQUARE, y1 + DIMENSION_OF_EACH_SQUARE
                if(self.all_squares_to_be_highlighted and (row,col) in self.all_squares_to_be_highlighted):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=HIGHLIGHT_COLOR)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=current_color)
                    current_color = self.get_alternate_color(current_color)

    def get_x_y_coordinate(self, row, col):
        x = (col * DIMENSION_OF_EACH_SQUARE)
        y = ((7 - row) * DIMENSION_OF_EACH_SQUARE)
        return (x, y)

    def get_alternate_color(self, current_color):
        if current_color == self.board_color_2:
            next_color = self.board_color_1
        else:
            next_color = self.board_color_2
        return next_color

    def on_square_clicked(self, event):
        clicked_row, clicked_column =self.get_clicked_row_column(event)
        print("Hey you clicked on", clicked_row, clicked_column)
        position_of_click =self.controller.get_alphanumeric_position((clicked_row, clicked_column))
        print("Hey you clicked on", position_of_click)
        if self.selected_piece_position:  # on second click
            # print("Hey you now clicked on", position_of_click)
            self.shift(self.selected_piece_position,position_of_click)
            self.selected_piece_position = None
        self.update_highlight_list(position_of_click)
        self.draw_board()
        self.draw_all_pieces()

    def get_clicked_row_column(self, event):
        col_size = row_size = DIMENSION_OF_EACH_SQUARE
        clicked_column = event.x // col_size
        clicked_row = 7 - (event.y // row_size)
        return (clicked_row, clicked_column)

    def draw_single_piece(self, position, piece):
        x, y = self.controller.get_numeric_notation(position)
        if piece:
            filename = "./pieces_image/{}_{}.png".format(piece.name.lower(), piece.color)
            if filename not in self.images:
                self.images[filename] = ImageTk.PhotoImage(file=filename)
            x0, y0 = self.calculate_piece_coordinate(x, y)
            self.canvas.create_image(x0, y0, image=self.images[filename], tags=("occupied"), anchor="c")

    def calculate_piece_coordinate(self, row, col):
        x0 = (col * DIMENSION_OF_EACH_SQUARE) + int(DIMENSION_OF_EACH_SQUARE / 2)
        y0 = ((7 - row) * DIMENSION_OF_EACH_SQUARE) + int(DIMENSION_OF_EACH_SQUARE / 2)
        return (x0, y0)

    def draw_all_pieces(self):
        self.canvas.delete("occupied")
        for position, piece in self.controller.get_all_peices_on_chess_board():
            self.draw_single_piece(position, piece)

    def start_new_game(self):
        self.controller.reset_game_data()
        self.controller.reset_to_initial_locations()
        self.draw_all_pieces()

    def shift(self, start_pos, end_pos):
        selected_piece = self.controller.get_piece_at(start_pos)
        piece_at_destination =self.controller.get_piece_at(end_pos)
        if not piece_at_destination or piece_at_destination.color != selected_piece.color:
            try:
                self.controller.pre_move_validation(start_pos,end_pos)
            except exceptions.ChessError as error:
                self.info_label["text"] = error.__class__.__name__
            else:
                self.update_label(selected_piece, start_pos,end_pos) #careful

    def update_label(self, p1,p2):
        self.info_label["text"] = '' + piece.color.capitalize() + "  :  " + p1 + p2 + '    '  '\'s turn'

    def update_highlight_list(self, position):
        self.all_squares_to_be_highlighted = None
        try:
            piece = self.controller.get_piece_at(position)
        except:
            piece = None
        if piece and (piece.color == self.controller.player_turn()):
            self.selected_piece_position = position
            self.all_squares_to_be_highlighted = list(map(self.controller.get_numeric_notation,self.controller.get_piece_at(position).moves_available(position)))






#main
root = Tk()
root.title(PROGRAM_NAME)
View(root, Controller())
root.mainloop()

