import pygame

class MusicHandler:
    def __init__(self):
        self.__menu_music = True
        self.__playing = False

        self.__click = pygame.mixer.Sound("blipSelect.wav")
        self.__death = pygame.mixer.Sound("explosion.wav")
        self.__success = pygame.mixer.Sound("Yippee.wav")
        self.__collectible = pygame.mixer.Sound("pickupCoin.wav")
        self.__error = pygame.mixer.Sound("error.mp3")

        pygame.mixer.music.load("menu_bg.mp3")
        pygame.mixer.music.play(-1)
    
    def play_action_music(self):
        if self.__menu_music == True or self.__playing == False:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("action_bg.mp3")

            pygame.mixer.music.play(-1)
            self.__playing = True
            self.__menu_music = False
    
    def play_menu_music(self):
        if self.__menu_music == False or self.__playing == False:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("menu_bg.mp3")
            
            pygame.mixer.music.play(-1)
            self.__playing = True
            self.__menu_music = True
    
    def stop_bg_music(self):
        pygame.mixer.music.stop()
        self.__playing = False
    
    def play_sfx_click(self):
        pygame.mixer.Sound.play(self.__click)
    
    def play_sfx_death(self):
        pygame.mixer.Sound.play(self.__death)
    
    def play_sfx_success(self):
        pygame.mixer.Sound.play(self.__success)
    
    def play_sfx_collectible(self):
        pygame.mixer.Sound.play(self.__collectible)
    
    def play_sfx_error(self):
        pygame.mixer.Sound.play(self.__error)
    
    def set_background_volume(self, volume:int):
        pygame.mixer.music.set_volume((volume/100))
    
    def set_sfx_volume(self, volume:int):
        volume_dec = volume/100
        self.__click.set_volume(volume_dec)
        self.__death.set_volume(volume_dec)
        self.__success.set_volume(volume_dec)
        self.__collectible.set_volume(volume_dec)
        self.__error.set_volume(volume_dec)