import pygame
import pygame_gui

class GUIHandler:
    def __init__(self):
        main_desktop_size = pygame.display.get_desktop_sizes()[1] #gets display sizes (px) as tuples (width, height). I use index 0 as this is the main monitor.
        self.__WINDOW_SIZE = (int(main_desktop_size[0]*0.8), int(main_desktop_size[1]*0.8)) #sets window size to 80% of screen size so that user can easily switch to other windows and close game, but large enough to see maze clearly.
        self.__MAZE_SCREEN_HEIGHT = min(int(self.__WINDOW_SIZE[0]*0.9), int(self.__WINDOW_SIZE[1]*0.95)) #maze height is either set to 90% of the window width, or 95% of window height. Means maze is as large as possible whilst leaving some around it.
        self.__MAZE_SCREEN_POS = ((self.__WINDOW_SIZE[0]-self.__MAZE_SCREEN_HEIGHT)//2, (self.__WINDOW_SIZE[1]-self.__MAZE_SCREEN_HEIGHT)//2) #start position in window (x,y) from top left. Centers maze by finding difference between window size and maze size and halving.

        self.__canvas = pygame.display.set_mode(self.__WINDOW_SIZE) #creates the window, with the size we calculated earlier.
        pygame.display.set_caption("Joel's A-maze-ing Game") #sets window title

        self.__gui_manager = pygame_gui.UIManager(self.__WINDOW_SIZE, "test_theme.json")
        #pygame.time.Clock() not needed as simple game so can just assume 1/60 for time_deltas.

        self.__main_menu_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0), self.__WINDOW_SIZE), starting_height=1, manager=self.__gui_manager)
        self.__txt_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((30,30), (500,50)), text="Joel's A-maze-ing Game", manager=self.__gui_manager, container=self.__main_menu_panel)
        self.__txt_level = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((30,100), (5000,500)), text="Current Level: ___", manager=self.__gui_manager, container=self.__main_menu_panel)
        self.__txt_stars = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((30,200), (5000,500)), text="Stars Collected: ___", manager=self.__gui_manager, container=self.__main_menu_panel)
        self.__btn_play_level = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100,100), (100,50)), text="Play", manager=self.__gui_manager, container=self.__main_menu_panel)
        self.__btn_settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100,300), (100,50)), text="Settings", manager=self.__gui_manager, container=self.__main_menu_panel)
        self.__btn_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100,500), (100,50)), text="Quit Game", manager=self.__gui_manager, container=self.__main_menu_panel)
        
        self.__level_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0), self.__WINDOW_SIZE), starting_height=1, manager=self.__gui_manager)
        self.__txt_collectibles_collected = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,60), (200,20)), text="Collectibles Collected: _/_", manager=self.__gui_manager, container=self.__level_panel)
        self.__txt_time_remaining = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,80), (200,20)), text="Time Remaining: __:__", manager=self.__gui_manager, container=self.__level_panel)
        self.__btn_pause = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((5,5), (50,50)), text="⏸", manager=self.__gui_manager, container=self.__level_panel)

        self.__pause_menu_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0), self.__WINDOW_SIZE), starting_height=1, manager=self.__gui_manager)
        self.__txt_pause_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,5), (150,20)), text="Game Paused", manager=self.__gui_manager, container=self.__pause_menu_panel)
        self.__txt_pause_volume_subtitle = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,25), (150,20)), text="Volume Settings:", manager=self.__gui_manager, container=self.__pause_menu_panel)
        self.__txt_pause_bg_volume = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,45), (200,20)), text="Background Volume: __%", manager=self.__gui_manager, container=self.__pause_menu_panel)
        self.__slider_pause_bg_volume = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((5,65), (1000,50)), start_value=50, value_range=(0,100), manager=self.__gui_manager, container=self.__pause_menu_panel)
        self.__txt_pause_sfx_volume = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,115), (200,20)), text="Sound Effects Volume: __%", manager=self.__gui_manager, container=self.__pause_menu_panel)
        self.__slider_pause_sfx_volume = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((5,135), (1000,50)), start_value=50, value_range=(0,100), manager=self.__gui_manager, container=self.__pause_menu_panel)
        self.__btn_resume = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((5,185), (100,50)), text="Resume", manager=self.__gui_manager, container=self.__pause_menu_panel)
        self.__btn_pause_settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((110, 185), (100,50)), text="Settings", manager=self.__gui_manager, container=self.__pause_menu_panel)
        self.__btn_restart = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((215,185), (100,50)), text="Restart Level", manager=self.__gui_manager, container=self.__pause_menu_panel)
        self.__btn_quit_level = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((320,185), (100,50)), text="Quit Level", manager=self.__gui_manager, container=self.__pause_menu_panel)

        self.__settings_menu_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0), self.__WINDOW_SIZE), starting_height=1, manager=self.__gui_manager)
        self.__txt_settings_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,5), (150,20)), text="Settings", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__txt_settings_volume_subtitle = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,25), (150,20)), text="Volume Settings:", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__txt_settings_bg_volume = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,45), (200,20)), text="Background Volume: __%", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__slider_settings_bg_volume = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((5,65), (500,50)), start_value=50, value_range=(0,100), manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__txt_settings_sfx_volume = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,115), (200,20)), text="Sound Effects Volume: __%", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__slider_settings_sfx_volume = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((5,135), (500,50)), start_value=50, value_range=(0,100), manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__txt_theme_subtitle = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550,25), (150,20)), text="Theme Settings:", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__drop_theme_section = pygame_gui.elements.UIDropDownMenu(options_list=["Background", "Text/Walls", "Buttons", "Highlights", "Player", "Enemy"], starting_option="Background", relative_rect=pygame.Rect((550,45),(200,50)), manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__colour_rect = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((550,95), (200,50)), manager=self.__gui_manager, container=self.__settings_menu_panel, object_id="#colour_rect")
        self.__txt_red_level = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((750,45), (100,20)), text="Red: __%", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__slider_red_level = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((750,65), (500,50)), start_value=50, value_range=(0,100), manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__txt_green_level = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((750,115), (150,20)), text="Green: __%", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__slider_green_level = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((750,135), (500,50)), start_value=50, value_range=(0,100), manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__txt_blue_level = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((750,185), (150,20)), text="Blue: __%", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__slider_blue_level = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((750,205), (500,50)), start_value=50, value_range=(0,100), manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__txt_preset_themes = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550,255), (150,20)), text="Preset Themes:", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__btn_light_theme = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550,275), (100,50)), text="Light", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__btn_dark_theme = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650,275), (100,50)), text="Dark", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__btn_light_hc_theme = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((750,275), (100,50)), text="Light High\nContrast", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__btn_dark_hc_theme = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((850,275), (100,50)), text="Dark High\nContrast", manager=self.__gui_manager, container=self.__settings_menu_panel)
        self.__btn_exit_settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((5,325), (100,50)), text="Exit Settings", manager=self.__gui_manager, container=self.__settings_menu_panel)

        self.__endgame_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0), self.__WINDOW_SIZE), starting_height=1, manager=self.__gui_manager)
        self.__txt_endgame_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,5), (150,20)), text="Game Win/Loss", manager=self.__gui_manager, container=self.__endgame_panel)
        self.__btn_replay = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((5,50), (100,50)), text="Replay Level", manager=self.__gui_manager, container=self.__endgame_panel)
        self.__btn_return = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((110,50), (100,50)), text="Return to\nMain Menu", manager=self.__gui_manager, container=self.__endgame_panel)

        self.__main_menu_panel.show()
        self.__level_panel.hide()
        self.__pause_menu_panel.hide()
        self.__settings_menu_panel.hide()
        self.__endgame_panel.hide()
    
    def get_main_menu_panel(self) -> dict:
        return {"panel": self.__main_menu_panel, "txt_title": self.__txt_title, "txt_level": self.__txt_level, "txt_stars": self.__txt_stars, "btn_play_level": self.__btn_play_level, "btn_settings": self.__btn_settings, "btn_quit": self.__btn_quit}
    
    def get_level_panel(self) -> dict:
        return {"panel": self.__level_panel, "txt_collectibles_collected": self.__txt_collectibles_collected, "txt_time_remaining": self.__txt_time_remaining, "btn_pause": self.__btn_pause}
    
    def get_pause_menu_panel(self):
        return {"panel": self.__pause_menu_panel, "txt_pause_title": self.__txt_pause_title, "txt_pause_volume_subtitle": self.__txt_pause_volume_subtitle, "txt_bg_volume": self.__txt_pause_bg_volume, "slider_bg_volume": self.__slider_pause_bg_volume, "txt_sfx_volume": self.__txt_pause_sfx_volume, "slider_sfx_volume": self.__slider_pause_sfx_volume, "btn_resume": self.__btn_resume, "btn_pause_settings": self.__btn_pause_settings, "btn_restart": self.__btn_restart, "btn_quit_level": self.__btn_quit_level}

    def get_settings_menu_panel(self):
        return {"panel": self.__settings_menu_panel, "txt_settings_title": self.__txt_settings_title, "txt_settings_volume_subtitle": self.__txt_settings_volume_subtitle, "txt_settings_bg_volume": self.__txt_settings_bg_volume, "slider_settings_bg_volume": self.__slider_settings_bg_volume, "txt_settings_sfx_volume": self.__txt_settings_sfx_volume, "slider_settings_sfx_volume": self.__slider_settings_sfx_volume, "txt_theme_subtitle": self.__txt_theme_subtitle, "drop_theme_section": self.__drop_theme_section, "colour_rect": self.__colour_rect, "txt_red_level": self.__txt_red_level, "slider_red_level": self.__slider_red_level, "txt_green_level": self.__txt_green_level, "slider_green_level": self.__slider_green_level, "txt_blue_level": self.__txt_blue_level, "slider_blue_level": self.__slider_blue_level, "txt_preset_themes": self.__txt_preset_themes, "btn_light_theme": self.__btn_light_theme, "btn_dark_theme": self.__btn_dark_theme, "btn_light_hc_theme": self.__btn_light_hc_theme, "btn_dark_hc_theme": self.__btn_dark_hc_theme, "btn_exit_settings": self.__btn_exit_settings}

    def get_endgame_panel(self):
        return {"panel": self.__endgame_panel, "txt_endgame_title": self.__txt_endgame_title, "btn_replay": self.__btn_replay, "btn_return": self.__btn_return}

    def process_events(self, event):
        self.__gui_manager.process_events(event)
    
    def update(self, delta):
        self.__gui_manager.update(delta)
    
    def draw_ui(self):
        self.__gui_manager.draw_ui(self.__canvas)
    
    def get_canvas(self):
        return self.__canvas

    def get_window_size(self) -> tuple:
        return self.__WINDOW_SIZE
    
    def get_maze_screen_height(self) -> int:
        return self.__MAZE_SCREEN_HEIGHT
    
    def get_maze_screen_pos(self) -> tuple:
        return self.__MAZE_SCREEN_POS