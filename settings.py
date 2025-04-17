import pygame, sys
from pygame.math import Vector2 as vector

# Game settings
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
TILE_SIZE = 64
ANIMATION_SPEED = 10
FPS = 60

# Layers
Z_LAYERS = {
    'background': 0,
    'terrain': 1,
    'player': 2,
    'ui': 3
}