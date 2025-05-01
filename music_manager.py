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

    def play_music(self, track_type, loops=-1):
        """Play specified track. loops=-1 means loop indefinitely"""
        if track_type in self.sounds:
            if self.current_music:
                self.current_music.stop()
            self.current_music = self.sounds[track_type]
            self.current_music.play(loops)

    def stop_music(self):
        """Stop currently playing music"""
        if self.current_music:
            self.current_music.stop()
            self.current_music = None

    def set_volume(self, volume):
        """Set volume for all sounds (0.0 to 1.0)"""
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def plays_sound(self, sound_type):
        """Play a sound effect once"""
        if sound_type in self.sounds:
            self.sounds[sound_type].play()