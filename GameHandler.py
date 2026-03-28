import pygame
import pygame_gui
from LevelHandler import LevelHandler #importing my LevelHandler class
from GUIHandler import GUIHandler
from MusicHandler import MusicHandler
from SettingsHandler import SettingsHandler
from time import time
import json

class GameHandler:
    def __init__(self):
        pygame.init() #initialises pygame. Necessary to use pygame functions.

        self.__settings_handler = SettingsHandler() #instantiate SettingsHandler
        self.__gui_handler = GUIHandler(self) #instantiate GUIHandler
        self.__canvas = self.__gui_handler.get_canvas()
        self.__main_menu_gui = self.__gui_handler.get_main_menu_panel()
        self.__settings_menu_gui = self.__gui_handler.get_settings_menu_panel()
        

        self.__music_handler = MusicHandler() #instantiate MusicHandler
        self.__music_handler.set_background_volume(self.__settings_handler.get_bg_volume()) #set sound volumes to current values in settings.
        self.__music_handler.set_sfx_volume(self.__settings_handler.get_sfx_volume())

        try: #attempt to load save data file and store as dictionary
            with open("user_data.json", "r") as f:
                self.__user_data = json.load(f)
        
        except FileNotFoundError: #if not save file exists, create new user data dictionary.
            self.__user_data = {"current_level": 1, "total_collectibles": 0}

        self.__running = True #while True, game loop runs.

    #main_game_loop is the method that contains the main game loop. When this method ends, so does the game.
    def main_game_loop(self):
        quit_pressed = float("inf") #variable for tracking how long Esc key held for.
        while self.__running == True:
            self.__update_gui_text()
            self.__music_handler.play_menu_music()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #If window closed, save user data and settings before closing.
                    self.__music_handler.play_sfx_click()
                    self.save_and_quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: #when Esc pressed, record the time.
                        self.__music_handler.play_sfx_click()
                        quit_pressed = time()
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE): #if Enter or Space pressed, play the next level.
                        self.__music_handler.play_sfx_click()
                        self.__play_level()
                    
                    else:
                        self.__music_handler.play_sfx_error()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE: #when Esc key released, if it has been held for over 3 seconds, save user data and settings before closing game.
                        if time()-quit_pressed > 3:
                            self.__music_handler.play_sfx_click()
                            self.save_and_quit()
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.__main_menu_gui["btn_play_level"]: #if onscreen play button pressed, play level.
                        self.__music_handler.play_sfx_click()
                        self.__play_level()
                    elif event.ui_element == self.__main_menu_gui["btn_settings"]: #if onscreen settings button pressed, open settings.
                        self.__music_handler.play_sfx_click()
                        quit_pressed = float("inf")
                        self.__settings_menu()
                    elif event.ui_element == self.__main_menu_gui["btn_quit"]: #if onscreen quit button pressed, save user data and settings before closing game.
                        self.__music_handler.play_sfx_click()
                        self.save_and_quit()
                
                self.__gui_handler.process_events(event)
            
            self.__gui_handler.update(1/60)

            self.__canvas.fill(self.__settings_handler.get_bg_col()) #clear window.
            self.__gui_handler.draw_ui()#redraw GUI.

            pygame.display.update()

    #settings_menu method creates settings menu over current screen, adjusts settings, and then closes, returning the user back to where they were.
    def __settings_menu(self):
        self.__main_menu_gui["panel"].hide() #hide main menu GUI and show settings menu GUI
        self.__settings_menu_gui["panel"].show()

        current_settings = self.__settings_handler.get_settings() #get settings from SettingsHandler

        settings_open = True
        colour_changed = False
        volume_changed = False
        while settings_open == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #if user clicks screen's X button, set __exit_level to True to escape level loop. Run GameHandler's save_and_quit method, closing program.
                    self.__music_handler.play_sfx_click()
                    self.save_and_quit()
                    settings_open = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: #If press Esc, return to Main menu
                        self.__music_handler.play_sfx_click()
                        settings_open = False
                    else:
                        self.__music_handler.play_sfx_error()

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.__settings_menu_gui["btn_exit_settings"]: #If press onscreen exit settings button, return to Main Menu
                        self.__music_handler.play_sfx_click()
                        settings_open = False
                    
                    elif event.ui_element == self.__settings_menu_gui["btn_light_theme"]: #If press onscreen light theme button, set the colour scheme to the light theme and reload all UI elements.
                        self.__music_handler.play_sfx_click()
                        self.__settings_handler.set_light_theme()
                        self.__reload_theme("settings_menu")
                    
                    elif event.ui_element == self.__settings_menu_gui["btn_light_hc_theme"]: #If press onscreen light contrast theme button, set the colour scheme to the light contrast theme.
                        self.__music_handler.play_sfx_click()
                        self.__settings_handler.set_light_hc_theme()
                        self.__reload_theme("settings_menu")
                    
                    elif event.ui_element == self.__settings_menu_gui["btn_dark_theme"]: #If press onscreen dark theme button, set the colour scheme to the dark theme and reload all UI elements.
                        self.__music_handler.play_sfx_click()
                        self.__settings_handler.set_dark_theme()
                        self.__reload_theme("settings_menu")
                    
                    elif event.ui_element == self.__settings_menu_gui["btn_dark_hc_theme"]: #If press onscreen dark contrast theme button, set the colour scheme to the dark contrast theme.
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
                        self.__music_handler.play_sfx_click()
                        colour_changed = False
                        rgb_r_value = int((self.__settings_menu_gui["slider_red_level"].get_current_value()/100)*255)
                        rgb_g_value = int((self.__settings_menu_gui["slider_green_level"].get_current_value()/100)*255)
                        rgb_b_value = int((self.__settings_menu_gui["slider_blue_level"].get_current_value()/100)*255)

                        current_settings[current_settings["selected_item"]] = (rgb_r_value, rgb_g_value, rgb_b_value)
                        self.__settings_handler.set_settings(current_settings)
                        self.__reload_theme("settings_menu")
                    
                    if volume_changed == True: #if mouse released and volume_changed, volume slider must have been released. Reset colour_changed and update the text above the sliders.
                        self.__music_handler.play_sfx_click()
                        self.__gui_handler.update_slider_values()

                
                self.__gui_handler.process_events(event)
            
            self.__gui_handler.update_settings_text()

            self.__gui_handler.update(1/60)

            self.__canvas.fill(self.__settings_handler.get_bg_col()) #clear screen
            
            self.__gui_handler.draw_ui()
            pygame.display.update() #updates the window with any changes.
        
        self.__settings_menu_gui["panel"].hide()
        self.__main_menu_gui["panel"].show()

    #__play_level method instantiates the LevelHandler to play a specific level.
    #level_id is an integer representing what level is to be loaded.
    def __play_level(self):
        self.__main_menu_gui["panel"].hide() #hide Main Menu GUI

        replay = True
        while replay == True:
            level_handler = LevelHandler(self, self.__user_data["current_level"]) #instantiate LevelHandler
            collectibles, success, replay = level_handler.level_loop() #run the main level_handler loop. returns a boolean of whether the user would like to play the level again.
            if success == True:
                self.__user_data["total_collectibles"] += collectibles #if player completed level, add collectibles to their total.
        if success == True and self.__user_data["current_level"] < 3: #if player completed level and not at max level, add one to their current level.
            self.__user_data["current_level"] += 1
        
        self.__main_menu_gui["panel"].show() #show main menu GUI

    def save_and_quit(self):
        with open("user_data.json", "w") as f: #save user data dict in JSON format
            json.dump(self.__user_data, f)
        self.__settings_handler.save_settings() #save settings
        self.__running = False #exit main_game_loop closing game.
    
    def get_gui_handler(self):
        return self.__gui_handler
    
    def get_music_handler(self):
        return self.__music_handler
    
    def get_settings_handler(self):
        return self.__settings_handler

    def __update_gui_text(self): #updates the collectibles and current level text on the homescreen to match the user_data dict.
        self.__main_menu_gui["txt_collectibles"].set_text(f"Collectibles Collected: {self.__user_data["total_collectibles"]}")
        self.__main_menu_gui["txt_level"].set_text(f"Current Level: {self.__user_data["current_level"]}")
    
    def reload_elements(self): #fetches the dicts containing UI elements from SettingsHandler after theme changed.
        self.__main_menu_gui = self.__gui_handler.get_main_menu_panel()
        self.__settings_menu_gui = self.__gui_handler.get_settings_menu_panel()
    
    def __reload_theme(self, current_screen): #changes theme and then refetches all the UI element dicts.
        self.__gui_handler.reload_theme(current_screen)
        self.reload_elements()