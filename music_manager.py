
import pygame
import os

class MusicManager:
    def __init__(self):
        self.current_music = None
        self.music_paths = {
            'main_menu': 'data/main_menu.mp3',
            'gameplay': 'data/gameplay.mp3',
            'game_over': 'data/game_over.mp3'
        }
        
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
