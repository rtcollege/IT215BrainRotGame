
import pygame
from math import sin, cos, radians

class BallSimulation:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.radius = 30
        self.center_x = 100
        self.center_y = self.display_surface.get_height() // 2
        self.angle = 0
        self.rotation_speed = 2
        self.color = '#b68f40'  # Matching the UI gold color
        self.orbit_radius = 20

    def update(self, dt):
        # Update angle
        self.angle = (self.angle + self.rotation_speed) % 360
        
        # Calculate orbit position
        orbit_x = self.center_x + cos(radians(self.angle)) * self.orbit_radius
        orbit_y = self.center_y + sin(radians(self.angle)) * self.orbit_radius
        
        # Draw the ball
        pygame.draw.circle(self.display_surface, self.color, (orbit_x, orbit_y), self.radius)
