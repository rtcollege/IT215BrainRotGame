
import pygame
import pygame.gfxdraw
from math import sin, cos, radians, degrees
from settings import SCALE_X, SCALE_Y

class BallSimulation:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.base_radius = 100
        self.base_box_width = 200
        self.base_box_height = 300
        self.base_box_x = 50
        self.angle = 0
        self.rotation_speed = 2
        self.color = (182, 143, 64)  # RGB values for #b68f40
        self.recalculate_layout()

    def recalculate_layout(self):
        # Scale all dimensions
        self.radius = int(self.base_radius * min(SCALE_X, SCALE_Y))
        self.box_width = int(self.base_box_width * SCALE_X)
        self.box_height = int(self.base_box_height * SCALE_Y)
        self.box_x = int(self.base_box_x * SCALE_X)
        self.box_y = (self.display_surface.get_height() - self.box_height) // 2
        self.center_x = self.box_x + self.box_width // 2
        self.center_y = self.box_y + self.box_height // 2
        self.line_thickness = max(1, int(3 * min(SCALE_X, SCALE_Y)))

    def update(self, dt):
        # Draw container box with scaled thickness
        pygame.draw.rect(self.display_surface, '#cccccc', 
                        (self.box_x, self.box_y, self.box_width, self.box_height), 
                        max(1, int(1 * min(SCALE_X, SCALE_Y))))

        # Update angle and draw hollow circle with cutout
        self.angle = (self.angle + self.rotation_speed) % 360
        start_angle = radians(self.angle)
        end_angle = radians((self.angle + 330) % 360)  # 330 degrees creates a 30-degree gap
        
        # Draw arc with scaled thickness
        for i in range(self.line_thickness):
            pygame.gfxdraw.arc(self.display_surface, 
                            self.center_x, 
                            self.center_y, 
                            self.radius - i, 
                            int(degrees(start_angle)), 
                            int(degrees(end_angle)), 
                            self.color)
