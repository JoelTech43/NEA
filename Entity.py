import pygame #pygame used to draw the entity. Initialised in main.py but must be imported here to use the functions in this file.
from random import choice
from math import sqrt

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

    # def __determine_target_cell(self) -> tuple:
    #     player_maze_pos, _ = self._parent.get_entity_positions()
    #     distance = sqrt((player_maze_pos[0]-self._maze_pos[0])**2 + (player_maze_pos[1]-self._maze_pos[1])**2) #Pythagorean distance between enemy and player.
    #     maze_height = self._parent.get_maze_height()

    #     if distance < 5:
    #         target_cell = player_maze_pos
    #     else:


    def __find_shortest_route(self, target_cell: tuple) -> list:
        cells = self._parent.get_maze().get_cells()
        visited = []
        potential = []

        visiting_cell_coord = self._maze_pos
        
        visiting_cell = cells[visiting_cell_coord[1]][visiting_cell_coord[0]]

        visiting_cell.update_estimate(0, 10000)

        while visiting_cell_coord != target_cell:
            print(visiting_cell_coord)
            visited.append(visiting_cell_coord)
            
            walls = visiting_cell.get_walls()

            considering_cell_coords = []

            if walls[0] is False:
                considering_coord = (visiting_cell_coord[0]-1, visiting_cell_coord[1])
                considering_cell_coords.append(considering_coord)
            
            if walls[1] is False:
                considering_coord = (visiting_cell_coord[0], visiting_cell_coord[1]-1)
                considering_cell_coords.append(considering_coord)
            
            if walls[2] is False:
                considering_coord = (visiting_cell_coord[0]+1, visiting_cell_coord[1])
                considering_cell_coords.append(considering_coord)
            
            if walls[3] is False:
                considering_coord = (visiting_cell_coord[0], visiting_cell_coord[1]+1)
                considering_cell_coords.append(considering_coord)
            
            for considering_coord in considering_cell_coords:
                if considering_coord not in visited: #don't attempt to update visited cells as they already have shortest route
                    potential.append(considering_coord)
                    considering_cell = cells[considering_coord[1]][considering_coord[0]]

                    start_dist = visiting_cell.get_start_dist() + 1
                    heuristic_estimate = abs(target_cell[0]-considering_coord[0])+abs(target_cell[1]-considering_coord[1])

                    updated = considering_cell.update_estimate(start_dist, heuristic_estimate)

                    if updated:
                        considering_cell.set_prev_cell(visiting_cell)

            potential = list(set(potential))

            potential.sort(key=lambda coord: (cells[coord[1]][coord[0]].get_overall_estimate(), cells[coord[1]][coord[0]].get_heuristic_estimate())) #sort primarily by total estimate, then by heuristic estimate.

            visiting_cell_coord = potential[0]
            del potential[0]

            visiting_cell = cells[visiting_cell_coord[1]][visiting_cell_coord[0]]
        
        #out of loop so visiting_cell is destination
        route = [] #list to hold all coords along shortest route

        while visiting_cell.get_prev_cell() != None: #while haven't got back to start
            route.append(visiting_cell.get_maze_pos()) #add current cell to route
            visiting_cell = visiting_cell.get_prev_cell() #move to previous cell
        
        #route list now starts with destination and ends with start
        route.reverse() #now starts at start and ends at end. DOESN'T INCLUDE START CELL.
        return route

    def __move_enemy(self, dest: tuple) -> None:
        _, enemy_poses = self._parent.get_entity_positions()
        if dest in enemy_poses:
            options = [(self._maze_pos[0]-1,self._maze_pos[1]),(self._maze_pos[0]+1,self._maze_pos[1]),(self._maze_pos[0],self._maze_pos[1]-1),(self._maze_pos[0]-1,self._maze_pos[1]+1)]
            options.remove(dest)
            dest = choice(options)
        
        self._maze_pos = dest

    def make_calculated_move(self) -> None:
        player_maze_pos, _ = self._parent.get_entity_positions()
        shortest_route = self.__find_shortest_route(player_maze_pos)

        self.__move_enemy(shortest_route[0])
        self._parent.get_maze().reset_cell_estimates()