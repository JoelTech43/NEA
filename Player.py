from Entity import Entity
import pygame

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

    def move_player(self) -> bool:
        if self.__suggested_move != (0,0):
            x = self._maze_pos[0] + self.__suggested_move[0]
            y = self._maze_pos[1] + self.__suggested_move[1]
            self._maze_pos = (x,y)
            self.__suggested_move = (0,0)
            return True
        
        return False