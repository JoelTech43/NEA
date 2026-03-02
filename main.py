from Maze import Maze #importing my Maze class to create the maze object. Cell is imported in Maze.py so I don't need to import it here.
import pygame #importing pygame to create game window and handle user inputs.

pygame.init() #initialises pygame. Necessary to use pygame functions.

#test data, will be stored in file later to be read by program.
maze_info = {
    "height": 10,
    "width": 10,
    "player": [4, 0],
    "finish": [5, 9],
    "enemies": [[7, 8],[4, 5],[2, 3],[7, 3]],
    "maze": [
        [[True, True, False, False],[False, True, False, False],[False, True, False, True],[False, True, True, True],[True, True, False, False],[False, True, False, True],[False, True, False, True],[False, True, True, False],[True, True, False, True],[False, True, True, False]],
        [[True, False, True, False],[True, False, False, True],[False, True, False, True],[False, True, True, False],[True, False, False, True],[False, True, True, False],[True, True, False, False],[False, False, True, True],[True, True, False, False],[False, False, True, False]],
        [[True, False, False, True],[False, True, False, False],[False, True, True, False],[True, False, True, False],[True, True, False, False],[False, False, True, True],[True, False, False, True],[False, True, False, True],[False, False, True, True],[True, False, True, False]],
        [[True, True, False, False],[False, False, True, True],[True, False, True, True],[True, False, False, True],[False, False, True, True],[True, True, False, False],[False, True, False, True],[False, True, False, True],[False, True, True, True],[True, False, True, False]],
        [[True, False, False, True],[False, True, False, False],[False, True, True, False],[True, True, False, False],[False, True, True, False],[True, False, False, True],[False, True, False, False],[False, True, False, True],[False, True, False, True],[False, False, True, True]],
        [[True, True, False, False],[False, False, True, True],[True, False, False, True],[False, False, True, True],[True, False, True, False],[True, True, False, False],[False, False, True, True],[True, True, False, True],[False, True, False, True],[False, True, True, False]],
        [[True, False, True, False],[True, True, False, True],[False, True, False, True],[False, True, False, True],[False, False, True, True],[True, False, False, True],[False, True, False, True],[False, True, False, True],[False, True, True, False],[True, False, True, False]],
        [[True, False, True, False],[True, True, False, False],[False, True, False, True],[False, True, True, False],[True, True, False, False],[False, True, True, False],[True, True, True, False],[True, True, False, False],[False, False, False, True],[False, False, True, True]],
        [[True, False, True, False],[True, False, True, False],[True, True, False, False],[False, False, True, True],[True, False, True, False],[True, False, True, False],[True, False, True, False],[True, False, False, False],[False, True, True, False],[True, True, True, False]],
        [[True, False, False, True],[False, False, True, True],[True, False, False, True],[False, True, False, True],[False, False, True, True],[True, False, True, True],[True, False, False, True],[False, False, True, True],[True, False, False, True],[False, False, True, True]]
        ]
}

main_desktop_size = pygame.display.get_desktop_sizes()[1] #gets display sizes (px) as tuples (width, height). I use index 0 as this is the main monitor.
WINDOW_SIZE = (main_desktop_size[0]*0.8, main_desktop_size[1]*0.8) #sets window size to 80% of screen size so that user can easily switch to other windows and close game, but large enough to see maze clearly.
MAZE_HEIGHT = min(WINDOW_SIZE[0]*0.9, WINDOW_SIZE[1]*0.95) #maze height is either set to 90% of the window width, or 95% of window height. Means maze is as large as possible whilst leaving some around it.
CELL_HEIGHT = MAZE_HEIGHT//maze_info["height"] #calculates cell height based on maze height.
MAZE_SCREEN_POS = ((WINDOW_SIZE[0]-MAZE_HEIGHT)//2, (WINDOW_SIZE[1]-MAZE_HEIGHT)//2) #start position in window (x,y) from top left. Centers maze by finding difference between window size and maze size and halving.

canvas = pygame.display.set_mode(WINDOW_SIZE) #creates the window, with the size we calculated earlier.
pygame.display.set_caption("Joel's A-maze-ing Game")

maze = Maze(None, maze_info["maze"], maze_info["height"], CELL_HEIGHT, MAZE_SCREEN_POS)

exit = False
while not exit: #main game loop, runs until user clicks window's close button.
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if user clicks close button, set exit to True to escape game loop, closing program.
            exit = True
    maze.draw_maze(canvas)
    pygame.display.update() #updates the window with any changes. None at the moment.