import pygame
import os

class MusicManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.current_music = None
        # Load music
        self.sounds['main_menu'] = pygame.mixer.Sound('data/music/main_menu.mp3')
        self.sounds['gameplay'] = pygame.mixer.Sound('data/music/gameplay.mp3')
        self.sounds['game_over'] = pygame.mixer.Sound('data/music/game_over.mp3')
        # Load sound effects
        self.sounds['bounce'] = pygame.mixer.Sound('data/sfx/bounce.mp3')

    def play_music(self, music_type, loops=-1):
        """Play music of specified type. loops=-1 means loop indefinitely"""
        if music_type in self.music_paths:
            path = self.music_paths[music_type]
            if os.path.exists(path):
                if self.current_music != music_type:
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.play(loops)
                    self.current_music = music_type

    def stop_music(self):
        """Stop currently playing music"""
        pygame.mixer.music.stop()
        self.current_music = None

    def set_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        pygame.mixer.music.set_volume(volume)

    def play_sound(self, sound_type):
        if sound_type in self.sounds:
            self.sounds[sound_type].play()