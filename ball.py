
import pygame
import random
from math import cos, sin

class Ball:
    def __init__(self, x, y, radius, center_x=0, center_y=0):
        self.x = x
        self.y = y
        self.center_x = center_x
        self.center_y = center_y
        self.rel_x = x - center_x  # Store relative position
        self.rel_y = y - center_y
        self.radius = radius
        angle = random.uniform(0, 2 * 3.14159)
        speed = random.uniform(1, 50)  # Reduced max initial speed
        self.vel_x = cos(angle) * speed + random.uniform(-100, 100)
        self.vel_y = sin(angle) * speed + random.uniform(-100, 100)
        self.gravity = 540
        self.max_speed = 500  # Maximum allowed speed
        self.cell_x = 0
        self.cell_y = 0
        
    def rescale(self, new_center_x, new_center_y, scale_factor, ball_radius):
        """Rescale ball position and properties based on new center and scale"""
        self.center_x = new_center_x
        self.center_y = new_center_y
        # Update position based on relative coordinates
        self.x = new_center_x + (self.rel_x * scale_factor)
        self.y = new_center_y + (self.rel_y * scale_factor)
        # Update relative position with new scale
        self.rel_x = self.x - new_center_x
        self.rel_y = self.y - new_center_y
        # Scale radius and velocities
        self.radius = ball_radius * scale_factor
        self.vel_x *= scale_factor
        self.vel_y *= scale_factor
        self.max_speed *= scale_factor
        self.gravity *= scale_factor
        
    def update(self, dt):
        self.vel_y += self.gravity * dt
        
        # Limit velocity to max_speed using squared comparison (avoid sqrt)
        speed_squared = self.vel_x ** 2 + self.vel_y ** 2
        max_speed_squared = self.max_speed ** 2
        if speed_squared > max_speed_squared:
            scale = (self.max_speed / (speed_squared ** 0.5))
            self.vel_x *= scale
            self.vel_y *= scale
            
        # Use fewer substeps for better performance
        substeps = 2
        dt_sub = dt / substeps
        for _ in range(substeps):
            self.x += self.vel_x * dt_sub
            self.y += self.vel_y * dt_sub

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
