import pygame
from piece import *
from mouse import Mouse
from stack import Stack
N,E,S,W = -8,1,8,-1
class Board():
    def __init__(self,board_size,mouse):
        self.__square_size = int(board_size/8)
        self.__boardcolour1 = (240,217,181)#(180,175,165)#(218,168,88) #(232,235,239) #(118,150,86)
        self.__boardcolour2 = (181,136,99)#(145,140,125)#(129,79,48)#(125,135,150)	#(238,238,210) 
        self.__boardcolour3 = (205,92,92)  #(235,64,52) # highlights legal moves
        self.__boardcolour4 = (205,210,106) # highlights preview move
        self.__boardcolour5 = (170,162,58)
        self.__board = dict()
        self.__mouse = mouse
        self.__position_black_king = None
        self.__position_white_king = None
        self.__move_log = Stack()
        self.__columns_to_files = {0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
        self.__rows_to_rank = {0:"8",1:"7",2:"6",3:"5",4:"4",5:"3",6:"2",7:"1"}
        self.__move_record = Stack()
        self.__castling_rights = []
        self.__en_passant = Stack()
        self.__legal_moves = []
        self.__perspective = "w"
        self.__piece_classes = {'p': Pawn, 'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King}
        self.__pieces_moves = {"R":[N,E,S,W],
                               "B":[N+E,S+E,S+W,N+W],
                               "Q":[N,E,S,W,N+E,S+E,S+W,N+W],
                               "K":[N,E,S,W,N+E,S+E,S+W,N+W],
                               "p":[N,N+E,N+W],
                               "N":[E+N+N,N+E+E,S+E+E,S+S+E,S+S+W,S+W+W,N+W+W,N+N+W]}
        self.__pieces_moves_types = {"R":[[N],[E],[S],[W]],
                               "B":[[N,E],[S,E],[S,W],[N,W]],
                               "Q":[[N],[E],[S],[W],[N,E],[S,E],[S,W],[N,W]],
                               "K":[[N],[E],[S],[W],[N,E],[S,E],[S,W],[N,W]],
                               "p":[[N],[N,E],[N,W]],
                               "N":[[E,N,N],[N,E,E],[S,E,E],[S,S,E],[S,S,W],[S,W,W],[N,W,W],[N,N,W]]}
        self.__white_pieces = []
        self.__black_pieces = []
        self.__pieces = {"w":self.__white_pieces,"b":self.__black_pieces}
        self.__end_game = False

    def rotate_board(self): # switches all the variables so that the white/black pieces can be on either side of board
        self.__board = {63-i:self.__board[i] for i in range(len(self.__board))}
        self.__perspective = "b"
        temp_move_log = Stack()
        temp_move_record = Stack()
        temp_en_passant = Stack()
        while not self.__move_log.is_empty(): # pop items off the stack, modify them, and push them onto the temporary stack
            i, j, s, t = self.__move_log.pop()
            temp_move_log.push((63-i, 63-j, s, t))
            i, j = self.__move_record.pop()
            temp_move_record.push((63-i, 63-j))
            i = self.__en_passant.pop()
            if i != None:
                i = 63-i
            temp_en_passant.push(i)
        while not temp_move_log.is_empty(): # pop items off the temporary stack and push them back onto the original stack
            self.__move_log.push(temp_move_log.pop())
            self.__move_record.push(temp_move_record.pop())
            self.__en_passant.push(temp_en_passant.pop())
        self.__legal_moves = [(63-i,63-j) for i,j in self.__legal_moves]
        self.__mouse.update_selected_piece(None)
        self.__white_pieces = [63-i for i in self.__white_pieces]
        self.__black_pieces = [63-i for i in self.__black_pieces]
        self.__position_white_king = 63-self.__position_white_king
        self.__position_black_king = 63-self.__position_black_king
        self.__pieces = {"w":self.__white_pieces,"b":self.__black_pieces}
        for piece in self.__pieces["w"]:
            self.__board[piece].rotate_piece_square_table()
        for piece in self.__pieces["b"]:
            self.__board[piece].rotate_piece_square_table()
        self.__columns_to_files = {i: chr(104 - i) for i in range(8)}
        self.__rows_to_rank = {i: str(i + 1) for i in range(8)}
        self.update_rects()

    def create_board_set_up(self,perspective,fen): # Algorithm to Interpret FEN string
        self.__perspective = perspective
        square = 0
        wr_pos = []
        br_pos = []
        for character in fen:
            if character == " ":
                index = fen.index(character)
                index += 1
                break
            if character == "/":
                pass
            elif character.isdigit():
                for i in range(int(character)):
                    self.__board[square] = None
                    square += 1
            else:
                if character.isupper():
                    colour = "w"
                    self.__white_pieces.append(square)
                else:
                    colour = "b"
                    self.__black_pieces.append(square)
                    
                if character == "p" or character == "P":
                    piece_class = self.__piece_classes.get(character.lower())
                else:
                    piece_class = self.__piece_classes.get(character.upper())
                if character == "K":
                    self.__position_white_king = square
                if character == "k":
                    self.__position_black_king = square
                if piece_class:
                    row = square // 8
                    column = square %8
                    self.__board[square] = piece_class(colour,(column * self.__square_size, row * self.__square_size),self.__square_size)
                    if character == "R":
                        wr_pos.append(square)
                    if character == "r":
                        br_pos.append(square)
                square += 1
        index += 2
        if fen[index] == "-": # this character in the fen string represents the castling rights
            for i in wr_pos:
                self.__board[i].add_move_made()
            for i in br_pos:
                self.__board[i].add_move_made()
        else:
            s = index
            while True:
                if fen[index] == " ":
                    break
                index +=1
            c_rights = set(fen[s:index])
            p_rights = set("KQkq")
            self.__castling_rights = list(p_rights.intersection(c_rights))
                    
        if fen[index] == "-": # this character in the fen string represents the possible en passant square
            self.__en_passant.push(None)
        else:
            column = next((k for k, v in self.__columns_to_files.items() if v == fen[index]),None)
            row = next((k for k, v in self.__rows_to_rank.items() if v == fen[index+1]),None)
            sq = None
            if column != None:
                sq = (8*row +column)
            self.__en_passant.push(sq)
        if self.__perspective == "b":
            self.rotate_board()

    def display_board(self,screen):
        for i in range(len(self.__board)):
            row = i // 8
            column = i % 8
            rect=(column *self.__square_size,row*self.__square_size,self.__square_size,self.__square_size)
            if (column+row)%2 == 0: # test whether the square is a light/dark square
                pygame.draw.rect(screen,self.__boardcolour1,rect)
            else:
                pygame.draw.rect(screen,self.__boardcolour2,rect)
                
        if self.__move_log.length() > 0:
            for i in range(2): # show the previous move made
                start_row = self.__move_log.peek()[i]//8
                start_column = self.__move_log.peek()[i]%8
                rect=(start_column *self.__square_size,start_row*self.__square_size,self.__square_size,self.__square_size)
                if (start_column+start_row)%2 == 0:
                    pygame.draw.rect(screen,self.__boardcolour4,rect)
                else:
                    pygame.draw.rect(screen,self.__boardcolour5,rect)

    def display_pieces(self,screen):
        selected_piece = self.__mouse.return_selected_piece()
        for i in self.__white_pieces:
            piece = self.__board[i]
            if selected_piece != piece:
                piece.display_piece(screen) 
        for i in self.__black_pieces:
            piece = self.__board[i]
            if selected_piece != piece:
                piece.display_piece(screen)
        if selected_piece != None:
            selected_piece.display_piece(screen)

    def piece_picked_up(self,colour_to_move):
        x_prev,y_prev = self.__mouse.return_initial_position()
        prev_column = x_prev// self.__square_size
        prev_row = y_prev// self.__square_size
        if 0 <= prev_row <8 and 0 <= prev_column <8:
            square = prev_row * 8 +prev_column
            piece = self.__board[square]
            if piece != None:
                if piece.return_colour() == colour_to_move:
                    self.__mouse.update_selected_piece(piece)
                    return square
        return 100

    def convert_mouse_end_position_to_piece_position(self):
        x_new,y_new = self.__mouse.return_final_position()
        new_column = x_new// self.__square_size
        new_row = y_new//self.__square_size
        return (new_row,new_column)
    
    def update_piece_rect(self,piece,piece_position):
        row = piece_position // 8
        column = piece_position % 8
        rect =  (column*self.__square_size,row*self.__square_size)
        piece.update_rect(rect)

    def update_board(self,piece,piece_position,end_position):
        self.__board[piece_position] = None
        self.__board[end_position] = piece
        colour = piece.return_colour()
        if end_position != piece_position:
            self.__pieces[colour].remove(piece_position)
            self.__pieces[colour].append(end_position)
        elif piece_position == end_position:
            self.__pieces[colour].append(end_position)

    def move(self,move):
        piece_position = move[0]
        end_position = move[1]
        special_case = ""
        en_passant = None
        taken_piece = None
        piece = self.__board[piece_position]
        colour = piece.return_colour()
        op_colour = "w" if colour == "b" else "b"
        piece.add_move_made()
        if self.__board[end_position] != None:
            taken_piece = self.__board[end_position]
            special_case = "t"
            self.__pieces[op_colour].remove(end_position)
        self.update_board(piece,piece_position,end_position)
    
        if piece.return_name() == "King":
            self.update_king_position(colour,end_position)
            if self.__perspective == "w":
                if abs(piece_position - end_position) == 2:
                    if end_position > piece_position:
                        self.update_board(self.__board[end_position+1],end_position+1,end_position-1)
                        special_case = "k"
                    else:
                        self.update_board(self.__board[end_position-2],end_position-2,end_position+1)
                        special_case = "q"
                        
            if self.__perspective == "b":
                if abs(piece_position - end_position) == 2:
                    if end_position < piece_position:
                        self.update_board(self.__board[end_position-1],end_position-1,end_position+1)
                        special_case = "k"
                    else:
                        self.update_board(self.__board[end_position+2],end_position+2,end_position-1)
                        special_case = "q"

        elif piece.return_name() == "Pawn":
            if end_position == self.__en_passant.peek():
                if colour != self.__perspective:
                    t_square = end_position + N
                else:
                    t_square = end_position-N
                taken_piece = self.__board[t_square]
                self.__board[t_square] = None
                self.__pieces[op_colour].remove(t_square)
                special_case = "e"
            elif abs(piece_position - end_position) == S+S:
                if colour == self.__perspective:
                    en_passant = end_position - N
                else:
                    en_passant = end_position + N
            elif end_position // 8 == 0 or end_position // 8 == 7:
                promotion = "Q"
                if promotion in self.__piece_classes:
                    new = self.__piece_classes[promotion]
                    rect = piece.return_rect()
                    self.__board[end_position] = new(colour,rect,self.__square_size)
                temp = special_case
                special_case = temp +"p"+ promotion
        self.__en_passant.push(en_passant)
        self.__move_log.push([piece_position,end_position,special_case,taken_piece])
    
    def handling_castling(self,start_square,end_square,colour):
        c_castling_rights = []
        if colour == "w":
            castle = [c for c in self.__castling_rights if c in ("K","Q")]
            if self.__perspective == "w":
                k = 60
                offset = 1
            else:
                k = 3
                offset = -1
        elif colour == "b":
            castle = [c for c in self.__castling_rights if c in ("k","q")]
            if self.__perspective == "w":
                k = 4
                offset = 1
            else:
                k = 59
                offset = -1
        if start_square != k or len(castle) == 0:
            return c_castling_rights
        for i in castle:
            if i.upper() == "K" and end_square == k+2*offset:
                if self.__board[k+2*offset] == None and self.__board[k+3*offset] != None:
                    if self.__board[k+3*offset].return_algebraic() == "R" and self.__board[k+3*offset].return_number_of_moves() == 0: #check if rook has moved
                        c_castling_rights.append((k,k+2*offset))
            if i.upper() == "Q" and end_square == k-2*offset:
                if self.__board[k-2*offset] == None and self.__board[k-3*offset] == None and self.__board[k-4*offset] != None:
                    if self.__board[k-4*offset].return_algebraic() == "R" and self.__board[k-4*offset].return_number_of_moves() == 0:
                        c_castling_rights.append((k,k-2*offset))
        return c_castling_rights
            

        
    def all_possible_moves(self,colour):
        if self.__perspective == colour:  
            ub,lb = 7,0
            m = 1
        else:
            ub,lb = 0,7
            m = -1

        for start_position in self.__pieces[colour]:
            piece = self.__board[start_position]
            algebraic = piece.return_algebraic()
            moves = self.__pieces_moves[algebraic]
            moves_types = self.__pieces_moves_types[algebraic]
            for move,move_type in zip(moves, moves_types):# iterates through the pieces moves - uses move_type to check the the move contains certain direction
                end_position = start_position +m* move
                if 0 <= end_position <= 63:
                    target_piece = self.__board[end_position]
                    if algebraic == "p":
                        row = start_position // 8
                        if move == N and target_piece == None:
                            yield (start_position, end_position)

                            end_position += m*move
                            if ((row == 6 and colour == self.__perspective) or (row == 1 and colour != self.__perspective)) and self.__board[end_position] == None:
                                yield (start_position, end_position)

                        elif target_piece != None and target_piece.return_colour() != colour:
                            column = start_position % 8
                            if E in move_type and ((column < 7 and m== 1) or (0 < column and m == -1)):
                                yield (start_position, end_position)

                            elif W in move_type and ((0 < column and m == 1) or (column < 7 and m == -1)):
                                yield (start_position, end_position)

                        elif end_position == self.__en_passant.peek():
                            column = start_position % 8
                            if E in move_type and (( column < 7 and m == 1) or (0 < column and m == -1)):
                                yield (start_position, end_position)
                                
                            elif W in move_type and ((0 < column and m == 1) or (column < 7 and m == -1)):
                                yield (start_position, end_position)
                        continue
                    check = start_position
                    while True: # check legal moves for sliding pieces
                        if (check //8 == lb and N in move_type) or (check //8 == ub and S in move_type) or (check %8 == lb and W in move_type) or (check %8 == ub and E in move_type):
                            break                 
                        if not(0 <= end_position <= 63):
                            break
                        target_piece = self.__board[end_position]
                        if algebraic == "N":
                            if (check //8 == lb+m and move_type.count(N) == 2) or (check %8 == ub-m and move_type.count(E) == 2) or (check %8 == lb +m and move_type.count(W) == 2) or (check //8 == ub -m and move_type.count(S) == 2):
                                break
                            elif target_piece == None:
                                yield (start_position, end_position)
                            elif target_piece.return_colour() != colour:
                                yield (start_position, end_position)
                            break

                        if target_piece == None:
                            yield (start_position, end_position)
                            if algebraic == "K":
                                break
                            check = end_position
                            end_position += m*move 
                        else:
                            if target_piece.return_colour() != colour:
                                yield (start_position, end_position)
                            break

    def all_legal_moves(self, colour): # converts pseudo-legal moves to legal moves
        self.__legal_moves = []
        all_moves = set(self.all_possible_moves(colour))
        op_colour = "w" if colour == "b" else "b"
        for move in all_moves:
            self.move(move)
            king_position = self.return_king_position(colour)
            all_op_moves =set(t[1] for t in set(self.all_possible_moves(op_colour)))
            if king_position not in all_op_moves: # sees if the opponent can take the king in the next move if they can then it is not a legal move
                self.__legal_moves.append(move)
                if king_position == move[1] and abs(move[0] - move[1]) == 1 and self.__move_log.peek()[2] == "":
                    if move[0] not in all_op_moves and (2 * move[1] - move[0]) not in all_op_moves and self.__board[king_position].return_number_of_moves() == 1:
                        if self.handling_castling(move[0], 2 * move[1] - move[0], colour):
                            self.__legal_moves.append((move[0], 2 * move[1] - move[0]))
            self.undo_move()
        return self.__legal_moves
    
    def is_check(self,colour):
        if colour == "w":
            op_colour = "b"
            king_pos = self.__position_white_king
        else:
            op_colour = "w"
            king_pos = self.__position_black_king
        op_moves = set(self.all_possible_moves(op_colour))
        op_moves_end = set(t[1] for t in op_moves)
        if king_pos in op_moves_end:
            return True , op_moves
        else:
            return False , op_moves
        
    def is_checkmate(self,colour,op_moves):
        if colour == "w":
            king_pos = self.__position_white_king
        else:
            king_pos = self.__position_black_king
        op_moves_end = set(t[1] for t in op_moves)
        if king_pos in op_moves_end:
            return True
        else:
            return False
        
    def return_all_colour_pieces_positions(self,colour):
        return self.__pieces[colour]
    
    def return_piece(self,position):
        return self.__board[position]
    
    def displaying_possible_moves(self, screen, piece_position):
        p_moves = [t for t in self.__legal_moves if t[0] == piece_position]
        if len(p_moves) > 0: 
            for i in range(len(p_moves)):
                square = p_moves[i][1]
                row = square // 8
                column = square % 8
                rect = (column * self.__square_size, row * self.__square_size, self.__square_size, self.__square_size)
                pygame.draw.rect(screen, self.__boardcolour3, rect)

    def update_king_position(self,colour,position):
        if colour == "b":
            self.__position_black_king = position
        else:
            self.__position_white_king = position

    def return_king_position(self,colour):
        if colour == "b":
            return self.__position_black_king
        elif colour == "w":
            return self.__position_white_king

    def undo_move(self): # undoes the move / maintains castling rights, en passant etc
        if self.__move_log.length() == 0:
            return
        move = self.__move_log.pop()
        piece = self.__board[move[1]]
        piece.remove_move_made()
        colour = piece.return_colour()
        t_piece = move[3]
        self.update_board(piece,move[1],move[0])
        if piece.return_algebraic() == "K":
            self.update_king_position(colour,move[0])
        if move[2] != "":
            if move[2] in "t":
                self.update_board(move[3],move[1],move[1])
            elif move[2] == "e":

                if colour != self.__perspective:
                    t_square = move[1] + N
                else:
                    t_square =move[1]-N
                self.update_board(move[3],t_square,t_square)
            elif "p" in move[2] :
                self.__pieces[colour].remove(move[0])
                self.update_board(Pawn(colour,piece.return_rect(),self.__square_size),move[0],move[0])
                
                if t_piece != None:
                    self.update_board(t_piece,move[1],move[1])
            elif move[2] in "kq":
                if self.__perspective == "w":
                    if move[1] > move[0]:
                        self.update_board(self.__board[move[1]-1],move[1]-1,move[1]+1)
                    else:
                        self.update_board(self.__board[move[1]+1],move[1]+1,move[1]-2)
                if self.__perspective == "b":
                    if move[1] < move[0]:
                        self.update_board(self.__board[move[1]+1],move[1]+1,move[1]-1)
                    else:
                        self.update_board(self.__board[move[1]-1],move[1]-1,move[1]+2)
        self.__en_passant.pop()

    def update_rects(self):
        for i in range(len(self.__board)):
            piece = self.__board[i]
            if piece != None:
                self.update_piece_rect(piece,i)

    def validate_user_move(self,move):
        if move in self.__legal_moves:
            return True
        else:
            return False

    def convert_move_log_to_notation(self): # Algorithms used to convert move made into chess notation
        move = self.__move_log.peek()
        prev_file = self.__columns_to_files[move[0]%8]
        notation_x = self.__columns_to_files[move[1]%8]
        notation_y = self.__rows_to_rank[move[1]//8]
        piece = self.return_piece(move[1])
        notation = ""
        if move[2] != "":
            if move[2][0] == "t" or move[2] == "e": # t = taken, e = en passant, q = queen side castling, k = king side castling
                if piece.return_algebraic() == "p" or "p" in move[2]:
                    notation = (prev_file + "x"+ notation_x + notation_y)  
                else:
                    notation = (piece.return_algebraic() + "x" + notation_x + notation_y)
            if move[2] == "q":
                notation = ("O-O-O")
            if move[2] == "k":
                notation = ("O-O")
            if "p" in move[2]:
                if len(notation) == 0:
                    notation = notation_x + notation_y
                temp = notation
                notation = temp + move[2][move[2].index("p") +1 ]
        else:
            if piece.return_algebraic() == "p":
                notation = (notation_x + notation_y) 
            else:
                notation = (piece.return_algebraic() + notation_x + notation_y)
        if self.__move_log.length()%2 == 0:
            opposite_colour = "w"
        else:
            opposite_colour = "b"
        check, moves = self.is_check(opposite_colour)
        if check:
            notation = notation + "+"
        self.all_legal_moves(opposite_colour)
        if len(self.__legal_moves) == 0:
            if self.is_checkmate(opposite_colour,moves):
                notation = notation + "+"
        self.__move_record.push(notation)

    def check_if_stalemate(self):
        if len(self.__legal_moves) == 0:
            return True

    def check_if_draw_by_repetition(self): # checks if the same position has been repeated 3 times
        if self.__move_log.length() > 6:
            last_six_move_logs = []
            for i in range(6):
                last_six_move_logs.append(self.__move_log.pop())
            last_six_moves = [(t[0], t[1]) for t in last_six_move_logs]
            reverse_direction = [(b,a) for a,b in last_six_moves[2:4]] 
            repeated = last_six_moves[0:2] == reverse_direction == last_six_moves[4:6]
            for move in reversed(last_six_move_logs):
                self.__move_log.push(move)
            return repeated
        return False

    def check_if_end_game(self): # if end game change evaluation method
        self.__end_game = False
        count = 0
        for pos in self.__pieces["w"]:
            if self.__board[pos].return_algebraic() not in ["K","p"]:
                count += 1
        if count <=3:
            self.__board[self.__position_white_king].set_piece_square_table_end_game()
            self.__end_game = True
        else:
            self.__board[self.__position_white_king].set_piece_square_table()
        count = 0
        for pos in self.__pieces["b"]:
            if  self.__board[pos].return_algebraic() not in ["K","p"]:
                count += 1
        if count <=3:
            self.__board[self.__position_black_king].set_piece_square_table_end_game()
            self.__end_game = True
        else:
            self.__board[self.__position_black_king].set_piece_square_table()

    def convert_puzzle_move_to_move(self,move):
        for key, value in self.__columns_to_files.items():
            if move[0] == value:
                column = key
                break
        for key, value in self.__rows_to_rank.items():
            if move[1] == value:
                row = key
                break
        return (row*8 + column)

    def is_end_game(self):
        return self.__end_game

    def return_move_record(self):
        return self.__move_record

    def return_move_log(self):
        return self.__move_log

    def return_moves(self):
        return self.__legal_moves

    def undo_move_record(self):
        if self.__move_record.length() > 0:
            self.__move_record.pop()