
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
        speed = random.uniform(100, 300)
        self.vel_x = cos(radians(angle)) * speed
        self.vel_y = sin(radians(angle)) * speed + 100  # Add slight downward bias
        
        self.gravity = 540 * scale_factor
        self.lifetime = random.uniform(0.5, 1.5)  # Particle lives for 0.5-1.5 seconds
        
    def update(self, dt):
        self.lifetime -= dt
        self.vel_y += self.gravity * dt
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))
        
    def is_alive(self):
        return self.lifetime > 0
