from Entity import Entity
from random import choice

class Enemy(Entity):
    #__init__ method:
    #parent is object that instantiated this object.
    #move_distance is an integer representing how many cells the entity moves per turn.
    #maze_pos is a tuple of (x, y) representing the position of the cell in maze - top left is (0, 0).
    #cell_height is the height/width of the cell in px.
    def __init__(self, parent, move_distance: int, maze_pos: tuple, cell_height: int) -> None:
        super().__init__(parent, move_distance, maze_pos, cell_height) #calls Entity's __init__ to do most of the setup
        self._col = (255,0,0)

    #__find_shortest_route() - finds shortest route between Enemy's current position and the target cell.
    #target_cell is a tuple (x,y) representing the coord in the maze that the enemy wants to move towards.
    #Returns a tuple of tuples. Each inner tuple is the coord of the cells along the route. Route includes target_cell but not the start/current cell.
    #Checks if a route for this start/dest is already in the level_handler's adjacency matrix - if so use it, if not calc the route and add it to the adj mat.
    def __find_shortest_route(self, target_cell: tuple) -> tuple:
        adj_mat_route = self._parent.get_route_between_cells(self._maze_pos, target_cell) #either a route or None
        
        if adj_mat_route == None: #no route previously found.
            cells = self._parent.get_maze().get_cells() #gets Maze's list of Cell objects.
            visited = [] #cells we have been to + therefore have shortest route to.
            potential = [] #cells we can move to from ones we have visited.

            visiting_cell_coord = self._maze_pos #starts by visiting the cell enemy is currently in.
            
            visiting_cell = cells[visiting_cell_coord[1]][visiting_cell_coord[0]]

            visiting_cell.update_estimate(0, 10000) #10000 as lower than infinity (so updates cell distance values) but large enough to never be smaller than an actual calculated value.

            while visiting_cell_coord != target_cell:
                visited.append(visiting_cell_coord)
                
                walls = visiting_cell.get_walls()

                considering_cell_coords = []

                if walls[0] is False: #based on the walls around the visiting cell, add adjacent cells to considering
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
            self.__update_adj_mat(self._maze_pos, route.copy())
        
        else:
            route = list(adj_mat_route)
            route.append(target_cell) #route from adj mat doesn't include destination cell, so add it here.

        return tuple(route)

    def __update_adj_mat(self, start: tuple, shortest_route: list): #updates adj_matrix. shortest_route DOES NOT include start, DOES include dest.
        shortest_route.insert(0,start) #now shortest_route includes start and dest
        for start_cell_ind in range(len(shortest_route)-1):
            for dest_cell_ind in range(len(shortest_route)):
                if self._parent.get_route_between_cells(shortest_route[start_cell_ind], shortest_route[dest_cell_ind]) == None:
                    new_route = [cell_coord for cell_coord in shortest_route[start_cell_ind+1:dest_cell_ind]] #route between start_cell and dest_cell, not including either.
                    self._parent.set_route_between_cells(shortest_route[start_cell_ind], shortest_route[dest_cell_ind], new_route)

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