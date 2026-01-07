import pygame

class Mouse():
    def __init__(self):
        self.__initial_position_x = 0
        self.__initial_position_y = 0
        self.__final_position_x = 0
        self.__final_position_y = 0
        self.__selected_piece = None
    def update_initial_position(self):
        self.__initial_position_x,self.__initial_position_y = pygame.mouse.get_pos()
    def return_initial_position(self):
        return self.__initial_position_x,self.__initial_position_y
    def update_final_position(self):
        self.__final_position_x,self.__final_position_y = pygame.mouse.get_pos()
    def return_final_position(self):
        return self.__final_position_x,self.__final_position_y
    def update_selected_piece(self,piece):
        self.__selected_piece = piece
    def return_selected_piece(self):
        return self.__selected_piece
    def drag(self,rel_position):
        if self.__selected_piece != None:
            self.__selected_piece.drag_rect(rel_position)
    def reset(self):
        self.__initial_position_x = 0
        self.__initial_position_y = 0
        self.__final_position_x = 0
        self.__final_position_y = 0
        self.__selected_piece = None