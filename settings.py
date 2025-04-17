import pygame, sys
from pygame.math import Vector2 as vector

# Game settings
# Base resolution for scaling
BASE_WIDTH = 1280
BASE_HEIGHT = 720

# Current window size
WINDOW_WIDTH = 960  # You can adjust this
WINDOW_HEIGHT = 540  # You can adjust this

# Calculate scale factors
SCALE_X = WINDOW_WIDTH / BASE_WIDTH
SCALE_Y = WINDOW_HEIGHT / BASE_HEIGHT

# Other settings
ANIMATION_SPEED = 10
FPS = 60

# Layers
Z_LAYERS = {
    'background': 0,
    'terrain': 1,
    'player': 2,
    'ui': 3
}