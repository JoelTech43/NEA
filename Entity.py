import pygame #pygame used to draw the entity. Initialised in main.py but must be imported here to use the functions in this file.

class Entity:
    #__init__ method:
    #parent is object that instantiated this object.
    #move_distance is an integer representing how many cells the entity moves per turn.
    #maze_pos is a tuple of (x, y) representing the position of the cell in maze - top left is (0, 0).
    #cell_height is the height/width of the cell in px.
    def __init__(self, parent, move_distance: int, maze_pos: tuple, cell_height: int) -> None:
        self.parent = parent
        self.move_distance = move_distance
        self.maze_pos = maze_pos
        self.cell_height = cell_height
        self.col = (0,0,255)
    
    def draw_entity(self, canvas) -> None:
        maze_screen_pos = self.parent.maze.get_screen_pos()
        player_screen_x = maze_screen_pos[0]+(self.maze_pos[0]*self.cell_height)+1
        player_screen_y = maze_screen_pos[1]+(self.maze_pos[1]*self.cell_height)+1
        pygame.draw.rect(canvas, self.col, (player_screen_x, player_screen_y, self.cell_height-2, self.cell_height-2))

class Player(Entity):
    def __init__(self, parent, move_distance: int, maze_pos: tuple, cell_height: int) -> None:
        super().__init__(parent, move_distance, maze_pos, cell_height)
        self.suggested_move = (0,0)
        self.col = (0,255,0)
    
    def validate_input(self, move_dir: tuple) -> bool:
        current_cell_walls = self.parent.maze.get_cell(self.maze_pos).get_walls()
        maze_height = self.parent.maze.get_maze_height()
        if move_dir == (-1,0) and current_cell_walls[0] == False and self.maze_pos[0] > 0:
            return True
        elif move_dir == (0,-1) and current_cell_walls[1] == False and self.maze_pos[1] > 0:
            return True
        elif move_dir == (1,0) and current_cell_walls[2] == False and self.maze_pos[0] < (maze_height-1):
            return True
        elif move_dir == (0,1) and current_cell_walls[3] == False and self.maze_pos[1] < (maze_height-1):
            return True
        else:
            return False

    def display_suggested_move(self, canvas) -> None:
        suggested_x = self.maze_pos[0] + self.suggested_move[0]
        suggested_y = self.maze_pos[1] + self.suggested_move[1]
        maze_screen_pos = self.parent.maze.get_screen_pos()
        suggested_screen_x = maze_screen_pos[0]+(suggested_x*self.cell_height)+1
        suggested_screen_y = maze_screen_pos[1]+(suggested_y*self.cell_height)+1
        pygame.draw.rect(canvas, (255,255,0), (suggested_screen_x, suggested_screen_y, self.cell_height-2, self.cell_height-2))
    
    def draw_entity(self, canvas) -> None:
        self.display_suggested_move(canvas)
        super().draw_entity(canvas)
    
    def enter_move(self, move_dir):
        if self.validate_input(move_dir) == True:
            self.suggested_move = move_dir

    def move_player(self):
        x = self.maze_pos[0] + self.suggested_move[0]
        y = self.maze_pos[1] + self.suggested_move[1]
        self.maze_pos = (x,y)

class Enemy(Entity):
    def __init__(self, parent, move_distance: int, maze_pos: tuple, cell_height: int) -> None:
        super().__init__(parent, move_distance, maze_pos, cell_height)
    
    def get_entity_positions(self):
        pass

    def determine_target_cell(self) -> tuple:
        pass

    def find_shortest_route(self, target_cell: tuple) -> list:
        pass

    def move_enemy(self, dest: tuple) -> None:
        pass

    def make_calculated_move(self) -> None:
        pass