import pygame

class MusicHandler:
    def __init__(self):
        self.__menu_music = True #represents whether menu music loaded. If False, action music loaded.
        self.__playing = False #represents whether background music currently playing.

        self.__click = pygame.mixer.Sound("blipSelect.wav") #load all sound effect files.
        self.__death = pygame.mixer.Sound("explosion.wav")
        self.__success = pygame.mixer.Sound("Yippee.wav")
        self.__collectible = pygame.mixer.Sound("pickupCoin.wav")
        self.__error = pygame.mixer.Sound("error.mp3")

        pygame.mixer.music.load("menu_bg.mp3") #load menu background music.
        pygame.mixer.music.play(-1) #play in an infinite loop.
    
    def play_action_music(self):
        if self.__menu_music == True or self.__playing == False: #if the current music is menu or no music playing. This means that if action music playing, not restarted.
            pygame.mixer.music.stop() #stop the current music
            pygame.mixer.music.load("action_bg.mp3") #load action music

            pygame.mixer.music.play(-1) #play on an infinite loop
            self.__playing = True #now playing music
            self.__menu_music = False #not menu music
    
    def play_menu_music(self):
        if self.__menu_music == False or self.__playing == False: #if the current music is action or no music playing. This means that if menu music playing, not restarted.
            pygame.mixer.music.stop() #stop the current music
            pygame.mixer.music.load("menu_bg.mp3") #load menu music
            
            pygame.mixer.music.play(-1) #play on an infinite loop
            self.__playing = True #now playing music
            self.__menu_music = True #it is menu music
    
    def stop_bg_music(self): #stops music
        pygame.mixer.music.stop()
        self.__playing = False #no longer playing.
    
    #play sfx methods play sfx over the background music.
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
    
    def set_background_volume(self, volume:int): #set volume of background music player to volume/100. Volume is integer showing desired volume percentage. Pygame takes volume as a float between 0 and 1.
        pygame.mixer.music.set_volume((volume/100))
    
    def set_sfx_volume(self, volume:int): #set volume of all sfx files to volume/100. Volume is integer showing desired volume percentage. Pygame takes volume as a float between 0 and 1.
        volume_dec = volume/100
        self.__click.set_volume(volume_dec)
        self.__death.set_volume(volume_dec)
        self.__success.set_volume(volume_dec)
        self.__collectible.set_volume(volume_dec)
        self.__error.set_volume(volume_dec)