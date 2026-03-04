class Cell:
    #__init__ method:
    #parent is object that instantiated this object, walls is a tuple of booleans
    #representing the cell walls in order (left, top, right, bottom) and True means there is a wall.
    #maze_pos is a tuple of (x, y) representing the position of the cell in maze - top left is (0, 0).
    #screen_pos is a tuple of (x,y) representing the top left coordinate on the screen.
    #cell_height is the height/width of the cell in px.
    def __init__(self, parent, walls: tuple, maze_pos: tuple, screen_pos: tuple, cell_height: int) -> None:
        self.parent = parent #setting attributes of object to the parameters passed in.
        self.walls = walls
        self.maze_pos = maze_pos
        self.screen_pos = screen_pos
        self.cell_height = cell_height
        self.border_width = 1 #border thickness in pixels.
        self.start_dist = float("inf") #setting attributes for pathfinding algorithms, default is float("inf") so that the 1st calculated distance will be less than it.
        self.heuristic_estimate = float("inf")
        self.overall_dist_estimate = float("inf")
        self.prev_cell = None #another attribute for pathfinding - prev_cell will be set in algorithm.
    
    def update_estimate(self, start_dist: int, heuristic_estimate: int|float) -> bool:
        new_total = start_dist+heuristic_estimate #calculates total estimate of route distance
        if new_total < self.overall_dist_estimate: #if lower than previous estimates, we have found new shortest route to this cell. Update all vars.
            self.start_dist = start_dist
            self.heuristic_estimate = heuristic_estimate
            self.overall_dist_estimate = new_total
            return True #returns boolean showing whether cell was updated or not.
        return False
    
    def set_prev_cell(self, prev_cell) -> None: #to be written later.
        self.prev_cell = prev_cell
    
    def get_prev_cell(self):
        return self.prev_cell

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
    
    def reset_estimates(self):
        self.prev_cell = None
        self.start_dist = float("inf")
        self.heuristic_estimate = float("inf")
        self.overall_dist_estimate = float("inf")

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

    def get_maze_pos(self) -> tuple:
        return self.maze_pos

class Player(Entity):
    def __init__(self, parent, move_distance: int, maze_pos: tuple, cell_height: int) -> None:
        super().__init__(parent, move_distance, maze_pos, cell_height)
        self.suggested_move = (0,0)
        self.col = (0,255,0)
    
    def validate_input(self, move_dir: tuple) -> bool:
        current_cell_walls = self.parent.get_maze().get_cell(self.maze_pos).get_walls()
        maze_height = self.parent.get_maze().get_maze_height()
        _, enemy_poses = self.parent.get_entity_positions()
        new_maze_pos = (self.maze_pos[0]+move_dir[0], self.maze_pos[1]+move_dir[1])

        if new_maze_pos in enemy_poses:
            return False
        elif move_dir == (-1,0) and current_cell_walls[0] == False and self.maze_pos[0] > 0:
            return True
        elif move_dir == (0,-1) and current_cell_walls[1] == False and self.maze_pos[1] > 0:
            return True
        elif move_dir == (1,0) and current_cell_walls[2] == False and self.maze_pos[0] < (maze_height-1):
            return True
        elif move_dir == (0,1) and current_cell_walls[3] == False and self.maze_pos[1] < (maze_height-1):
            return True
        else:
            return False
    
    def enter_move(self, move_dir):
        if self.validate_input(move_dir) == True:
            self.suggested_move = move_dir

    def move_player(self):
        x = self.maze_pos[0] + self.suggested_move[0]
        y = self.maze_pos[1] + self.suggested_move[1]
        self.maze_pos = (x,y)
        self.suggested_move = (0,0)

class Enemy(Entity):
    def __init__(self, parent, move_distance: int, maze_pos: tuple, cell_height: int) -> None:
        super().__init__(parent, move_distance, maze_pos, cell_height)
        self.col = (255,0,0)


    def find_shortest_route(self, target_cell: tuple) -> tuple:
        adj_mat_route = self.parent.get_route_between_cells(self.maze_pos, target_cell)
        
        if adj_mat_route == None:
            print("USING A*")
            cells = self.parent.get_maze().get_cells()
            visited = []
            potential = []

            visiting_cell_coord = self.maze_pos
            
            visiting_cell = cells[visiting_cell_coord[1]][visiting_cell_coord[0]]

            visiting_cell.update_estimate(0, 10000) #10000 as lower than inf__init__y (so updates cell distance values) but large enough to never be smaller than an actual calculated value.

            while visiting_cell_coord != target_cell:
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
            route = route[::-1] #now starts at start and ends at end. DOESN'T INCLUDE START CELL.
            self.update_adj_mat(self.maze_pos, route.copy())
        
        else:
            print("USING ADJACENCY MATRIX")
            route = list(adj_mat_route)
            route.append(target_cell) #route from adj mat doesn't include destination cell, so add it here.

        return tuple(route)

    def update_adj_mat(self, start: tuple, shortest_route: list): #updates adj_matrix. shortest_route DOES NOT include start, DOES include dest.
        shortest_route.insert(0,start) #now shortest_route includes start and dest
        for start_cell_ind in range(len(shortest_route)-1):
            for dest_cell_ind in range(len(shortest_route)):
                if self.parent.get_route_between_cells(shortest_route[start_cell_ind], shortest_route[dest_cell_ind]) == None:
                    new_route = [cell_coord for cell_coord in shortest_route[start_cell_ind+1:dest_cell_ind]] #route between start_cell and dest_cell, not including either.
                    self.parent.set_route_between_cells(shortest_route[start_cell_ind], shortest_route[dest_cell_ind], new_route)


    def make_calculated_move(self) -> None:
        player_maze_pos, _ = self.parent.get_entity_positions()
        shortest_route = self.find_shortest_route(player_maze_pos)

        print(f"From {self.maze_pos} to {player_maze_pos}\nPath: {shortest_route}\n")
        self.maze_pos = shortest_route[0]
        self.parent.get_maze().reset_cell_estimates()

