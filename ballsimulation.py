
import pygame
import pygame.gfxdraw
from math import sin, cos, radians, degrees

class BallSimulation:
    def __init__(self, display_surface, sX, sY):
        self.display_surface = display_surface
        self.base_radius = 150
        self.base_box_width = int(display_surface.get_width() / 3)  # One third of screen width
        self.base_box_height = int(display_surface.get_height() * 2/3)  # Two thirds of screen height
        self.base_box_x = 50  # Fixed left position
        self.angle = 0
        self.rotation_speed = 2
        self.color = (182, 143, 64)  # RGB values for #b68f40
        self.recalculate_layout(sX, sY)

    def recalculate_layout(self, sX, sY):
        # Scale all dimensions
        self.radius = int(self.base_radius * min(sX, sY))
        self.box_width = int(self.base_box_width * sX)
        self.box_height = int(self.base_box_height * sY)
        self.box_x = int(self.base_box_x * sX)
        self.box_y = (self.display_surface.get_height() - self.box_height) // 2
        self.center_x = self.box_x + self.box_width // 2
        self.center_y = self.box_y + self.box_height // 2
        self.line_thickness = max(1, int(3 * min(sX, sY)))

    def update(self, dt, sX, sY):
        # Draw container box with scaled thickness
        pygame.draw.rect(self.display_surface, '#cccccc', 
                        (self.box_x, self.box_y, self.box_width, self.box_height), 
                        max(1, int(1 * min(sX, sY))))

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
