import pygame
import pygame_gui
from LevelHandler import LevelHandler #importing my LevelHandler class
from GUIHandler import GUIHandler

class GameHandler:
    def __init__(self):
        pygame.init() #initialises pygame. Necessary to use pygame functions.

        self.__gui_handler = GUIHandler()
        #create music handler, set theme, load user data.

        self.__running = True #while True, game loop runs.

    #main_game_loop is the method that contains the main game loop. When this method ends, so does the game.
    def main_game_loop(self):
        while self.__running == True:

            self.play_level(1)

    #settings_menu method creates settings menu over current screen, adjusts settings, and then closes, returning the user back to where they were.
    def settings_menu(self):
        pass

    #play_level method instantiates the LevelHandler to play a specific level.
    #level_id is an integer representing what level is to be loaded.
    def play_level(self, level_id: int):
        level_handler = LevelHandler(self, level_id) #instantiate LevelHandler
        replay = level_handler.level_loop() #run the main level_handler loop. returns a boolean of whether the user would like to play the level again.

    def process_inputs(self):
        pass

    def save_and_quit(self):
        self.__running = False
    
    def get_gui_handler(self):
        return self.__gui_handler