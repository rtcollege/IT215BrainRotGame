
import pygame
import random
from math import cos, sin

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        angle = random.uniform(0, 2 * 3.14159)
        speed = random.uniform(1, 50)  # Reduced max initial speed
        self.vel_x = cos(angle) * speed + random.uniform(-50, 50)
        self.vel_y = sin(angle) * speed + random.uniform(-50, 50)
        self.gravity = 540
        self.max_speed = 300  # Maximum allowed speed
        self.cell_x = 0
        self.cell_y = 0
        
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
