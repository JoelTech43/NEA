import pygame
from LevelHandler import LevelHandler #importing my LevelHandler class

class GameHandler:
    def __init__(self):
        pygame.init() #initialises pygame. Necessary to use pygame functions.
        
        #create music handler, set theme, load user data.

        main_desktop_size = pygame.display.get_desktop_sizes()[0] #gets display sizes (px) as tuples (width, height). I use index 0 as this is the main monitor.
        self.__WINDOW_SIZE = (main_desktop_size[0]*0.8, main_desktop_size[1]*0.8) #sets window size to 80% of screen size so that user can easily switch to other windows and close game, but large enough to see maze clearly.
        self.__MAZE_SCREEN_HEIGHT = min(int(self.__WINDOW_SIZE[0]*0.9), int(self.__WINDOW_SIZE[1]*0.95)) #maze height is either set to 90% of the window width, or 95% of window height. Means maze is as large as possible whilst leaving some around it.
        self.__MAZE_SCREEN_POS = ((self.__WINDOW_SIZE[0]-self.__MAZE_SCREEN_HEIGHT)//2, (self.__WINDOW_SIZE[1]-self.__MAZE_SCREEN_HEIGHT)//2) #start position in window (x,y) from top left. Centers maze by finding difference between window size and maze size and halving.

        self.__canvas = pygame.display.set_mode(self.__WINDOW_SIZE) #creates the window, with the size we calculated earlier.
        pygame.display.set_caption("Joel's A-maze-ing Game") #sets window title
        self.__running = True #while True, game loop runs.
    
    #main_game_loop is the method that contains the main game loop. When this method ends, so does the game.
    def main_game_loop(self):
        self.play_level(1)

    #settings_menu method creates settings menu over current screen, adjusts settings, and then closes, returning the user back to where they were.
    def settings_menu(self):
        pass

    #play_level method instantiates the LevelHandler to play a specific level.
    #level_id is an integer representing what level is to be loaded.
    def play_level(self, level_id: int):
        level_handler = LevelHandler(self, self.__canvas, level_id) #instantiate LevelHandler
        replay = level_handler.level_loop() #run the main level_handler loop. returns a boolean of whether the user would like to play the level again.

    def process_inputs(self):
        pass

    def save_and_quit(self):
        self.__running = False

    #get_maze_screen_pos method returns a tuple (x,y) representing the position (in pixels) of the top left corner of the maze from the top left corner of the window.
    def get_maze_screen_pos(self) -> tuple:
        return self.__MAZE_SCREEN_POS
    
    #get_maze_screen_height method returns an integer representing the height and width (in pixels) of the maze on the screen.
    def get_maze_screen_height(self) -> int:
        return self.__MAZE_SCREEN_HEIGHT