from board import Board
from engine import Engine
from stack import Stack
import pygame

class Chess():
    def __init__(self,screen,mouse,board_dimension):
        self.__mouse = mouse
        self.__screen = screen
        self.__board = Board(board_dimension,self.__mouse)
        self.__selected_piece_position = 100
        self.__player1_colour = None
        self.__player2_colour = None
        self.__AI = None
        self.__mode = None
        self.__colour_to_move = None
    
    def set_up_playing_condition(self,player1,AI_difficulty,mode,fen): # sets up game conditions for the given mode
        self.__mode = mode
        if player1 == "w":
            self.__player1_colour = "w"
            self.__player2_colour = "b"
        else:
            self.__player1_colour = "b"
            self.__player2_colour = "w"
        if self.__mode == "Puzzles":
            self.__colour_to_move = self.__player1_colour
        else:
            self.__colour_to_move = "w" if "w" in fen else "b"
        self.__board.create_board_set_up(self.__player1_colour,fen)
        self.__board.display_board(self.__screen)
        self.__board.display_pieces(self.__screen)
        if self.__mode == "AI":
            pygame.display.update()
            self.add_engine(AI_difficulty)

    def add_engine(self,AI_difficulty): # makes the engine the 2nd player
        self.__AI = Engine(self.__board,self.__player2_colour,AI_difficulty)
        if self.__player1_colour == "b":
            self.AI_move()

    def select_piece(self): # allows the user to select a piece in game
        if self.__board.return_move_log().length()%2 == 0:
            self.__colour_to_move = "w"
        else:
            self.__colour_to_move = "b"
        if not(self.__board.check_if_draw_by_repetition()): # prevents users from being able to move when its a draw
            self.__board.all_legal_moves(self.__colour_to_move)
            self.__selected_piece_position = self.__board.piece_picked_up(self.__colour_to_move)
    
    def select_piece_in_puzzle(self): # allows the user to select a piece in a puzzle
        self.__colour_to_move = "w" if self.__colour_to_move == "b" else "b"
        self.__board.all_legal_moves(self.__colour_to_move)
        self.__selected_piece_position = self.__board.piece_picked_up(self.__colour_to_move)

    def move_piece(self, end_position, selected_piece_position): # valiades the moves made by the user
        if 0 <= selected_piece_position < 64:
            if 0 <= end_position[0] < 8 and 0 <= end_position[1] < 8:
                position = end_position[0] * 8 + end_position[1]
                if self.__board.validate_user_move((selected_piece_position, position)):
                    self.__board.move((selected_piece_position, position))
                    piece = self.__board.return_piece(position)
                    self.__board.update_piece_rect(piece, position)
                    self.__board.convert_move_log_to_notation()
                    self.__board.update_rects()
                    return True
        return False

    def update_piece_rect_if_needed(self, selected_piece_position): #updates the position of the pieces on the board
        if selected_piece_position != 100:
            piece = self.__board.return_piece(selected_piece_position)
            if piece is not None:
                self.__board.update_piece_rect(piece, selected_piece_position)

    def piece_moved(self):
        end_position = self.__board.convert_mouse_end_position_to_piece_position()
        moved = self.move_piece(end_position, self.__selected_piece_position)
        if not moved:
            self.update_piece_rect_if_needed(self.__selected_piece_position)
        return moved

    def puzzle_piece_moved(self, move): # checks if the move made by the user is the same the correct move held in database
        end_position_coord = self.__board.convert_mouse_end_position_to_piece_position()
        if self.__selected_piece_position == move[0]:
            end_position = end_position_coord[0] * 8 + end_position_coord[1]
            if end_position == move[1]:
                moved = self.move_piece(end_position_coord, self.__selected_piece_position)
                self.update_piece_rect_if_needed(self.__selected_piece_position)
                return moved
        self.update_piece_rect_if_needed(self.__selected_piece_position)
        self.__colour_to_move = "w" if self.__colour_to_move == "b" else "b"
        return False
    
    def undo_move(self):
        self.__board.undo_move()
        self.__board.update_rects()
        self.__board.undo_move_record()

    def change_colour_to_move(self,colour):
        self.__colour_to_move = colour

    def AI_move(self): # allows the AI to move
        if self.__AI != None:
            
            if self.__board.return_move_log().length()%2 == 0:
                colour_to_move = "w"
            else:
                colour_to_move = "b"
            self.__colour_to_move = colour_to_move
            if colour_to_move == self.__player2_colour:
                if self.__player2_colour == "w":
                    maximising_player = True
                else:   
                    maximising_player = False
                self.__board.check_if_end_game()
                self.__AI.update_board(self.__board)
                best_move,evaluation = self.__AI.iterative_deepening(maximising_player)
                if best_move == None:
                    return
                start_position = best_move[0]
                end_position = best_move[1]
                self.non_player_move(start_position,end_position)

    def non_player_move(self, start_position, end_position): # used for Puzzles/AI to move the opposition pieces
        self.__board.all_legal_moves(self.__colour_to_move)
        self.__board.move((start_position,end_position))
        self.__board.convert_move_log_to_notation()
        self.__board.update_rects()
        self.__colour_to_move = "w" if self.__colour_to_move == "b" else "b"

    def cal_start_end_position(self,move):
        start_position = move[:2]
        end_position = move[2:4]
        start_position = self.__board.convert_puzzle_move_to_move(start_position)
        end_position = self.__board.convert_puzzle_move_to_move(end_position)
        return start_position,end_position
    
    def display_chess(self,dragging):
        self.__board.display_board(self.__screen)
        if 0 <=self.__selected_piece_position < 64:
            if dragging == True:
                self.__board.displaying_possible_moves(self.__screen,self.__selected_piece_position)
        self.__board.display_pieces(self.__screen)

    def get_move_record(self):
        return(self.__board.return_move_record())
    
    def get_move_log(self):
        return(self.__board.return_move_log())
    
    def get_result(self):
        move_record = self.__board.return_move_record()
        if move_record.length() > 0:
            last_move = move_record.peek()
            if "++" in last_move:
                if move_record.peek() % 2 == 0 and self.__player1_colour == "w":
                    return "L"
                elif move_record.peek() % 2 == 1 and self.__player1_colour == "b":
                    return "L"
                else:
                    return "W"
            elif self.__board.check_if_stalemate() or self.__board.check_if_draw_by_repetition():
                return "D"
        return "U"
    
    def playingAI(self):
        if self.__AI != None:
            return True
        else:
            return False
    
    def return_move_record_as_string(self):
        move_record = self.__board.return_move_record()
        move_record_string = ""
        temp_stack = Stack()
        while not move_record.is_empty(): # pop items from stack and push them onto a temporary stack
            item = move_record.pop()
            temp_stack.push(item)
        while not temp_stack.is_empty(): # pop items from temporary stack and push them back onto the original stack and add them to a string
            move_record_string += str(temp_stack.peek()) + ", "
            move_record.push(temp_stack.pop())

        move_record_string = move_record_string.rstrip(", ")
        return move_record_string
    def state_of_game(self):
        move_record = self.__board.return_move_record()
        if move_record.length() > 0:
            last_move = move_record.peek()
            if "++" in last_move:
                return "Checkmate"
            elif "+" in last_move:
                return "Check"
            else:
                if self.__board.check_if_stalemate():
                    return "Stalemate"
                elif self.__board.check_if_draw_by_repetition():
                    return "Draw by repetition"        
        return ""