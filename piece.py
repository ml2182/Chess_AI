import pygame

class Piece():
    def __init__(self,name,colour,value,algebraic,rect,square_size):
        self.__square_size = square_size
        self.__name = name
        self.__colour = colour
        self.__value = value
        self.__algebraic = algebraic
        self.__rect = rect
        self.__num_moves = 0

    def return_value(self):
        return self.__value
    def display_piece(self,screen):
        surf = pygame.transform.smoothscale(pygame.transform.scale(pygame.image.load("Pieces/"+ self.__colour + self.__algebraic +".png"),(self.__square_size,self.__square_size)).convert_alpha(),(self.__square_size,self.__square_size))
        screen.blit(surf,self.__rect)
    def return_colour(self):
        return self.__colour
    def drag_rect(self,relative_position):
        rect_x = self.__rect[0] + relative_position[0]
        rect_y = self.__rect[1] + relative_position[1]
        self.__rect = (rect_x,rect_y)
    def update_rect(self,rect):
        self.__rect = rect
    def return_algebraic(self):
        return self.__algebraic
    def return_name(self):
        return self.__name
    def add_move_made(self):
        self.__num_moves +=1
    def remove_move_made(self):
        self.__num_moves -=1
    def return_number_of_moves(self):
        return self.__num_moves
    def return_rect(self):
        return self.__rect
class Rook(Piece):
    def __init__ (self, colour,rect,square_size):
        super().__init__("Rook",colour,500,"R",rect,square_size)
        self.__evaluation_squares = [0,  0,  0,  0,  0,  0,  0,  0,
                                     5, 10, 10, 10, 10, 10, 10,  5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                     0,  0,  0,  5,  5,  0,  0,  0]
    def rotate_piece_square_table(self):
        self.__evaluation_squares.reverse()
    def return_piece_square_table(self,position):
        return self.__evaluation_squares[position]
class Bishop(Piece):
    def __init__ (self, colour, rect,square_size):
        super().__init__("Bishop",colour,330,"B",rect,square_size)
        self.__evaluation_squares = [-20,-10,-10,-10,-10,-10,-10,-20,
                                    -10,  0,  0,  0,  0,  0,  0,-10,
                                    -10,  0,  5, 10, 10,  5,  0,-10,
                                    -10,  5,  5, 10, 10,  5,  5,-10,
                                    -10,  0, 10, 10, 10, 10,  0,-10,
                                    -10, 10, 10, 10, 10, 10, 10,-10,
                                    -10,  5,  0,  0,  0,  0,  5,-10,
                                    -20,-10,-10,-10,-10,-10,-10,-20]
    def return_piece_square_table(self,position):
        return self.__evaluation_squares[position]
    def rotate_piece_square_table(self):
        self.__evaluation_squares.reverse()
class Knight(Piece):
    def __init__ (self, colour,rect,square_size):
        super().__init__("Knight",colour,320,"N",rect,square_size)
        self.__evaluation_squares = [-50,-40,-30,-30,-30,-30,-40,-50,
                                    -40,-20,  0,  0,  0,  0,-20,-40,
                                    -30,  0, 10, 15, 15, 10,  0,-30,
                                    -30,  5, 15, 20, 20, 15,  5,-30,
                                    -30,  0, 15, 20, 20, 15,  0,-30,
                                    -30,  5, 10, 15, 15, 10,  5,-30,
                                    -40,-20,  0,  5,  5,  0,-20,-40,
                                    -50,-40,-30,-30,-30,-30,-40,-50]

    def return_piece_square_table(self,position):
        return self.__evaluation_squares[position]
    def rotate_piece_square_table(self):
        self.__evaluation_squares.reverse()
class Queen(Piece):
    def __init__ (self, colour,rect,square_size):
        super().__init__("Queen",colour,900,"Q",rect,square_size)
        self.__evaluation_squares = [-20,-10,-10, -5, -5,-10,-10,-20,
                                    -10,  0,  0,  0,  0,  0,  0,-10,
                                    -10,  0,  5,  5,  5,  5,  0,-10,
                                    -5,  0,  5,  5,  5,  5,  0, -5,
                                     0,  0,  5,  5,  5,  5,  0, -5,
                                    -10,  5,  5,  5,  5,  5,  0,-10,
                                    -10,  0,  5,  0,  0,  0,  0,-10,
                                    -20,-10,-10, -5, -5,-10,-10,-20]
    def return_piece_square_table(self,position):
        return self.__evaluation_squares[position]
    def rotate_piece_square_table(self):
        self.__evaluation_squares.reverse()
class King(Piece):
    def __init__ (self, colour,rect,square_size):
        super().__init__("King",colour,20000,"K",rect,square_size)
        self.__evaluation_squares= [-30,-40,-40,-50,-50,-40,-40,-30,
                                    -30,-40,-40,-50,-50,-40,-40,-30,
                                    -30,-40,-40,-50,-50,-40,-40,-30,
                                    -30,-40,-40,-50,-50,-40,-40,-30,
                                    -20,-30,-30,-40,-40,-30,-30,-20,
                                    -10,-20,-20,-20,-20,-20,-20,-10,
                                    20, 20,  0,  0,  0,  0, 20, 20,
                                    20, 30, 10,  0,  0, 10, 30, 20 ]
        self.__evaluation_squares_end_game = [-50,-40,-30,-20,-20,-30,-40,-50,
                                            -30,-20,-10,  0,  0,-10,-20,-30,
                                            -30,-10, 20, 30, 30, 20,-10,-30,
                                            -30,-10, 30, 40, 40, 30,-10,-30,
                                            -30,-10, 30, 40, 40, 30,-10,-30,
                                            -30,-10, 20, 30, 30, 20,-10,-30,
                                            -30,-30,  0,  0,  0,  0,-30,-30,
                                            -50,-30,-30,-30,-30,-30,-30,-50]          ###https://www.chessprogramming.org/Simplified_Evaluation_Function
        self.__current_evaluation_squares = self.__evaluation_squares
    def return_piece_square_table(self,position):
        return self.__current_evaluation_squares[position]
    def set_piece_square_table_end_game(self):
        self.__current_evaluation_squares = self.__evaluation_squares_end_game
    def is_in_end_game(self):
        if self.__current_evaluation_squares == self.__evaluation_squares_end_game:
            return True
        return False
    def set_piece_square_table(self):
        self.__current_evaluation_squares = self.__evaluation_squares
    def rotate_piece_square_table(self):
        self.__evaluation_squares.reverse()

class Pawn(Piece):
    def __init__ (self, colour,rect,square_size):
        super().__init__("Pawn",colour,100,"p",rect,square_size)
        self.__evaluation_squares = [0,  0,  0,  0,  0,  0,  0,  0,
                                    50, 50, 50, 50, 50, 50, 50, 50,
                                    10, 10, 20, 30, 30, 20, 10, 10,
                                    5,  5, 10, 25, 25, 10,  5,  5,
                                    0,  0,  0, 20, 20,  0,  0,  0,
                                    5, -5,-10,  0,  0,-10, -5,  5,
                                    5, 10, 10,-20,-20, 10, 10,  5,
                                    0,  0,  0,  0,  0,  0,  0,  0]
    def return_piece_square_table(self,position):
        return self.__evaluation_squares[position]
    def rotate_piece_square_table(self):
        self.__evaluation_squares.reverse()