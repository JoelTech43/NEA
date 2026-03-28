import json

class SettingsHandler:
    def __init__(self): #loads current settings and sets the pygame_gui theme to the current settings.
        self.__settings = self.__load_settings()
        self.__update_theme_file()
    
    def __load_settings(self) -> dict: #if settings.json file exists, load it as a dictionary.
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
        
        except FileNotFoundError: #if doesn't exist, create a new settings dist.
            settings = {
                "bg_vol": 100,
                "sfx_vol": 100,
                "bg_col": (230, 229, 229),
                "wall_col": (0, 0, 0),
                "btn_col": (156, 150, 150),
                "highlight_col": (0, 153, 255),
                "player_col": (2, 186, 13),
                "enemy_col": (255, 0, 0),
                "selected_item": "bg_col"
            }
        
        return settings

    def __update_theme_file(self): #load the theme.json file as a dictionary, change the dictionary to match the colours in the settings dict, then dump the dictionary into theme.json using the json module.
        with open("theme.json", "r") as f:
            theme = json.load(f)

        theme["#colour_rect"]["colours"]["dark_bg"] = self.__rgb_to_hex(self.__settings[self.__settings["selected_item"]])
        
        theme["label"]["colours"]["normal_text"] = self.__rgb_to_hex(self.__settings["wall_col"])
        theme["button"]["colours"]["normal_bg"] = self.__rgb_to_hex(self.__settings["btn_col"])
        theme["button"]["colours"]["normal_text"] = self.__rgb_to_hex(self.__settings["wall_col"])
        theme["horizontal_slider"]["colours"]["dark_bg"] = self.__rgb_to_hex(self.__settings["btn_col"])
        theme["horizontal_slider.#left_button"]["colours"]["normal_bg"] = self.__rgb_to_hex(self.__settings["btn_col"])
        theme["horizontal_slider.#left_button"]["colours"]["normal_text"] = self.__rgb_to_hex(self.__settings["wall_col"])
        theme["horizontal_slider.#right_button"]["colours"]["normal_bg"] = self.__rgb_to_hex(self.__settings["btn_col"])
        theme["horizontal_slider.#right_button"]["colours"]["normal_text"] = self.__rgb_to_hex(self.__settings["wall_col"])
        theme["horizontal_slider.#sliding_button"]["colours"]["normal_bg"] = self.__rgb_to_hex(self.__settings["btn_col"])
        theme["horizontal_slider.#sliding_button"]["colours"]["normal_text"] = self.__rgb_to_hex(self.__settings["wall_col"])

        with open("theme.json", "w") as f:
            json.dump(theme, f, indent=4)
        
        f = open("theme.json", "a")
        f.close()

    def __rgb_to_hex(self, col):
        r,g,b = col
        return '#%02x%02x%02x' % (r, g, b) #not designed by me.
    
    def set_light_theme(self): #sets colours to the light theme created by me and updates the theme.json file to change the pygame_gui theme.
        self.__settings["bg_col"] = (230, 229, 229)
        self.__settings["wall_col"] = (0, 0, 0)
        self.__settings["btn_col"] = (156, 150, 150)
        self.__settings["highlight_col"] = (0, 153, 255)
        self.__settings["player_col"] = (2, 186, 13)
        self.__settings["enemy_col"] = (255, 0, 0)
        
        self.__update_theme_file()
    
    def set_light_hc_theme(self): #sets colours to the light high contrast theme created by me and updates the theme.json file to change the pygame_gui theme.
        self.__settings["bg_col"] = (255, 255, 255)
        self.__settings["wall_col"] = (0, 0, 0)
        self.__settings["btn_col"] = (255, 255, 255)
        self.__settings["highlight_col"] = (240, 228, 66)
        self.__settings["player_col"] = (0, 158, 115)
        self.__settings["enemy_col"] = (213,94, 0)
        
        self.__update_theme_file()
    
    def set_dark_theme(self): #sets colours to the dark theme created by me and updates the theme.json file to change the pygame_gui theme.
        self.__settings["bg_col"] = (97, 97, 97)
        self.__settings["wall_col"] = (246, 110, 13)
        self.__settings["btn_col"] = (51, 51, 51)
        self.__settings["highlight_col"] = (246, 199, 13)
        self.__settings["player_col"] = (2, 186, 13)
        self.__settings["enemy_col"] = (255, 0, 0)
        
        self.__update_theme_file()
    
    def set_dark_hc_theme(self): #sets colours to the dark high contrast theme created by me and updates the theme.json file to change the pygame_gui theme.
        self.__settings["bg_col"] = (0, 0, 0)
        self.__settings["wall_col"] = (255, 255, 255)
        self.__settings["btn_col"] = (0, 0, 0)
        self.__settings["highlight_col"] = (240, 228, 66)
        self.__settings["player_col"] = (0, 158, 115)
        self.__settings["enemy_col"] = (213,94, 0)
        
        self.__update_theme_file()

    def get_bg_volume(self):
        return self.__settings["bg_vol"]
    
    def get_sfx_volume(self):
        return self.__settings["sfx_vol"]
    
    def set_bg_volume(self, vol):
        self.__settings["bg_vol"] = vol
    
    def set_sfx_volume(self, vol):
        self.__settings["sfx_vol"] = vol
    
    def get_bg_col(self):
        return self.__settings["bg_col"]

    def get_wall_col(self):
        return self.__settings["wall_col"]
    
    def get_btn_col(self):
        return self.__settings["btn_col"]
    
    def get_highlight_col(self):
        return self.__settings["highlight_col"]
    
    def get_player_col(self):
        return self.__settings["player_col"]
    
    def get_enemy_col(self):
        return self.__settings["enemy_col"]
    
    def get_selected_item(self):
        return self.__settings["selected_item"]
    
    def get_settings(self):
        return self.__settings.copy()
    
    def set_settings(self, settings):
        self.__settings = settings
        self.__update_theme_file()
    
    def save_settings(self): #save settings by dumping the dictionary in settings.json using the json module. If settings.json does not exist, opening in write mode will create it.
        with open("settings.json", "w") as f:
            json.dump(self.__settings, f, indent=4)