class Maze:
    #__init__ method:
    #parent is object that instantiated this object, cell_array is a 2D array of lists representing each cell (3D array),
    #maze_height is a integer representing how many rows/cols the maze has,
    #cell_height is the height of each cell in pixels.
    #screen_pos is a tuple (x, y) where x and y are integers. Represents coord in screen of top left of maze.
    def __init__(self, parent, cell_array: list, maze_height: int, cell_height: int, screen_pos: tuple) -> None:
        self.parent = parent
        self.maze_height = maze_height
        self.screen_pos = screen_pos
        self.cell_height = cell_height
        self.cells = [] #will be a 2D list of Cell objects, each inner list is a row in the maze.

        for row in range(self.maze_height):
            new_row = [] #new list for each row
            for col in range(self.maze_height):
                cell_screen_pos = (self.screen_pos[0]+col*self.cell_height, self.screen_pos[1]+row*self.cell_height) #calculate position of cell on screen.
                new_row.append(Cell(self, cell_array[row][col], (col, row), cell_screen_pos, self.cell_height)) #instantiating a Cell object for each cell in the cell_array and storing it in a list for each row.
            self.cells.append(new_row) #appending the row to the full list of cells.
    
    def get_screen_pos(self) -> tuple: #returns the top left screen coordinate of the maze
        return self.screen_pos

    def get_cell(self, maze_pos: tuple) -> Cell: #returns the Cell object for the given position.
        return self.cells[maze_pos[1]][maze_pos[0]]
    
    def get_cells(self) -> list: #returns the 2D list of Cell objects representing the maze.
        return self.cells
    
    def get_cell_height(self) -> int: #returns the height/width of each cell in pixels.
        return self.cell_height
    
    def get_maze_height(self) -> int:
        return self.maze_height

    def reset_cell_estimates(self):
        for row in self.cells:
            for cell in row:
                cell.reset_estimates()


class LevelHandler:
    def __init__(self, parent, canvas, level_id: int) -> None:
        self.parent = parent
        self.canvas = canvas
        self.level_id = level_id

        #would load maze info from file here, just using test data for now.
        maze_info = {
            "height": 10,
            "width": 10,
            "player": (4, 0),
            "finish": (5, 9),
            "enemies": [(7, 8),(4, 5),(2, 3),(7, 3)],
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

        self.maze = Maze(self, maze_info["maze"], maze_info["height"], 0, (0,0))
        self.player = Player(self, 1, maze_info["player"], 0)
        self.enemies = [Enemy(self, 1, pos, 0) for pos in maze_info["enemies"]]
        self.MAZE_CELL_HEIGHT = maze_info["height"]
        
        #instantiate timer object

        self.exit_level = False #level_loop runs until this is True
        #Adjacency matrix functionality
        self.route_adj_mat = [[None for cell in range(maze_info["height"]**2)] for row in range(maze_info["height"]**2)]

    def find_cell_adj_mat_index(self, maze_pos):
        maze_height = self.get_maze_cell_height()
        ind = maze_pos[1]*maze_height + maze_pos[0]
        return ind

    def get_route_between_cells(self, start: tuple, dest: tuple) -> None|tuple:
        start_ind = self.find_cell_adj_mat_index(start)
        dest_ind = self.find_cell_adj_mat_index(dest)
        route = self.route_adj_mat[start_ind][dest_ind]
        return route

    def set_route_between_cells(self, start: tuple, dest: tuple, route: tuple):
        current_route = self.get_route_between_cells(start, dest)
        current_route_length = float("inf") if current_route == None else len(current_route)
        start_ind = self.find_cell_adj_mat_index(start)
        dest_ind = self.find_cell_adj_mat_index(dest)
        if len(route) < current_route_length:
            self.route_adj_mat[start_ind][dest_ind] = route
            self.route_adj_mat[dest_ind][start_ind] = route[::-1]
        

    def get_player(self) -> Player:
        return self.player
    
    def get_enemies(self) -> list:
        return self.enemies
    
    def get_maze_cell_height(self) -> int:
        return self.MAZE_CELL_HEIGHT

    def get_entity_positions(self) -> tuple|list:
        player_pos = self.player.get_maze_pos()
        enemy_poses = [enemy.get_maze_pos() for enemy in self.enemies]
        return player_pos, enemy_poses
    
    def get_maze(self) -> Maze:
        return self.maze


level_handler = LevelHandler(None, None, 0)

level_handler.enemies[0].make_calculated_move()
level_handler.enemies[0].make_calculated_move()
