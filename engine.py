from time import time

class Engine():
    def __init__(self,board,AI_colour,max_depth):
        self.__board = board
        self.__AI_colour = AI_colour
        self.__max_depth = max_depth
        self.__current_best_move = None

    def update_board(self,board):
        self.__board = board
    def Minimax(self,depth,maximising_player,alpha,beta): # + using alpha beta pruning
        moves = []
        if depth == 0: # check if max depth
            return None,self.evaluate_position()
        colour = "w" if maximising_player else "b"
        self.__board.all_legal_moves(colour)
        moves = self.__board.return_moves()
        if len(moves) ==0: # check if game is over
            op_colour = "w" if colour == "b" else "b"
            m = list(self.__board.all_possible_moves(op_colour))
            if self.__board.is_checkmate(colour,m):
                evaluation = -10000 if colour == "w" else 10000
            else:
                evaluation = 0
            return None,evaluation
        if self.__board.check_if_draw_by_repetition():
            return None,0
        moves = self.order_moves(moves)
        if self.__search_depth == self.__max_depth and self.__search_depth == depth: # ensures that the previous depth search best move is searched first
            if self.__current_best_move in moves:
                moves.remove(self.__current_best_move)
                moves.insert(0, self.__current_best_move)
        if maximising_player: # maximising player wants a more position evaluation
            max_evaluation = -100000
            for move in moves:
                self.__board.move(move)
                evaluation = self.Minimax(depth-1,False,alpha,beta) # recusively calls the Minimax function - reducing the depth
                self.__board.undo_move()
                if evaluation[1] > max_evaluation:
                    max_evaluation = evaluation[1]
                    best_move = move
                alpha = max(alpha,max_evaluation)
                if beta <= alpha: #pruning worse branches
                    break
            return best_move,max_evaluation
        else: # maximising player wants a more negative evaluation
            min_evaluation = 100000
            for move in moves:
                self.__board.move(move)
                evaluation = self.Minimax(depth-1,True,alpha,beta)
                self.__board.undo_move()
                if evaluation[1] < min_evaluation:
                    min_evaluation = evaluation[1]
                    best_move = move
                beta = min(beta,min_evaluation)
                if beta <= alpha:
                    break
            return best_move,min_evaluation
        
    def iterative_deepening(self,maximising_player): # Optimisation - Iteratively calls Minimax - increasing the depth https://www.chessprogramming.org/Iterative_Deepening
        self.__current_best_move = None
        start_time = time()
        self.__search_depth = 0
        while True:
            self.__current_best_move, self.__current_best_eval = self.Minimax(self.__search_depth, maximising_player, -1000000, 1000000)
            if self.__search_depth == self.__max_depth or time() - start_time > 10: # if time to make move exceeds limits/max depth reached then stop
                break
            self.__search_depth += 1
        return self.__current_best_move, self.__current_best_eval

    def order_moves(self, moves): # shallow evaluation to order the moves
        move_predictions = sorted(
            ((move, (self.__board.return_piece(move[1]).return_value()-self.__board.return_piece(move[0]).return_value())  if self.__board.return_piece(move[1]) is not None else 0) for move in moves),
            key=lambda x: x[1],
            reverse=True
        ) # orders move by the difference between the taken piece and piece taking it
        ordered_moves = [move for move, prediction in move_predictions]
        return ordered_moves   

    def evaluate_position(self): # checks number of pieces and their position on the board
        evaluation = 0
        pos = self.__board.return_all_colour_pieces_positions("w")
        for i in pos:
            piece= self.__board.return_piece(i)
            evaluation += piece.return_value()
            evaluation += piece.return_piece_square_table(i)
        pos = self.__board.return_all_colour_pieces_positions("b")
        for i in pos:
            piece= self.__board.return_piece(i)
            evaluation -= piece.return_value()
            evaluation -= piece.return_piece_square_table(63-i)
        if self.__board.is_end_game():
            evaluation += self.end_game_evaluation()
        return evaluation
    
    def end_game_evaluation(self): # Encourages the king to move towards each other
        w_king_position = self.__board.return_king_position("w")
        b_king_position = self.__board.return_king_position("b")
        king_distance = self.manhattan_distance(w_king_position, b_king_position)
        if self.__AI_colour == "w":
            return 4 * (14- king_distance) # tested with 4 and it works the best
        else:
            return -4 * (14 - king_distance)
        
    def manhattan_distance(self,position1,position2): # Calculates the distance between two positions on the board
        x1,y1 = position1//8,position1%8
        x2,y2 = position2//8,position2%8
        return abs(x1-x2) + abs(y1-y2)
    