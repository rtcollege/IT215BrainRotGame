from settings import *
from timer import Timer

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font


    def update(self, dt):
        self.sprites.update(dt)
        self.sprites.draw(self.display_surface)