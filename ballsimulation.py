
import pygame
import pygame.gfxdraw
from math import sin, cos, radians, degrees
from settings import SCALE_X, SCALE_Y

class BallSimulation:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.radius = int(100 * min(SCALE_X, SCALE_Y))
        self.box_width = int(200 * SCALE_X)
        self.box_height = int(300 * SCALE_Y)
        self.box_x = int(50 * SCALE_X)
        self.box_y = (self.display_surface.get_height() - self.box_height) // 2
        self.center_x = self.box_x + self.box_width // 2
        self.center_y = self.box_y + self.box_height // 2
        self.angle = 0
        self.rotation_speed = 2
        self.color = (182, 143, 64)  # RGB values for #b68f40

    def update(self, dt):
        # Draw container box
        pygame.draw.rect(self.display_surface, '#cccccc', 
                        (self.box_x, self.box_y, self.box_width, self.box_height), 
                        int(1 * min(SCALE_X, SCALE_Y)))

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
        
        # Draw anti-aliased arc with scaled thickness
        thickness = int(3 * min(SCALE_X, SCALE_Y))
        for i in range(thickness):
            pygame.gfxdraw.arc(self.display_surface, 
                            self.center_x, 
                            self.center_y, 
                            self.radius - i, 
                            int(degrees(start_angle)), 
                            int(degrees(end_angle)), 
                            self.color)
