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

        self.__settings_handler = SettingsHandler()
        self.__gui_handler = GUIHandler(self)
        self.__canvas = self.__gui_handler.get_canvas()
        self.__main_menu_gui = self.__gui_handler.get_main_menu_panel()
        self.__settings_menu_gui = self.__gui_handler.get_settings_menu_panel()
        

        self.__music_handler = MusicHandler()
        self.__music_handler.set_background_volume(self.__settings_handler.get_bg_volume())
        self.__music_handler.set_sfx_volume(self.__settings_handler.get_sfx_volume())

        try:
            with open("user_data.json", "r") as f:
                self.__user_data = json.load(f)
        
        except FileNotFoundError:
            self.__user_data = {"current_level": 1, "total_collectibles": 0}

        self.__running = True #while True, game loop runs.

    #main_game_loop is the method that contains the main game loop. When this method ends, so does the game.
    def main_game_loop(self):
        self.__update_gui_text()
        quit_pressed = 0
        while self.__running == True:
            self.__music_handler.play_menu_music()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__music_handler.play_sfx_click()
                    self.save_and_quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__music_handler.play_sfx_click()
                        quit_pressed = time()
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.__music_handler.play_sfx_click()
                        self.__play_level()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        if time()-quit_pressed > 3:
                            self.__music_handler.play_sfx_click()
                            self.save_and_quit()
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.__main_menu_gui["btn_play_level"]:
                        self.__music_handler.play_sfx_click()
                        self.__play_level()
                    elif event.ui_element == self.__main_menu_gui["btn_settings"]:
                        self.__music_handler.play_sfx_click()
                        self.settings_menu()
                    elif event.ui_element == self.__main_menu_gui["btn_quit"]:
                        self.__music_handler.play_sfx_click()
                        self.save_and_quit()
                
                self.__gui_handler.process_events(event)
            
            self.__gui_handler.update(1/60)

            self.__canvas.fill(self.__settings_handler.get_bg_col())
            self.__gui_handler.draw_ui()

            pygame.display.update()

    #settings_menu method creates settings menu over current screen, adjusts settings, and then closes, returning the user back to where they were.
    def settings_menu(self):
        self.__main_menu_gui["panel"].hide()
        self.__settings_menu_gui["panel"].show()

        settings_open = True
        while settings_open == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #if user clicks screen's X button, set __exit_level to True to escape level loop. Run GameHandler's save_and_quit method, closing program.
                    self.save_and_quit()
                    settings_open = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__music_handler.play_sfx_click()
                        settings_open = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.__settings_menu_gui["btn_exit_settings"]:
                        self.__music_handler.play_sfx_click()
                        settings_open = False
                
                self.__gui_handler.process_events(event)
            
            self.__gui_handler.update(1/60)

            self.__canvas.fill(self.__settings_handler.get_bg_col()) #clear screen
            
            self.__gui_handler.draw_ui()
            pygame.display.update() #updates the window with any changes.
        
        self.__settings_menu_gui["panel"].hide()
        self.__main_menu_gui["panel"].show()

    #__play_level method instantiates the LevelHandler to play a specific level.
    #level_id is an integer representing what level is to be loaded.
    def __play_level(self):
        self.__main_menu_gui["panel"].hide()

        replay = True
        while replay == True:
            level_handler = LevelHandler(self, self.__user_data["current_level"]) #instantiate LevelHandler
            collectibles, success, replay = level_handler.level_loop() #run the main level_handler loop. returns a boolean of whether the user would like to play the level again.
            if success == True:
                self.__user_data["total_collectibles"] += collectibles
        if success == True and self.__user_data["current_level"] < 3:
            self.__user_data["current_level"] += 1
        
        self.__update_gui_text()
        self.__main_menu_gui["panel"].show()

    def save_and_quit(self):
        with open("user_data.json", "w") as f:
            json.dump(self.__user_data, f)
        self.__settings_handler.save_settings()
        self.__running = False
    
    def get_gui_handler(self):
        return self.__gui_handler
    
    def get_music_handler(self):
        return self.__music_handler
    
    def get_settings_handler(self):
        return self.__settings_handler

    def __update_gui_text(self):
        self.__main_menu_gui["txt_collectibles"].set_text(f"Collectibles Collected: {self.__user_data["total_collectibles"]}")
        self.__main_menu_gui["txt_level"].set_text(f"Current Level: {self.__user_data["current_level"]}")
    
    def reload_theme(self):
        self.__main_menu_gui = self.__gui_handler.get_main_menu_panel()
        self.__settings_menu_gui = self.__gui_handler.get_settings_menu_panel()