
import pygame
from ui import UI
from settings import *

class GameView:
    def __init__(self, model):
        self.model = model
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", 40)
        self.ui = UI(self.font, {
            'currency': pygame.image.load('graphics/ui/currency.png').convert_alpha()
        })
        self.model.data.ui = self.ui

    def render(self, dt):
        self.display_surface.fill("gray")
        self.ui.update(dt)
        pygame.display.update()
