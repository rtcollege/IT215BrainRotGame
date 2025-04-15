import pygame

# Game settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Player settings
PLAYER_SPEED = 5
PLAYER_SIZE = 64
GRAVITY = 0.8
JUMP_SPEED = -16

# Game states
MENU = 'menu'
PLAYING = 'playing'
PAUSED = 'paused'
GAME_OVER = 'game_over'

# Layers
Z_LAYERS = {
    'background': 0,
    'terrain': 1,
    'player': 2,
    'ui': 3
}

# Asset paths
ASSET_DIR = 'assets'
GRAPHICS_DIR = f'{ASSET_DIR}/graphics'
SOUND_DIR = f'{ASSET_DIR}/sound'
MUSIC_DIR = f'{ASSET_DIR}/music'
