class Cell:
    #__init__ method:
    #parent is object that instantiated this object, walls is a tuple of booleans
    #representing the cell walls in order (left, top, right, bottom) and True means there is a wall.
    #maze_pos is a tuple of (x, y) representing the position of the cell in maze - top left is (0, 0).
    def __init__(self, parent, walls: tuple, maze_pos: tuple) -> None:
        self.parent = parent #setting attributes of object to the parameters passed in.
        self.walls = walls
        self.maze_pos = maze_pos
        self.start_dist = float("inf") #setting attributes for pathfinding algorithms, default is float("inf") so that the 1st calculated distance will be less than it.
        self.heuristic_estimate = float("inf")
        self.overall_dist_estimate = float("inf")
        self.prev_cell = None #another attribute for pathfinding - prev_cell will be set in algorithm.
    
    def update_estimate(self, start_dist: int, heuristic_estimate: int) -> bool: #to be written later.
        pass
    
    def set_prev_cell(self, prev_cell) -> None: #to be written later.
        pass

    def get_walls(self) -> tuple: #returns this cell's walls tuple
        return self.walls
    
    def get_start_dist(self) -> int|float: #returns this cell's current shortest calculated distance from start cell (start and finish as defined by pathfinding alg, not the player's start and finish).
        return self.start_dist

    def get_heuristic_estimate(self) -> int|float: #returns this cell's current estimated distance from finish cell (start and finish as defined by pathfinding alg, not the player's start and finish).
        return self.heuristic_estimate

    def get_overall_estimate(self) -> int|float: #returns this cell's current overall distance estimate from start to finish cell (start and finish as defined by pathfinding alg, not the player's
        return self.overall_dist_estimate        #start and finish).

    def get_maze_pos(self) -> tuple: #returns the tuple of this cell's position in the maze, in the form (x, y) where top left is (0, 0).
        return self.maze_pos
    
    def draw_cell(self, canvas):
        ...
