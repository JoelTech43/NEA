from Maze import Maze
from Enemy import Enemy
from Player import Player
from Timer import Timer
import pygame
import pygame_gui
import json

class LevelHandler:
    #__init__ method:
    #parent is object that instantiated this object, GameHandler in this case.
    #level_id is an integer what maze is to be loaded.
    def __init__(self, parent, level_id: int) -> None:
        self.__parent = parent
        self.__level_id = level_id
        self.__gui_handler = self.__parent.get_gui_handler() #get GUIHandler from GameHandler
        self.__canvas = self.__gui_handler.get_canvas()
        self.__level_gui = self.__gui_handler.get_level_panel()
        self.__pause_menu_gui = self.__gui_handler.get_pause_menu_panel()
        self.__settings_menu_gui = self.__gui_handler.get_settings_menu_panel()
        self.__endgame_gui = self.__gui_handler.get_endgame_panel()

        self.__music_handler = self.__parent.get_music_handler() #get MusicHandler from GameHandler

        self.__settings_handler = self.__parent.get_settings_handler() #get SettingsHandler from GameHandler

        maze_info = self.__load_maze() #load the current maze

        self.__CELL_HEIGHT = self.__gui_handler.get_maze_screen_height()//maze_info["height"] #calculates cell height in pixels by dividing the height of the maze in pixels by number of cells in a column.
        self.__collectibles_coords = list(tuple(coord) for coord in maze_info["collectibles"])
        self.__maze = Maze(self, maze_info["maze"], maze_info["height"], self.__CELL_HEIGHT, self.__gui_handler.get_maze_screen_pos(), tuple(maze_info["finish"]), tuple(self.__collectibles_coords)) 
        self.__player = Player(self, 1, maze_info["player"], self.__CELL_HEIGHT)
        self.__enemies = [Enemy(self, 1, pos, self.__CELL_HEIGHT) for pos in maze_info["enemies"]] #instantiates all needed Enemy objects and stores them in a list.
        self.__MAZE_CELL_HEIGHT = maze_info["height"]
        
        self.__level_timed = maze_info["time"] > 0 #if maze info's time value is greater than 0 then there is a time constraint.
        self.__level_timer = Timer(self, maze_info["time"], self.__level_timed) #instantiate Timer object.

        self.__exit_level = False #level_loop runs until this is True
        self.__paused = False

        self.__collectibles_collected = 0
        self.__level_success = False
        self.__replay = False

        self.__route_adj_mat = [[None for cell in range(maze_info["height"]**2)] for row in range(maze_info["height"]**2)] #creates empty adjacency matrix - 2D array. Number of rows/columns is total number of cells in maze.
        #adjacency matrix will be updated with shortest routes between cells as they are calculated by the A* algorithm.

    def __load_maze(self):
        with open(f"level_{self.__level_id}.json", "r") as f: #loads maze file. File depends on level_id. Stored as a dictionary using the json module.
            maze_data = json.load(f)
        
        return maze_data

    #level_loop method contains the loop that repeats for the whole level. Once this ends, the program returns to GameHandler's main game loop.
    def level_loop(self) -> tuple:
        self.__update_level_gui_text() #updates the Level GUI text showing time remaining and collectibles collected
        self.__level_gui["panel"].show() #shows Level GUI.
        while self.__exit_level == False:
            self.__music_handler.play_action_music()
            self.__user_move() #let user move
            self.__enemy_move() #calculate enemy moves and move them
            self.__check_game_state() #check if player has won or lost and take relevant action
        self.__level_gui["panel"].hide()
        self.__music_handler.play_menu_music()
        return self.__collectibles_collected, self.__level_success, self.__replay

    #runs when it is the user's turn.
    def __user_move(self):
        user_turn = True
        while user_turn == True and self.__exit_level == False: #runs until player chooses to quit the game (presses X on window), or has moved the character.
            for event in pygame.event.get(): #run through all pygame events since last checked.
                if event.type == pygame.QUIT: #if user clicks close button, set user_turn to False and __exit_level to True to escape level loop. Run GameHandler's save_and_quit method, closing program.
                    self.__music_handler.play_sfx_click()
                    self.__parent.save_and_quit()
                    user_turn = False
                    self.__exit_level = True
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        self.__music_handler.play_sfx_click()
                        self.__player.enter_move((-1,0)) #Coordinate/vector for left.
                    elif event.key in (pygame.K_w, pygame.K_UP):
                        self.__music_handler.play_sfx_click()
                        self.__player.enter_move((0,-1)) #Coordinate for up.
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.__music_handler.play_sfx_click()
                        self.__player.enter_move((1,0)) #Coordinate for right.
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        self.__music_handler.play_sfx_click()
                        self.__player.enter_move((0,1)) #Coordinate for down.
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if self.__player.move_player() == True: #__player.move_player() returns True if player has entered a valid direction and has been moved. If not, returns False and we keep checking for inputs.
                            self.__music_handler.play_sfx_click()
                            user_turn = False #user has moved, so now enemies' moves.
                        else:
                            self.__music_handler.play_sfx_error()
                    elif event.key == pygame.K_ESCAPE: #if Esc key pressed, pause game.
                        self.__music_handler.play_sfx_click()
                        self.__pause()
                    else:
                        self.__music_handler.play_sfx_error()
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.__level_gui["btn_pause"]: #if onscreen pause button pressed, pause game
                        self.__music_handler.play_sfx_click()
                        self.__pause()
                
                self.__gui_handler.process_events(event)
            
            self.__gui_handler.update(1/60)

            if self.__level_timed == True:
                if self.__level_timer.check_finished() == True: #if level is timed and timer has reached 0, game over.
                    user_turn = False
                self.__update_level_gui_text()

            self.__canvas.fill(self.__settings_handler.get_bg_col()) #clear the screen
            self.__maze.draw_maze() #redraw the maze
            self.__draw_entities() #draw enemies and player

            self.__gui_handler.draw_ui()

            pygame.display.update() #updates the window with any changes.
        
        self.__check_on_collectible()

    #manages all of the tasks that need to be won 
    def __enemy_move(self):
        for enemy in self.__enemies: 
            if self.__exit_level == False: #only moves enemy if we aren't ending level. Only True if user has pressed screen's X button during user turn or enemy turn.
                enemy.make_calculated_move()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT: #if user clicks screen's X button, set __exit_level to True to escape level loop. Run GameHandler's save_and_quit method, closing program.
                        self.__music_handler.play_sfx_click()
                        self.__parent.save_and_quit()
                        self.__exit_level = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE: #if Esc key pressed, pause game
                            self.__music_handler.play_sfx_click()
                            self.__pause()
                        else:
                            self.__music_handler.play_sfx_error()
        
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.__level_gui["btn_pause"]: #if onscreen pause button pressed, pause game.
                            self.__music_handler.play_sfx_click()
                            self.__pause()
                    
                    self.__gui_handler.process_events(event)

        self.__gui_handler.update(1/60)

        self.__canvas.fill(self.__settings_handler.get_bg_col()) #clear screen
        self.__maze.draw_maze() #redraw the maze
        self.__draw_entities() #draw enemies and player
        self.__gui_handler.draw_ui()
        pygame.display.update() #updates the window with any changes.

    #pause method - draws pause screen etc.
    def __pause(self):
        self.__level_timer.pause_timer() #pause timer
        self.__level_gui["panel"].hide() #hide level GUI and show Pause Menu GUI
        self.__pause_menu_gui["panel"].show()
        self.__paused = True

        volume_changed = False
        while self.__paused == True:
            self.__music_handler.play_menu_music()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #if user clicks screen's X button, set __exit_level to True to escape level loop. Run GameHandler's save_and_quit method, closing program.
                    self.__music_handler.play_sfx_click()
                    self.__parent.save_and_quit()
                    self.__exit_level = True
                    self.__paused = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: #if Esc key pressed, close pause menu by setting paused to False
                        self.__music_handler.play_sfx_click()
                        self.__paused = False
                    else:
                        self.__music_handler.play_sfx_error()

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.__pause_menu_gui["btn_resume"]: #if 
                        self.__music_handler.play_sfx_click()
                        self.__paused = False
                    
                    elif event.ui_element == self.__pause_menu_gui["btn_pause_settings"]:
                        self.__music_handler.play_sfx_click()
                        self.__settings_menu()
                    
                    elif event.ui_element == self.__pause_menu_gui["btn_restart"]:
                        self.__music_handler.play_sfx_click()
                        self.__exit_level = True
                        self.__replay = True
                        self.__paused = False
                        self.__pause_menu_gui["panel"].hide()
                        self.__level_gui["panel"].show()
                    
                    elif event.ui_element == self.__pause_menu_gui["btn_quit_level"]:
                        self.__music_handler.play_sfx_click()
                        self.__paused = False
                        self.__exit_level = True
                
                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.__pause_menu_gui["slider_pause_bg_volume"]:
                        volume_changed = True
                        self.__settings_handler.set_bg_volume(event.value)
                        self.__music_handler.set_background_volume(event.value)
                    
                    elif event.ui_element == self.__pause_menu_gui["slider_pause_sfx_volume"]:
                        volume_changed = True
                        self.__settings_handler.set_sfx_volume(event.value)
                        self.__music_handler.set_sfx_volume(event.value)
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    if volume_changed == True:
                        volume_changed = False
                        self.__music_handler.play_sfx_click()
                        self.__gui_handler.update_slider_values()
                
                self.__gui_handler.process_events(event)
            
            self.__gui_handler.update_settings_text()

            self.__gui_handler.update(1/60)

            self.__canvas.fill(self.__settings_handler.get_bg_col()) #clear screen
            
            self.__gui_handler.draw_ui()
            pygame.display.update() #updates the window with any changes.
        
        self.__pause_menu_gui["panel"].hide()
        self.__level_gui["panel"].show()
        self.__music_handler.play_action_music()
        self.__level_timer.resume_timer()

    def __settings_menu(self):
        self.__pause_menu_gui["panel"].hide() #hide Pause menu GUI and show Settings GUI
        self.__settings_menu_gui["panel"].show()

        current_settings = self.__settings_handler.get_settings() #get current settings

        settings_open = True
        colour_changed = False
        volume_changed = False
        while settings_open == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #if user clicks screen's X button, set __exit_level to True to escape level loop. Run GameHandler's save_and_quit method, closing program.
                    self.__music_handler.play_sfx_click()
                    self.__parent.save_and_quit()
                    self.__exit_level = True
                    self.__paused = False #set paused and settings open to False to close settings and pause menus.
                    settings_open = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: #If press Esc, return to Pause menu.
                        self.__music_handler.play_sfx_click()
                        settings_open = False
                    else:
                        self.__music_handler.play_sfx_error()

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.__settings_menu_gui["btn_exit_settings"]: #If press onscreen exit settings button, return to Pause Menu
                        self.__music_handler.play_sfx_click()
                        settings_open = False
                    
                    elif event.ui_element == self.__settings_menu_gui["btn_light_theme"]: #If press onscreen light theme button, set the colour scheme to the light theme and reload all UI elements.
                        self.__music_handler.play_sfx_click()
                        self.__settings_handler.set_light_theme()
                        self.__reload_theme("settings_menu")
                    
                    elif event.ui_element == self.__settings_menu_gui["btn_light_hc_theme"]: #If press onscreen light contrast theme button, set the colour scheme to the light contrast theme and reload all UI elements.
                        self.__music_handler.play_sfx_click()
                        self.__settings_handler.set_light_hc_theme()
                        self.__reload_theme("settings_menu")
                    
                    elif event.ui_element == self.__settings_menu_gui["btn_dark_theme"]: #If press onscreen dark theme button, set the colour scheme to the dark theme and reload all UI elements.
                        self.__music_handler.play_sfx_click()
                        self.__settings_handler.set_dark_theme()
                        self.__reload_theme("settings_menu")
                    
                    elif event.ui_element == self.__settings_menu_gui["btn_dark_hc_theme"]: #If press onscreen dark contrast theme button, set the colour scheme to the dark contrast theme and reload all UI elements.
                        self.__music_handler.play_sfx_click()
                        self.__settings_handler.set_dark_hc_theme()
                        self.__reload_theme("settings_menu")
                
                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.__settings_menu_gui["slider_settings_bg_volume"]: #if background volume slider moved, adjust the background volume.
                        volume_changed = True
                        self.__settings_handler.set_bg_volume(event.value)
                        self.__music_handler.set_background_volume(event.value)
                    
                    elif event.ui_element == self.__settings_menu_gui["slider_settings_sfx_volume"]: #if sfx volume slider moved, adjust the sfx volume.
                        volume_changed = True
                        self.__settings_handler.set_sfx_volume(event.value)
                        self.__music_handler.set_sfx_volume(event.value)
                    
                    elif event.ui_element == self.__settings_menu_gui["slider_red_level"]: #if red colour slider moved, set colour_changed to True to deal with theme when released.
                        colour_changed = True
                    
                    elif event.ui_element == self.__settings_menu_gui["slider_green_level"]: #if green colour slider moved, set colour_changed to True to deal with theme when released.
                        colour_changed = True
                    
                    elif event.ui_element == self.__settings_menu_gui["slider_blue_level"]: #if blue colour slider moved, set colour_changed to True to deal with theme when released.
                        colour_changed = True
                
                elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED: #if drop down menu used, set the current theme item to the selected item, and reload theme to change coloured rect colour.
                    if event.ui_element == self.__settings_menu_gui["drop_theme_section"]:
                        self.__music_handler.play_sfx_click()
                        match event.text:
                            case "Background":
                                current_settings["selected_item"] = "bg_col"
                            
                            case "Text/Walls":
                                current_settings["selected_item"] = "wall_col"
                            
                            case "Buttons":
                                current_settings["selected_item"] = "btn_col"
                            
                            case "Highlights":
                                current_settings["selected_item"] = "highlight_col"
                            
                            case "Player":
                                current_settings["selected_item"] = "player_col"
                            
                            case "Enemy":
                                current_settings["selected_item"] = "enemy_col"
                            
                        self.__settings_handler.set_settings(current_settings)
                        self.__reload_theme("settings_menu")
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if colour_changed == True: #if the mouse is released and colour_changed, the theme sliders must have been released. Reset colour_changed, and update theme and settings.
                        colour_changed = False
                        self.__music_handler.play_sfx_click()
                        rgb_r_value = int((self.__settings_menu_gui["slider_red_level"].get_current_value()/100)*255)
                        rgb_g_value = int((self.__settings_menu_gui["slider_green_level"].get_current_value()/100)*255)
                        rgb_b_value = int((self.__settings_menu_gui["slider_blue_level"].get_current_value()/100)*255)

                        current_settings[current_settings["selected_item"]] = (rgb_r_value, rgb_g_value, rgb_b_value)
                        self.__settings_handler.set_settings(current_settings)
                        self.__reload_theme("settings_menu")
                    
                    if volume_changed == True: #if mouse released and volume_changed, volume slider must have been released. Reset colour_changed and update the text above the sliders.
                        volume_changed = False
                        self.__music_handler.play_sfx_click()
                        self.__gui_handler.update_slider_values()

                
                self.__gui_handler.process_events(event)
            
            self.__gui_handler.update_settings_text()

            self.__gui_handler.update(1/60)

            self.__canvas.fill(self.__settings_handler.get_bg_col()) #clear screen
            
            self.__gui_handler.draw_ui()
            pygame.display.update() #updates the window with any changes.
        
        self.__settings_menu_gui["panel"].hide()
        self.__pause_menu_gui["panel"].show()

    def __reload_theme(self, current_screen):
        self.__gui_handler.reload_theme(current_screen) #reloads the theme by destroying all pygame_gui UI elements and recreating them with the new theme. Current screen ensures correct screen shown.
        self.__player.update_colour() #update the Player colour as has already been initialised.
        for enemy in self.__enemies:
            enemy.update_colour() #update the Enemy colour as has already been initialised.
        
        self.__level_gui = self.__gui_handler.get_level_panel() #refetch all the UI element dictionaries needed by LevelHandler from GUIHandler to use the new UI elements.
        self.__pause_menu_gui = self.__gui_handler.get_pause_menu_panel()
        self.__settings_menu_gui = self.__gui_handler.get_settings_menu_panel()
        self.__endgame_gui = self.__gui_handler.get_endgame_panel()

        self.__parent.reload_elements() #refetch all the UI element dictionaries needed by GameHandler in GameHandler.

    #__check_game_state() - checks if user has lost or won and calls the relevant method.
    def __check_game_state(self) -> None:
        if self.__check_game_loss() == True:
            self.__replay = self.__game_over()
        elif self.__check_game_win() == True:
            self.__level_success = True
            self.__replay = self.__game_win()

    #__check_game_loss() - checks if user has same position in maze as any of the enemies.
    def __check_game_loss(self) -> bool:
        player_pos, enemy_poses = self.get_entity_positions()
        return player_pos in enemy_poses

    #__check_game_win() - checks if user's maze position is the same as the finish square.
    def __check_game_win(self) -> bool:
        player_pos, _ = self.get_entity_positions()
        finish_coord = self.__maze.get_finish_coord()
        return player_pos == finish_coord

    #__check_game_win() - checks if player is currently on a collectible.
    def __check_on_collectible(self) -> None:
        player_pos, _ = self.get_entity_positions()

        if player_pos in self.__collectibles_coords: #if player's coord is in the list of collectible coords
            self.__maze.remove_collectible(player_pos) #remove collectible from maze.
            self.__collectibles_coords.remove(player_pos) #remove collectible from LevelHandler's collectibles list.
            self.__collectibles_collected += 1 #increment the player's level collectible counter.
            self.__music_handler.play_sfx_collectible()
            self.__update_level_gui_text() #update the level GUI text.

    #__game_over() - will display game over method, sets __exit_level to false so that level loop ends, and will give user option to replay the same level.
    def __game_over(self) -> bool:
        self.__music_handler.play_sfx_death()
        self.__music_handler.stop_bg_music()
        self.__endgame_gui["txt_endgame_title"].set_text("Game Over!") #Set the title text to the appropriate method.
        self.__level_gui["panel"].hide()
        self.__endgame_gui["panel"].show()
        replay = False
        self.__exit_level = True
        exit_screen = False
        while exit_screen == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #if user clicks screen's X button, set __exit_level to True to escape level loop. Run GameHandler's save_and_quit method, closing program.
                    self.__music_handler.play_sfx_click()
                    self.__parent.save_and_quit()
                    self.__exit_level = True
                    self.__paused = False
                    exit_screen = True

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.__endgame_gui["btn_return"]: #If return to main menu button pressed, exit the game over screen. Default variables mean success is False and replay is False.
                        self.__music_handler.play_sfx_click()
                        exit_screen = True
                    
                    elif event.ui_element == self.__endgame_gui["btn_replay"]: #If replat button pressed, exit the game over screen. Set replay to True so that GameHandler will replay the level.
                        self.__music_handler.play_sfx_click()
                        replay = True
                        exit_screen = True
                
                elif event.type == pygame.KEYDOWN:
                    self.__music_handler.play_sfx_error()
                
                self.__gui_handler.process_events(event)
            
            self.__gui_handler.update(1/60)

            self.__canvas.fill(self.__settings_handler.get_bg_col()) #clear screen
            
            self.__gui_handler.draw_ui()
            pygame.display.update() #updates the window with any changes.

        self.__endgame_gui["panel"].hide()
        self.__level_gui["panel"].hide()
        return replay

    #__game_win() - will display game won method, sets __exit_level to false so that level loop ends, and will give user option to replay the same level.
    def __game_win(self) -> bool:
        self.__music_handler.play_sfx_success()
        self.__music_handler.stop_bg_music()
        self.__endgame_gui["txt_endgame_title"].set_text("Level Complete!") #set title text to appropriate message.
        self.__level_gui["panel"].hide()
        self.__endgame_gui["panel"].show()
        replay = False
        self.__exit_level = True
        exit_screen = False
        while exit_screen == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #if user clicks screen's X button, set __exit_level to True to escape level loop. Run GameHandler's save_and_quit method, closing program.
                    self.__music_handler.play_sfx_click()
                    self.__parent.save_and_quit()
                    self.__exit_level = True
                    self.__paused = False
                    exit_screen = True

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.__endgame_gui["btn_return"]: #If return to main menu button pressed, exit game win screen. Success has been set to True and replay is False so go to Main Menu.
                        self.__music_handler.play_sfx_click()
                        exit_screen = True
                    
                    elif event.ui_element == self.__endgame_gui["btn_replay"]: #If replay button pressed, exit game win screen. Success has been set to True, and replay is now set to True.
                        self.__music_handler.play_sfx_click()
                        replay = True
                        exit_screen = True
                
                elif event.type == pygame.KEYDOWN:
                    self.__music_handler.play_sfx_error()
                
                self.__gui_handler.process_events(event)
            
            self.__gui_handler.update(1/60)

            self.__canvas.fill(self.__settings_handler.get_bg_col()) #clear screen
            
            self.__gui_handler.draw_ui()
            pygame.display.update() #updates the window with any changes.

        self.__endgame_gui["panel"].hide()
        self.__level_gui["panel"].hide()
        return replay

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
        enemy_poses = [tuple(enemy.get_maze_pos()) for enemy in self.__enemies]
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
    
    #__update_level_gui_text() - changes the pygame_gui labels to reflect the current time remaining and collectibles collected.
    def __update_level_gui_text(self) -> None:
        self.__level_gui["txt_collectibles_collected"].set_text(f"Collectibles Collected: {self.__collectibles_collected}/3")
        mins, secs = self.__level_timer.get_minute_second_time_left()
        self.__level_gui["txt_time_remaining"].set_text(f"Time Remaining: {mins}:{secs}")
    
    def get_settings_handler(self):
        return self.__settings_handler