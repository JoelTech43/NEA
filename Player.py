from Entity import Entity
import pygame

class Player(Entity):
    #__init__ method:
    #parent is object that instantiated this object.
    #move_distance is an integer representing how many cells the entity moves per turn.
    #maze_pos is a tuple of (x, y) representing the position of the cell in maze - top left is (0, 0).
    #cell_height is the height/width of the cell in px.
    def __init__(self, parent, move_distance: int, maze_pos: tuple, cell_height: int) -> None:
        super().__init__(parent, move_distance, maze_pos, cell_height) #calls Entity's __init__ to do most of the setup
        self.__suggested_move = (0,0)
        self._col = (0,255,0)
    
    #__validate_input() - takes direction player wants to move in and returns True if this is a valid move, and False if not.
    #move_dir is a tuple representing direction to move (-1,0) is left, (1,0) is right, (0,-1) is up, (0,1) is down.
    #checks if the move would place the player on the same square as an enemy, or if there is a wall blocking that direction.
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

    #__display_suggested_move() - draws square to display the inputted move before it is confirmed
    def __display_suggested_move(self, canvas) -> None:
        suggested_x = self._maze_pos[0] + self.__suggested_move[0]
        suggested_y = self._maze_pos[1] + self.__suggested_move[1]
        maze_screen_pos = self._parent.get_maze().get_screen_pos()
        suggested_screen_x = maze_screen_pos[0]+(suggested_x*self._cell_height)+1
        suggested_screen_y = maze_screen_pos[1]+(suggested_y*self._cell_height)+1
        pygame.draw.rect(canvas, (255,255,0), (suggested_screen_x, suggested_screen_y, self._cell_height-2, self._cell_height-2))
    
    #draw_entity() - overrides the Entity draw_entity() method so that it displays the suggested move and then calls the parent method to draw the player.
    def draw_entity(self, canvas) -> None:
        self.__display_suggested_move(canvas)
        super().draw_entity(canvas)
    
    #enter_move() - takes a move in the form of a tuple (change in x, change in y) and if valid it sets the Player's suggested_move to the direction.
    def enter_move(self, move_dir:tuple):
        if self.__validate_input(move_dir) == True:
            self.__suggested_move = move_dir

    #move_player() - moves the player in the direction stored in suggested move, returning True. If no direction entered (suggested_move = (0,0)) returns False.
    def move_player(self) -> bool:
        if self.__suggested_move != (0,0):
            x = self._maze_pos[0] + self.__suggested_move[0]
            y = self._maze_pos[1] + self.__suggested_move[1]
            self._maze_pos = (x,y)
            self.__suggested_move = (0,0)
            return True
        
        return False