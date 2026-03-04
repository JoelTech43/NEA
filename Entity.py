import pygame #pygame used to draw the entity. Initialised in main.py but must be imported here to use the functions in this file.

class Entity:
    #__init__ method:
    #parent is object that instantiated this object.
    #move_distance is an integer representing how many cells the entity moves per turn.
    #maze_pos is a tuple of (x, y) representing the position of the cell in maze - top left is (0, 0).
    #cell_height is the height/width of the cell in px.
    def __init__(self, parent, move_distance: int, maze_pos: tuple, cell_height: int) -> None:
        self._parent = parent
        self._move_distance = move_distance
        self._maze_pos = maze_pos
        self._cell_height = cell_height
        self._col = (0,0,255)
    
    def draw_entity(self, canvas) -> None:
        maze_screen_pos = self._parent.get_maze().get_screen_pos()
        player_screen_x = maze_screen_pos[0]+(self._maze_pos[0]*self._cell_height)+1
        player_screen_y = maze_screen_pos[1]+(self._maze_pos[1]*self._cell_height)+1
        pygame.draw.rect(canvas, self._col, (player_screen_x, player_screen_y, self._cell_height-2, self._cell_height-2))

    def get_maze_pos(self) -> tuple:
        return self._maze_pos