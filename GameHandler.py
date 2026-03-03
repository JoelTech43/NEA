import pygame
from LevelHandler import LevelHandler

class GameHandler:
    def __init__(self):
        pygame.init() #initialises pygame. Necessary to use pygame functions.
        
        #create music handler, set theme, load user data.

        main_desktop_size = pygame.display.get_desktop_sizes()[0] #gets display sizes (px) as tuples (width, height). I use index 0 as this is the main monitor.
        self.__WINDOW_SIZE = (main_desktop_size[0]*0.8, main_desktop_size[1]*0.8) #sets window size to 80% of screen size so that user can easily switch to other windows and close game, but large enough to see maze clearly.
        self.__MAZE_HEIGHT = min(int(self.__WINDOW_SIZE[0]*0.9), int(self.__WINDOW_SIZE[1]*0.95)) #maze height is either set to 90% of the window width, or 95% of window height. Means maze is as large as possible whilst leaving some around it.
        self.__MAZE_SCREEN_POS = ((self.__WINDOW_SIZE[0]-self.__MAZE_HEIGHT)//2, (self.__WINDOW_SIZE[1]-self.__MAZE_HEIGHT)//2) #start position in window (x,y) from top left. Centers maze by finding difference between window size and maze size and halving.

        self.__canvas = pygame.display.set_mode(self.__WINDOW_SIZE) #creates the window, with the size we calculated earlier.
        pygame.display.set_caption("Joel's A-maze-ing Game")
        self.__running = True #while True, game loop runs.
    
    def main_game_loop(self):
        self.play_level(1)

    def settings_menu(self):
        pass

    def play_level(self, level_id: int):
        level_handler = LevelHandler(self, self.__canvas, level_id)
        level_handler.level_loop()

    def process_inputs(self):
        pass

    def save_and_quit(self):
        pass

    def get_maze_screen_pos(self) -> tuple:
        return self.__MAZE_SCREEN_POS
    
    def get_maze_height(self) -> int:
        return self.__MAZE_HEIGHT