
import pygame
import random
from math import cos, sin, radians

class Particle:
    def __init__(self, x, y, color, scale_factor=1.0):
        self.x = x
        self.y = y
        self.radius = 3 * scale_factor
        self.color = color
        
        # Random angle and speed
        angle = random.uniform(0, 360)
        speed = random.uniform(50, 150)  # Reduced speed range
        self.vel_x = cos(radians(angle)) * speed
        self.vel_y = sin(radians(angle)) * speed + 50  # Reduced downward bias
        
        self.gravity = 540 * scale_factor
        self.lifetime = random.uniform(0.2, 0.8)  # Reduced lifetime range
        
    def update(self, dt):
        self.lifetime -= dt
        self.vel_y += self.gravity * dt
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))
        
    def is_alive(self):
        return self.lifetime > 0
