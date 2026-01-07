import pygame
from chess import Chess
from mouse import Mouse
import pygame_menu 
from chessclient import ChessClient
import random
import bcrypt

pygame.init()
class Main():
    def __init__(self):
        self.__mouse = Mouse()
        self.__screen_width = 1200
        self.__screen_height = 600
        self.__screen = pygame.display.set_mode((self.__screen_width,self.__screen_height)) # displaying the screen with the dimensions
        self.__running = True
        self.__dragging = False
        self.__board_dimension = self.__screen_height if self.__screen_width > self.__screen_height else self.__screen_width
        self.__screen_to_show= "Start"
        self.__AI_diff = -1
        self.__player1_colour = "w"
        self.__mode = "PvP"
        self.__fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.__user = 0
        self.__base_menu = "Start"
        self.__chess = Chess(self.__screen,self.__mouse,self.__board_dimension)
        self.__menus = {"Start" : pygame_menu.Menu("Start",self.__screen_width,self.__screen_height,theme=pygame_menu.themes.THEME_BLUE),
                        "Register": pygame_menu.Menu("Register",self.__screen_width,self.__screen_height,theme=pygame_menu.themes.THEME_BLUE),
                        "Main Menu" : pygame_menu.Menu("Main Menu",self.__screen_width,self.__screen_height,theme=pygame_menu.themes.THEME_BLUE),
                        "Login" : pygame_menu.Menu("Login",self.__screen_width,self.__screen_height,theme=pygame_menu.themes.THEME_BLUE),
                        "Puzzle Selector" : pygame_menu.Menu("Puzzle Selector",self.__screen_width,self.__screen_height,theme=pygame_menu.themes.THEME_BLUE),
                        "Difficulty" : pygame_menu.Menu("Difficulty",self.__screen_width,self.__screen_height,theme=pygame_menu.themes.THEME_BLUE),
                        "Game" : pygame_menu.Menu("Game",self.__screen_width - self.__board_dimension,self.__screen_height,theme=pygame_menu.themes.THEME_BLUE),
                        "Game Selector" : pygame_menu.Menu("Game Selector",self.__screen_width,self.__screen_height,theme=pygame_menu.themes.THEME_BLUE),
                        "Puzzles" : pygame_menu.Menu("Puzzles",self.__screen_width - self.__board_dimension,self.__screen_height,theme=pygame_menu.themes.THEME_BLUE),
                        "Filter" : pygame_menu.Menu("Filter",self.__screen_width,self.__screen_height,theme=pygame_menu.themes.THEME_BLUE),
                        "Game Review" : pygame_menu.Menu("Game Review",self.__screen_width - self.__board_dimension,self.__screen_height,theme=pygame_menu.themes.THEME_BLUE)}

    def GameLoop(self): # the infinite loop where window is run from
        self.create_menus()
        set_up = False
        while self.__running==True:
            if self.__screen_to_show not in ["Game","Puzzles","Game Review"]:
                set_up = False
                self.__menus[self.__screen_to_show].mainloop(self.__screen)
            else:
                if set_up==False: # setting up the board for the game
                    self.__menus[self.__screen_to_show].enable()
                    if self.__screen_to_show == "Game" or self.__screen_to_show == "Game Review":
                        self.__fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
                    elif self.__screen_to_show == "Puzzles":
                        self.__menus[self.__screen_to_show].get_widget("accuracy").set_title("")
                        self.__menus[self.__screen_to_show].get_widget("rating").set_title("Rating: " + str(self.__puzzle[3]) )
                        number_of_puzzle_moves = 0
                        if "w" in self.__fen:
                            self.__player1_colour = "b"
                        else:
                            self.__player1_colour = "w"
                    self.__chess = Chess(self.__screen,self.__mouse,self.__board_dimension)
                    self.__chess.set_up_playing_condition(self.__player1_colour,self.__AI_diff,self.__mode,self.__fen)
                    self.update_move_record_label()
                    set_up = True

                if self.__screen_to_show == "Puzzles":
                    if number_of_puzzle_moves % 2 == 0:
                        puzzle_moves = self.__puzzle[2].split()

                        start_pos, end_pos = self.__chess.cal_start_end_position(puzzle_moves[number_of_puzzle_moves])
                        self.__chess.non_player_move(start_pos,end_pos)
                        number_of_puzzle_moves += 1
                self.__chess.display_chess(self.__dragging)
                                          
            events = pygame.event.get()
            if self.__menus[self.__screen_to_show].is_enabled():
                self.__menus[self.__screen_to_show].update(events)
                self.__menus[self.__screen_to_show].draw(self.__screen)
            for event in events:
                if event.type == pygame.QUIT:
                    self.__running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.__dragging = True
                    self.__mouse.update_initial_position()
                    if self.__screen_to_show == "Game":
                        self.__chess.select_piece()
                    elif self.__screen_to_show == "Puzzles":
                        self.__chess.select_piece_in_puzzle()

                if event.type == pygame.MOUSEMOTION and self.__dragging and (self.__screen_to_show == "Game" or self.__screen_to_show == "Puzzles"):
                    self.__mouse.drag(event.rel) ## allowing for dragging of pieces

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    
                    if self.__screen_to_show == "Game":
                        self.__dragging = False
                        self.__mouse.update_final_position()
                    
                        self.__chess.piece_moved()
                        self.__mouse.reset()
                        self.__chess.display_chess(self.__dragging)
                        self.update_move_record_label()

                        pygame.display.update()
                        self.__chess.AI_move()
                        self.update_move_record_label()
                        self.__chess.display_chess(self.__dragging)

                    elif self.__screen_to_show == "Puzzles":
                        self.__dragging = False
                        self.__mouse.update_final_position()
                        start_pos, end_pos = self.__chess.cal_start_end_position(puzzle_moves[number_of_puzzle_moves])
                        if self.__chess.puzzle_piece_moved((start_pos,end_pos)) == True:
                            number_of_puzzle_moves += 1
                            self.__menus[self.__screen_to_show].get_widget("accuracy").set_title("Correct")
                        else:
                            self.__menus[self.__screen_to_show].get_widget("accuracy").set_title("Try Again")
                        if number_of_puzzle_moves == len(puzzle_moves):
                            self.__chess.display_chess(self.__dragging)
                            pygame.display.update()
                            ChessClient.puzzle_completed(self.__user,self.__puzzle[0])
                            self.get_puzzle()
                            if len(self.__puzzle) >0:
                                set_up = False
                                self.__menus[self.__screen_to_show].get_widget("rating").set_title("Rating: " + str(self.__puzzle[3]) )
                                self.__menus[self.__screen_to_show].get_widget("accuracy").set_title("")
                        self.__mouse.reset()
            pygame.display.update()

    def update_screen(self,screen): # update menu to show
        if screen not in ["Game", "Puzzles","Game Review"]:
            self.__menus[self.__base_menu].enable()
            self.__menus[self.__base_menu]._open(self.__menus[screen])
            self.__menus["Game"].get_widget("Move Record").set_title("")
        else:
            self.__menus[self.__screen_to_show].disable()
            self.__menus[screen].enable()
        self.__screen_to_show = screen # previous menu determines what mode to play
        if self.__screen_to_show == "Puzzle Selector": 
            self.__mode = "Puzzles"
        elif self.__screen_to_show == "Difficulty":
            self.__mode = "AI"
        elif self.__screen_to_show =="Main Menu":
            self.__AI_diff = -1
            self.__mode = "PvP"
        elif self.__screen_to_show == "Game Selector":
            self.get_games_name()

    def create_menus(self): # creating the widgets for the menus
        self.__menus["Start"].add.label("A Chess Game",font_size=50,font_color=(0,0,0))
        self.__menus["Start"].add.button('Login', self.update_screen,"Login")
        self.__menus["Start"].add.button('Register', self.update_screen,"Register")

        self.__menus["Register"].add.text_input('Username :',textinput_id='username')
        self.__menus["Register"].add.text_input('Password :', password=True,textinput_id='password')
        self.__menus["Register"].add.label('', label_id="error")
        self.__menus["Register"].add.button('Submit', self.submit_login)

        self.__menus["Login"].add.text_input('Username :',textinput_id='username')
        self.__menus["Login"].add.text_input('Password :', password=True,textinput_id='password')
        self.__menus["Login"].add.label('', label_id="error")
        self.__menus["Login"].add.button('Submit', self.submit_login)

        self.__menus["Puzzles"].set_absolute_position(self.__board_dimension,0)
        self.__menus["Puzzles"].add.label("",label_id="rating")
        self.__menus["Puzzles"].add.label("",label_id="accuracy")
        self.__menus["Puzzles"].add.button('Back', self.update_screen, "Main Menu")
        
        self.__menus["Main Menu"].add.button('Play Against AI', self.update_screen,"Difficulty")
        self.__menus["Main Menu"].add.button('Play Against Human', self.update_screen,"Game")
        self.__menus["Main Menu"].add.button('Puzzles', self.update_screen,"Puzzle Selector")
        self.__menus["Main Menu"].add.button('Game Selector', self.update_screen,"Game Selector")
        self.__menus["Main Menu"].add.button('Quit', pygame_menu.events.EXIT)

        self.__menus["Filter"].add.dropselect('Colour You Played As:', [('Black', ("b")),('White',("w")),("Both",("w","b"))],dropselect_id="PlayedAs",default=2)
        self.__menus["Filter"].add.dropselect_multiple('Result:',[('Win', ("W")), ('Loss', ("L")),('Draw',("D")),("Undecided",("U"))],dropselect_multiple_id="Result",default=[0,1,2])
        self.__menus["Filter"].add.dropselect('Game Against:',[('AI', (1)), ('Human', (0)),('Both',(0,1))],dropselect_id="AI",default=2)
        self.__menus["Filter"].add.button('Set Filter', self.update_screen,"Game Selector")
        
        self.__menus["Game Selector"].add.dropselect('Games:',["TempValue"],selection_box_width = 800,dropselect_id="Game Selector")
        self.__menus["Game Selector"].add.button("Filter",self.update_screen,"Filter")
        self.__menus["Game Selector"].add.button('Load Game', self.load_game)
        self.__menus["Game Selector"].add.label("",label_id = "Error")
        
        self.__menus["Difficulty"].add.selector('Game Mode :', [('Easy', 2),('Intermediate',3),('Hard',4)],selector_id="Game Mode")
        self.__menus["Difficulty"].add.selector('Colour :', [("White", "w"), ('Black', "b"),('Random',"r")], selector_id= "Colour")
        self.__menus["Difficulty"].add.button('Play', self.settings_against_AI)

        self.__menus["Game"].set_absolute_position(self.__board_dimension,0)
        self.__menus["Game"].add.label("Move Log")
        self.__menus["Game"].add.label("",font_size = 15, wordwrap=True,label_id="Move Record")
        self.__menus["Game"].add.label("",label_id="Game State")
        self.__menus["Game"].add.button('Undo',self.undo_move)
        self.__menus["Game"].add.button('Back', self.update_screen, "Main Menu")
        self.__menus["Game"].add.text_input('Name :',textinput_id='Name')
        self.__menus["Game"].add.button('Save', self.save_game)
        self.__menus["Game"].add.label("",label_id="Error")

        self.__menus["Game Review"].set_absolute_position(self.__board_dimension,0)
        self.__menus["Game Review"].add.label("Move Log")
        self.__menus["Game Review"].add.label("",font_size = 15, wordwrap=True,label_id="Move Record")
        self.__menus["Game Review"].add.label("",label_id="Game State")
        self.__menus["Game Review"].add.button('Make Move',self.make_move)
        self.__menus["Game Review"].add.button('Undo Move',self.undo_move)
        self.__menus["Game Review"].add.label("Continue Playing Against:")
        self.__menus["Game Review"].add.selector('', [("No AI", 0), ('Easy', 2),('Intermediate',3),('Hard',4)], selector_id= "AI")
        self.__menus["Game Review"].add.button('Continue Game',self.continue_game)
        self.__menus["Game Review"].add.button('Back', self.update_screen, "Main Menu")

        self.__menus["Puzzle Selector"].add.range_slider("Rating",(0,2000),(0,2000),100, rangeslider_id= "Rating")
        self.__menus["Puzzle Selector"].add.label("",label_id = "Error")
        self.__menus["Puzzle Selector"].add.button('Play',self.get_puzzle)

    def get_games_name(self): # get game names from server
        input_data = self.__menus["Filter"].get_input_data()
        playedas = input_data['PlayedAs'][0][1]
        result = tuple(t[1] for t in input_data['Result'][0])
        AI = input_data['AI'][0][1]
        if result != ():
            self.__menus["Game Selector"].get_widget("Game Selector").update_items(ChessClient.get_games_name(self.__user,result,playedas,AI))
        else:
            self.__menus["Game Selector"].get_widget("Game Selector").update_items([])

    def settings_against_AI(self):
        input_data = self.__menus["Difficulty"].get_input_data()
        self.__AI_diff = input_data["Game Mode"][0][1]
        colour = input_data["Colour"][0][1]
        if colour == "r":
            colour = random.choice(["w","b"])
        self.__player1_colour = colour
        self.update_screen("Difficulty")
        self.update_screen("Game")

    def get_puzzle(self):
        input_data = self.__menus["Puzzle Selector"].get_input_data()
        rating = input_data['Rating']
        min_rating = round(rating[0])
        max_rating = round(rating[1])
        puzzle = ChessClient.get_puzzle(self.__user, min_rating,max_rating)
        if len(puzzle) > 0:
            self.__puzzle = puzzle[0]
            self.__fen = self.__puzzle[1]
            self.update_screen("Puzzle Selector")
            self.__menus["Puzzle Selector"].get_widget("Error").set_title("")
            self.update_screen("Puzzles")
        else:
            self.__puzzle = []
            self.update_screen("Main Menu")
            self.update_screen("Puzzle Selector")
            self.__menus["Puzzle Selector"].get_widget("Error").set_title("There are no puzzles within the selected range")

    def continue_game(self): # continue the game from position in game review
        input_data = self.__menus["Game Review"].get_input_data()
        AI = input_data["AI"][0][1]
        if AI != 0:
            self.__chess.add_engine(AI)
        self.update_screen("Game")


    def make_move(self): # used for the game review screen  - makes the move that was stored on the database
        move_to_make = self.__chess.get_move_record().length()
        if move_to_make < len(self.__moves):
            start_pos, end_pos = self.__moves[move_to_make].split(",")
            start_pos, end_pos = int(start_pos), int(end_pos)
            if move_to_make % 2 ==0:
                self.__chess.change_colour_to_move("w")
            else:
                self.__chess.change_colour_to_move("b")
            self.__chess.non_player_move(start_pos,end_pos)
            self.update_move_record_label()

    def undo_move(self):
        if self.__AI_diff != -1:
            self.__chess.undo_move()
        self.__chess.select_piece()
        self.__chess.undo_move()
        self.__chess.select_piece()
        
    def submit_login(self): # Registering/Logging In to account       
        if self.__screen_to_show == "Register":
            input_data = self.__menus["Register"].get_input_data()
            username = input_data["username"]
            password = input_data["password"]
            if len(password) < 8:
                self.__menus["Register"].get_widget("error").set_title("Password needs to be at least 8 characters long")
            else:
                count = 0
                for character in password:
                    if character in " !#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
                        count += 1
                if count == 0:
                    self.__menus["Register"].get_widget("error").set_title("Password needs to contain at least 1 special character")
                else: # producing the hash value for the password
                    salt = bcrypt.gensalt()
                    hashed_password = bcrypt.hashpw(password.encode("utf-8"),salt)
                    response = ChessClient.create_user(username,salt.decode("utf-8"),hashed_password.decode("utf-8")) #convert back to string and send to server
                    if response["error"] == "Username already exists":
                        self.__menus["Register"].get_widget("error").set_title("Username already exists")
                    else:
                        response = ChessClient.validate_user(username,hashed_password.decode("utf-8"))
                        self.__user = response[0][0]
                        self.__menus["Register"].get_widget("error").set_title("Inputted user details are valid")
                    
        elif self.__screen_to_show == "Login":

            input_data = self.__menus["Login"].get_input_data()
            username = input_data["username"]
            password = input_data["password"].encode("utf-8")
            response = ChessClient.get_salt(username)
            if not response:
                self.__menus["Login"].get_widget("error").set_title("Username does not exist")
            else: # checks if the hash values are the same
                salt = response[0][0].encode("utf-8")
                hashed_password = bcrypt.hashpw(password,salt)
                response = ChessClient.validate_user(username,hashed_password.decode("utf-8"))
                if not response:
                    self.__menus["Login"].get_widget("error").set_title("Incorrect Password")
                else:
                    self.__user = response[0][0]
                    self.__menus["Login"].get_widget("error").set_title("")
                    self.__menus[self.__base_menu].disable()
                    self.__base_menu = "Main Menu"
                    self.update_screen("Main Menu")
    
    def load_game(self):
        input_data = self.__menus["Game Selector"].get_input_data()
        if input_data != {}:
            gameID = input_data["Game Selector"][0][1]
            game = ChessClient.get_game_moves(gameID)[0]
            self.__player1_colour = game[2]
            self.__moves = game[0].split()
            self.__menus["Game Selector"].get_widget("Error").set_title("")
            self.update_screen("Game Review")
        else:
            self.__menus["Game Selector"].get_widget("Error").set_title("Select a Game")
            
    def save_game(self):
        move_log = self.__chess.get_move_log()
        moves = []
        while move_log.length() > 0:
            moves += [move_log.pop()]
        moves = list(reversed(moves)) # gets start square and end square for all moves in order
        list_of_moves = [(sublist[0], sublist[1]) for sublist in moves if len(sublist) >= 2] 
        list_of_moves_str = ' '.join([f'{x},{y}' for x, y in list_of_moves]) # store as a string so it can be stored in the database
        result = self.__chess.get_result()
        playedas = self.__player1_colour
        AI = self.__chess.playingAI()
        name = self.__menus["Game"].get_input_data()["Name"]
        all_user_games = ChessClient.get_games_name(self.__user, ("W","L","D","U"), ("w","b"), (0,1))
        all_user_game_names = [games[0] for games in all_user_games]
        if len(name) > 0 and name not in all_user_game_names:
            ChessClient.save_game(self.__user,name,list_of_moves_str,result,playedas,AI)
            self.__menus["Game"].get_widget("Error").set_title("")
            self.update_screen("Main Menu")
        else:
            self.__menus["Game"].get_widget("Error").set_title("Enter a valid name")

    def update_move_record_label(self):
        if self.__screen_to_show == "Game" or self.__screen_to_show == "Game Review":
            self.__menus[self.__screen_to_show].get_widget("Move Record").set_title(self.__chess.return_move_record_as_string())
            self.__menus[self.__screen_to_show].get_widget("Game State").set_title(self.__chess.state_of_game())

game1= Main()
game1.GameLoop()