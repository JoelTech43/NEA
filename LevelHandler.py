from Maze import Maze
from Enemy import Enemy
from Player import Player
import pygame
import pygame_gui

class LevelHandler:
    #__init__ method:
    #parent is object that instantiated this object, GameHandler in this case.
    #level_id is an integer what maze is to be loaded.
    def __init__(self, parent, level_id: int) -> None:
        self.__parent = parent
        self.__level_id = level_id
        self.__gui_handler = self.__parent.get_gui_handler()
        self.__canvas = self.__gui_handler.get_canvas()
        self.__level_gui = self.__gui_handler.get_level_panel()
        self.__pause_menu_gui = self.__gui_handler.get_pause_menu_panel()

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

        self.__CELL_HEIGHT = self.__gui_handler.get_maze_screen_height()//maze_info["height"] #calculates cell height in pixels by dividing the height of the maze in pixels by number of cells in a column.
        self.__maze = Maze(self, maze_info["maze"], maze_info["height"], self.__CELL_HEIGHT, self.__gui_handler.get_maze_screen_pos(), maze_info["finish"]) 
        self.__player = Player(self, 1, maze_info["player"], self.__CELL_HEIGHT)
        self.__enemies = [Enemy(self, 1, pos, self.__CELL_HEIGHT) for pos in maze_info["enemies"]] #instantiates all needed Enemy objects and stores them in a list.
        self.__MAZE_CELL_HEIGHT = maze_info["height"]
        
        #instantiate timer object

        self.__exit_level = False #level_loop runs until this is True

        self.__route_adj_mat = [[None for cell in range(maze_info["height"]**2)] for row in range(maze_info["height"]**2)] #creates empty adjacency matrix - 2D array. Number of rows/columns is total number of cells in maze.
        #adjacency matrix will be updated with shortest routes between cells as they are calculated by the A* algorithm.

    #level_loop method contains the loop that repeats for the whole level. Once this ends, the program returns to GameHandler's main game loop.
    def level_loop(self) -> bool:
        while self.__exit_level == False:
            self.__user_move() #let user move
            self.__enemy_move() #calculate enemy moves and move them
            self.__check_game_state() #check if player has won or lost and take relevant action

    #runs when it is the user's turn.
    def __user_move(self):
        user_turn = True
        while user_turn == True: #runs until player chooses to quit the game (presses X on window), or has moved the character.
            for event in pygame.event.get(): #run through all pygame events since last checked.
                if event.type == pygame.QUIT: #if user clicks close button, set user_turn to False and __exit_level to True to escape level loop. Run GameHandler's save_and_quit method, closing program.
                    self.__parent.save_and_quit()
                    user_turn = False
                    self.__exit_level = True
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        self.__player.enter_move((-1,0)) #Coordinate/vector for left.
                    elif event.key in (pygame.K_w, pygame.K_UP):
                        self.__player.enter_move((0,-1))
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.__player.enter_move((1,0))
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        self.__player.enter_move((0,1))
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if self.__player.move_player() == True: #__player.move_player() returns True if player has entered a valid direction and has been moved. If not, returns False and we keep checking for inputs.
                            user_turn = False #user has moved, so now enemies' moves.
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.__level_gui["btn_pause"]:
                        self.pause()
                
                self.__gui_handler.process_events(event)
            
            self.__gui_handler.update(1/60)

            self.__canvas.fill((0,0,0)) #clear the screen
            self.__maze.draw_maze() #redraw the maze
            self.__draw_entities() #draw enemies and player

            self.__gui_handler.draw_ui()

            pygame.display.update() #updates the window with any changes.

    #manages all of the tasks that need to be won 
    def __enemy_move(self):
        for enemy in self.__enemies: 
            if self.__exit_level == False: #only moves enemy if we aren't ending level. Only True if user has pressed screen's X button during user turn or enemy turn.
                enemy.make_calculated_move()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT: #if user clicks screen's X button, set __exit_level to True to escape level loop. Run GameHandler's save_and_quit method, closing program.
                        self.__parent.save_and_quit()
                        self.__exit_level = True
                    if event.type == pygame.KEYDOWN:
                        pass #will add pause functionality at later point
        
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.__level_gui["btn_pause"]:
                            print('Pause!')
                            self.__level_gui["btn_pause"].hide()
                    
                    self.__gui_handler.process_events(event)

        self.__gui_handler.update(1/60)

        self.__canvas.fill((0,0,0)) #clear screen
        self.__maze.draw_maze() #redraw the maze
        self.__draw_entities() #draw enemies and player
        self.__gui_handler.draw_ui()
        pygame.display.update() #updates the window with any changes.

    #pause method - draws pause screen etc.
    def pause(self):
        self.__level_gui["panel"].hide()
        self.__pause_menu_gui["panel"].show()

    #__check_game_state() - checks if user has lost or won and calls the relevant method.
    def __check_game_state(self) -> None:
        if self.__check_game_loss() == True:
            self.__game_over()
        elif self.__check_game_win() == True:
            self.__game_win()

    #__check_game_loss() - checks if user has same position in maze as any of the enemies.
    def __check_game_loss(self) -> bool:
        player_pos, enemy_poses = self.get_entity_positions()
        return player_pos in enemy_poses

    #__check_game_win() - checks if user's maze position is the same as the finish square.
    def __check_game_win(self) -> bool:
        player_pos, _ = self.get_entity_positions()
        finish_coord = self.__maze.get_finish_coord()
        return player_pos == finish_coord

    #__game_over() - will display game over method, sets __exit_level to false so that level loop ends, and will give user option to replay the same level.
    def __game_over(self) -> bool:
        print("Game Over!")
        self.__exit_level = True

    #__game_win() - will display game won method, sets __exit_level to false so that level loop ends, and will give user option to replay the same level.
    def __game_win(self) -> bool:
        print("Game Won!")
        self.__exit_level = True

    #__find_cell_adj_mat_index() - turns the coordinate tuple representing a position in the maze into a single number representing that cell's index in the adjacency matrix.
    #maze_pos is the coordinate of the cell in the maze that you want the index in the adjacency matrix of.
    def __find_cell_adj_mat_index(self, maze_pos: tuple):
        maze_height = self.get_maze_cell_height()
        ind = maze_pos[1]*maze_height + maze_pos[0] #index tarts with top left cell as 0 and then increases along the rows.
        return ind

    #get_route_between_cells() - returns the shortest route between 2 cells stored in the adjacency matrix - tuple of tuples of coords, or None if route never been calculated
    #start and dest are tuples of coordinates to find the route between.
    def get_route_between_cells(self, start: tuple, dest: tuple) -> None|tuple:
        start_ind = self.__find_cell_adj_mat_index(start)
        dest_ind = self.__find_cell_adj_mat_index(dest)
        route = self.__route_adj_mat[start_ind][dest_ind]
        return route

    #set_route_between_cells() - if the provided route is shorter that the current stored one, store the new route.
    #start and dest are tuples of coords to store route between, and route is a tuple of tuples storing coords along the route as tuples, not including start or dest.
    def set_route_between_cells(self, start: tuple, dest: tuple, route: tuple):
        current_route = self.get_route_between_cells(start, dest)
        current_route_length = float("inf") if current_route == None else len(current_route) #get the length of the current route (set to infinite if no route so that all routes are shorter.)
        start_ind = self.__find_cell_adj_mat_index(start)
        dest_ind = self.__find_cell_adj_mat_index(dest)
        if len(route) < current_route_length: #if new route is shorter.
            self.__route_adj_mat[start_ind][dest_ind] = route #add route from start to dest
            self.__route_adj_mat[dest_ind][start_ind] = route[::-1] #route from dest to start is the reversed route.

    #get_player() - returns the level handler's player object
    def get_player(self) -> Player:
        return self.__player
    
    #get_enemies() - returns a list of the level handler's Enemy objects
    def get_enemies(self) -> list:
        return self.__enemies
    
    #get_maze_cell_height() - returns level handler's maze height in terms of number of cells.
    def get_maze_cell_height(self) -> int:
        return self.__MAZE_CELL_HEIGHT

    #get_entity_positions() - returns a tuple representing the current maze coord of the player and a list of tuple coordinates representing the current maze coords of the enemies.
    def get_entity_positions(self) -> tuple|list:
        player_pos = self.__player.get_maze_pos()
        enemy_poses = [enemy.get_maze_pos() for enemy in self.__enemies]
        return player_pos, enemy_poses
    
    #get_maze() - returns level handler's maze object
    def get_maze(self) -> Maze:
        return self.__maze
    
    def get_gui_handler(self):
        return self.__gui_handler
    
    #__draw_entities() - draws player, and then draws enemy.
    def __draw_entities(self) -> None:
        self.__player.draw_entity()
        for enemy in self.__enemies:
            enemy.draw_entity()