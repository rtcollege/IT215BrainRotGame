
import pygame
from math import sin, cos, radians

class BallSimulation:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.radius = 50
        self.box_width = 150
        self.box_height = 200
        self.box_x = 50
        self.box_y = (self.display_surface.get_height() - self.box_height) // 2
        self.center_x = self.box_x + self.box_width // 2
        self.center_y = self.box_y + self.box_height // 2
        self.angle = 0
        self.rotation_speed = 2
        self.color = '#b68f40'

    def update(self, dt):
        # Draw container box
        pygame.draw.rect(self.display_surface, 'white', 
                        (self.box_x, self.box_y, self.box_width, self.box_height), 2)

        # Update angle and draw hollow circle with cutout
        self.angle = (self.angle + self.rotation_speed) % 360
        start_angle = radians(self.angle)
        end_angle = radians((self.angle + 330) % 360)  # 330 degrees creates a 30-degree gap
        
        # Draw arc (hollow circle with gap)
        rect = pygame.Rect(
            self.center_x - self.radius, 
            self.center_y - self.radius,
            self.radius * 2, 
            self.radius * 2
        )
        pygame.draw.arc(self.display_surface, self.color, rect, start_angle, end_angle, 3)
