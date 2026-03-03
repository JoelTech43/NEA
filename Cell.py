import pygame #pygame used to draw the cell. Initialised in main.py but must be imported here to use the functions in this file.

class Cell:
    #__init__ method:
    #parent is object that instantiated this object, walls is a tuple of booleans
    #representing the cell walls in order (left, top, right, bottom) and True means there is a wall.
    #maze_pos is a tuple of (x, y) representing the position of the cell in maze - top left is (0, 0).
    #screen_pos is a tuple of (x,y) representing the top left coordinate on the screen.
    #cell_height is the height/width of the cell in px.
    def __init__(self, parent, walls: tuple, maze_pos: tuple, screen_pos: tuple, cell_height: int) -> None:
        self.__parent = parent #setting attributes of object to the parameters passed in.
        self.__walls = walls
        self.__maze_pos = maze_pos
        self.__screen_pos = screen_pos
        self.__cell_height = cell_height
        self.__border_width = 1 #border thickness in pixels.
        self.__start_dist = float("inf") #setting attributes for pathfinding algorithms, default is float("inf") so that the 1st calculated distance will be less than it.
        self.__heuristic_estimate = float("inf")
        self.__overall_dist_estimate = float("inf")
        self.__prev_cell = None #another attribute for pathfinding - prev_cell will be set in algorithm.
    
    def update_estimate(self, start_dist: int, heuristic_estimate: int|float) -> bool:
        new_total = start_dist+heuristic_estimate #calculates total estimate of route distance
        if new_total < self.__overall_dist_estimate: #if lower than previous estimates, we have found new shortest route to this cell. Update all vars.
            self.__start_dist = start_dist
            self.__heuristic_estimate = heuristic_estimate
            self.__overall_dist_estimate = new_total
            return True #returns boolean showing whether cell was updated or not.
        return False
    
    def set_prev_cell(self, prev_cell) -> None: #to be written later.
        self.__prev_cell = prev_cell
    
    def get_prev_cell(self):
        return self.__prev_cell

    def get_walls(self) -> tuple: #returns this cell's walls tuple
        return self.__walls
    
    def get_start_dist(self) -> int|float: #returns this cell's current shortest calculated distance from start cell (start and finish as defined by pathfinding alg, not the player's start and finish).
        return self.__start_dist

    def get_heuristic_estimate(self) -> int|float: #returns this cell's current estimated distance from finish cell (start and finish as defined by pathfinding alg, not the player's start and finish).
        return self.__heuristic_estimate

    def get_overall_estimate(self) -> int|float: #returns this cell's current overall distance estimate from start to finish cell (start and finish as defined by pathfinding alg, not the player's
        return self.__overall_dist_estimate        #start and finish).

    def get_maze_pos(self) -> tuple: #returns the tuple of this cell's position in the maze, in the form (x, y) where top left is (0, 0).
        return self.__maze_pos
    
    def reset_estimates(self):
        self.__prev_cell = None
        self.__start_dist = float("inf")
        self.__heuristic_estimate = float("inf")
        self.__overall_dist_estimate = float("inf")
    
    def draw_cell(self, canvas):
        if self.__walls[0] == True: #draw left wall
            pygame.draw.rect(canvas, (255,255,255), (self.__screen_pos[0], self.__screen_pos[1], self.__border_width, self.__cell_height))
        if self.__walls[1] == True: #draw top wall
            pygame.draw.rect(canvas, (255,255,255), (self.__screen_pos[0], self.__screen_pos[1], self.__cell_height, self.__border_width))
        if self.__walls[2] == True: #draw right wall
            pygame.draw.rect(canvas, (255,255,255), (self.__screen_pos[0]+self.__cell_height-1, self.__screen_pos[1], self.__border_width, self.__cell_height))
        if self.__walls[3] == True: #draw bottom wall
            pygame.draw.rect(canvas, (255,255,255), (self.__screen_pos[0], self.__screen_pos[1]+self.__cell_height-1, self.__cell_height, self.__border_width))