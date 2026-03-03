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

class Player(Entity):
    def __init__(self, parent, move_distance: int, maze_pos: tuple, cell_height: int) -> None:
        super().__init__(parent, move_distance, maze_pos, cell_height)
        self.__suggested_move = (0,0)
        self._col = (0,255,0)
    
    def __validate_input(self, move_dir: tuple) -> bool:
        current_cell_walls = self._parent.get_maze().get_cell(self._maze_pos).get_walls()
        maze_height = self._parent.get_maze().get_maze_height()
        _, enemy_poses = self._parent.get_entity_positions()
        new_maze_pos = (self._maze_pos[0]+move_dir[0], self._maze_pos[1]+move_dir[1])

        if new_maze_pos in enemy_poses:
            return False
        elif move_dir == (-1,0) and current_cell_walls[0] == False and self._maze_pos[0] > 0:
            return True
        elif move_dir == (0,-1) and current_cell_walls[1] == False and self._maze_pos[1] > 0:
            return True
        elif move_dir == (1,0) and current_cell_walls[2] == False and self._maze_pos[0] < (maze_height-1):
            return True
        elif move_dir == (0,1) and current_cell_walls[3] == False and self._maze_pos[1] < (maze_height-1):
            return True
        else:
            return False

    def __display_suggested_move(self, canvas) -> None:
        suggested_x = self._maze_pos[0] + self.__suggested_move[0]
        suggested_y = self._maze_pos[1] + self.__suggested_move[1]
        maze_screen_pos = self._parent.get_maze().get_screen_pos()
        suggested_screen_x = maze_screen_pos[0]+(suggested_x*self._cell_height)+1
        suggested_screen_y = maze_screen_pos[1]+(suggested_y*self._cell_height)+1
        pygame.draw.rect(canvas, (255,255,0), (suggested_screen_x, suggested_screen_y, self._cell_height-2, self._cell_height-2))
    
    def draw_entity(self, canvas) -> None:
        self.__display_suggested_move(canvas)
        super().draw_entity(canvas)
    
    def enter_move(self, move_dir):
        if self.__validate_input(move_dir) == True:
            self.__suggested_move = move_dir

    def move_player(self):
        x = self._maze_pos[0] + self.__suggested_move[0]
        y = self._maze_pos[1] + self.__suggested_move[1]
        self._maze_pos = (x,y)
        self.__suggested_move = (0,0)

class Enemy(Entity):
    def __init__(self, parent, move_distance: int, maze_pos: tuple, cell_height: int) -> None:
        super().__init__(parent, move_distance, maze_pos, cell_height)
        self._col = (255,0,0)

    def determine_target_cell(self) -> tuple:
        pass

    def find_shortest_route(self, target_cell: tuple) -> list:
        pass

    def move_enemy(self, dest: tuple) -> None:
        pass

    def make_calculated_move(self) -> None:
        pass