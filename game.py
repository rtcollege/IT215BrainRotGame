
import pygame
from ballsim import BallSimulation

class Game:
    def __init__(self, ui):
        self.display_surface = pygame.display.get_surface()
        self.ui = ui
        self.ball_sim = BallSimulation()
        
    def update(self, dt):
        if self.ui.current_scene == 'gameplay' and not self.ui.is_paused:
            # Draw container box and ball
            self.ball_sim.update(dt)
