from Maze import Maze
from Enemy import Enemy
from Player import Player
import pygame

class LevelHandler:
    def __init__(self, parent, canvas, level_id: int) -> None:
        self.__parent = parent
        self.__canvas = canvas
        self.__level_id = level_id

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


        self.__CELL_HEIGHT = self.__parent.get_maze_screen_height()//maze_info["height"] #calculates cell height based on maze height.
        self.__maze = Maze(self, maze_info["maze"], maze_info["height"], self.__CELL_HEIGHT, self.__parent.get_maze_screen_pos(), maze_info["finish"])
        self.__player = Player(self, 1, maze_info["player"], self.__CELL_HEIGHT)
        self.__enemies = [Enemy(self, 1, pos, self.__CELL_HEIGHT) for pos in maze_info["enemies"]]
        self.__MAZE_CELL_HEIGHT = maze_info["height"]
        
        #instantiate timer object

        self.__exit_level = False #level_loop runs until this is True
        #Adjacency matrix functionality
        self.__route_adj_mat = [[None for cell in range(maze_info["height"]**2)] for row in range(maze_info["height"]**2)]
        

    def level_loop(self) -> bool:
        while self.__exit_level == False:
            self.__user_move()
            self.__check_game_state()
            if self.__exit_level == False:
                self.__enemy_move()
                self.__check_game_state()
            

    def __user_move(self):
        user_turn = True
        while user_turn == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #if user clicks close button, set exit to True to escape game loop, closing program.
                    self.__parent.save_and_quit()
                    user_turn = False
                    self.__exit_level = True
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        self.__player.enter_move((-1,0))
                    elif event.key in (pygame.K_w, pygame.K_UP):
                        self.__player.enter_move((0,-1))
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.__player.enter_move((1,0))
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        self.__player.enter_move((0,1))
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if self.__player.move_player() == True:
                            user_turn = False
            self.__canvas.fill((0,0,0))
            self.__maze.draw_maze(self.__canvas)
            self.__draw_entities()
            pygame.display.update() #updates the window with any changes.

    def __enemy_move(self):
        for enemy in self.__enemies:
            if self.__exit_level == False:
                enemy.make_calculated_move()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__parent.save_and_quit()
                        self.__exit_level = True
                    if event.type == pygame.KEYDOWN:
                        pass #will add pause functionality at later point
        
        self.__canvas.fill((0,0,0))
        self.__maze.draw_maze(self.__canvas)
        self.__draw_entities()
        pygame.display.update() #updates the window with any changes.


    def pause(self):
        pass

    def __check_game_state(self) -> None:
        if self.__check_game_loss() == True:
            self.__game_over()
        elif self.__check_game_win() == True:
            self.__game_win()

    def __check_game_loss(self) -> bool:
        player_pos, enemy_poses = self.get_entity_positions()
        return player_pos in enemy_poses

    def __check_game_win(self) -> bool:
        player_pos, _ = self.get_entity_positions()
        finish_coord = self.__maze.get_finish_coord()
        return player_pos == finish_coord

    def __game_over(self) -> bool:
        print("Game Over!")
        self.__exit_level = True

    def __game_win(self) -> bool:
        print("Game Won!")
        self.__exit_level = True

    def find_cell_adj_mat_index(self, maze_pos):
        maze_height = self.get_maze_cell_height()
        ind = maze_pos[1]*maze_height + maze_pos[0]
        return ind

    def get_route_between_cells(self, start: tuple, dest: tuple) -> None|tuple:
        start_ind = self.find_cell_adj_mat_index(start)
        dest_ind = self.find_cell_adj_mat_index(dest)
        route = self.__route_adj_mat[start_ind][dest_ind]
        return route

    def set_route_between_cells(self, start: tuple, dest: tuple, route: tuple):
        current_route = self.get_route_between_cells(start, dest)
        current_route_length = float("inf") if current_route == None else len(current_route)
        start_ind = self.find_cell_adj_mat_index(start)
        dest_ind = self.find_cell_adj_mat_index(dest)
        if len(route) < current_route_length:
            self.__route_adj_mat[start_ind][dest_ind] = route
            self.__route_adj_mat[dest_ind][start_ind] = route[::-1]

    def get_player(self) -> Player:
        return self.__player
    
    def get_enemies(self) -> list:
        return self.__enemies
    
    def get_maze_screen_height(self) -> int:
        return self.__parent.get_maze_screen_height()
    
    def get_maze_cell_height(self) -> int:
        return self.__MAZE_CELL_HEIGHT

    def get_entity_positions(self) -> tuple|list:
        player_pos = self.__player.get_maze_pos()
        enemy_poses = [enemy.get_maze_pos() for enemy in self.__enemies]
        return player_pos, enemy_poses
    
    def get_maze(self) -> Maze:
        return self.__maze
    
    def __draw_entities(self) -> None:
        self.__player.draw_entity(self.__canvas)
        for enemy in self.__enemies:
            enemy.draw_entity(self.__canvas)