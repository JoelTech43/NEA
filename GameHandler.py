import pygame
from LevelHandler import LevelHandler

class GameHandler:
    def __init__(self):
        pygame.init() #initialises pygame. Necessary to use pygame functions.
        
        #create music handler, set theme, load user data.

        main_desktop_size = pygame.display.get_desktop_sizes()[1] #gets display sizes (px) as tuples (width, height). I use index 0 as this is the main monitor.
        self.WINDOW_SIZE = (main_desktop_size[0]*0.8, main_desktop_size[1]*0.8) #sets window size to 80% of screen size so that user can easily switch to other windows and close game, but large enough to see maze clearly.
        self.MAZE_HEIGHT = min(self.WINDOW_SIZE[0]*0.9, self.WINDOW_SIZE[1]*0.95) #maze height is either set to 90% of the window width, or 95% of window height. Means maze is as large as possible whilst leaving some around it.
        self.MAZE_SCREEN_POS = ((self.WINDOW_SIZE[0]-self.MAZE_HEIGHT)//2, (self.WINDOW_SIZE[1]-self.MAZE_HEIGHT)//2) #start position in window (x,y) from top left. Centers maze by finding difference between window size and maze size and halving.

        self.canvas = pygame.display.set_mode(self.WINDOW_SIZE) #creates the window, with the size we calculated earlier.
        pygame.display.set_caption("Joel's A-maze-ing Game")
        self.running = True #while True, game loop runs.
    
    def main_game_loop(self):
        pass

    def settings_menu(self):
        pass

    def play_level(self, level_id: int):
        level_handler = LevelHandler(self, self.canvas, level_id)

    def process_inputs(self):
        pass

    def save_and_quit(self):
        pass