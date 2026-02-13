from Maze import Maze #importing my Maze class to create the maze object. Cell is imported in Maze.py so I don't need to import it here.
import pygame #importing pygame to create game window and handle user inputs.

pygame.init() #initialises pygame. Necessary to use pygame functions.

#test data, will be stored in file later to be read by program.
maze_info = {
    "height": 8, #number of rows in maze
    "width": 6, #number of columns in maze
    "player": [0, 0], #coordinates of where player starts
    "finish": [5, 5], #coodinates of finish point.
    "enemies": [[3, 6]], #list of coordinates of enemy starting points.
    "maze": [[[True, True, True, False], [True, True, False, False], [False, True, False, False], [False, True, False, False], [False, True, True, False], [True, True, True, False]],
             [[True, False, True, False], [True, False, True, True], [True, False, False, False], [False, False, False, False], [False, False, True, False], [True, False, True, False]],
             [[True, False, False, False], [False, True, False, True], [False, False, True, False], [True, False, False, False], [False, False, True, False], [True, False, True, False]],
             [[True, False, False, False], [False, True, False, False], [False, False, False, True], [False, False, False, False], [False, False, True, False], [True, False, True, False]],
             [[True, False, False, True], [False, False, False, True], [False, True, True, True], [True, False, False, True], [False, False, True, True], [True, False, True, False]],
             [[True, True, False, False], [False, True, False, False], [False, True, False, False], [False, True, False, False], [False, True, False, False], [False, False, True, False]],
             [[True, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, True, False]],
             [[True, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, True, True]]]
    #maze is a 3D list representing the maze layout. The outer list contains rows, the next list (separate lines) contain cells in that row, and each cell is a list of 4 booleans representing the walls
    #of that cell in the order [left, top, right, bottom]. True means there is a wall.
}

main_desktop_size = pygame.display.get_desktop_sizes()[1] #gets display sizes (px) as tuples. I use index 0 as this is the main monitor.
WINDOW_SIZE = (main_desktop_size[0]*0.8, main_desktop_size[1]*0.8) #sets window size to 80% of screen size so that user can easily switch to other windows and close game, but large enough to see maze clearly.
CELL_HEIGHT = min(WINDOW_SIZE[0] // maze_info["width"], WINDOW_SIZE[1] // maze_info["height"]) #calculates size of each cell in pixels if maze was to fill window horizontally or vertically
#Then takes the smaller of the two to ensure maze fits in window and fills window in one direction.

canvas = pygame.display.set_mode(WINDOW_SIZE) #creates the window, with the size we calculated earlier.
pygame.display.set_caption("Joel's A-maze-ing Game")

exit = False
while not exit: #main game loop, runs until user clicks window's close button.
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if user clicks close button, set exit to True to escape game loop, closing program.
            exit = True

    pygame.display.update() #updates the window with any changes. None at the moment.