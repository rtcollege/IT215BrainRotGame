
import pygame
import random
from math import cos, sin

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        angle = random.uniform(0, 2 * 3.14159)
        speed = random.uniform(1, 100)
        self.vel_x = cos(angle) * speed + random.uniform(-100, 100)
        self.vel_y = sin(angle) * speed + random.uniform(-100, 100)
        self.gravity = 540
        self.cell_x = 0
        self.cell_y = 0
        
    def update(self, dt):
        self.vel_y += self.gravity * dt
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
