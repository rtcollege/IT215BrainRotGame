
import pygame
import random
from math import cos, sin

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        angle = random.uniform(0, 2 * 3.14159)
        speed = random.uniform(100, 200)  # Increased initial speed range
        self.vel_x = cos(angle) * speed + random.uniform(-100, 100)
        self.vel_y = sin(angle) * speed + random.uniform(-100, 100)
        self.gravity = 400  # Reduced gravity
        self.max_speed = 600  # Increased max speed
        self.bounce_factor = random.uniform(0.92, 0.98)  # Random bounce energy retention
        self.drift_force = random.uniform(-50, 50)  # Random horizontal drift
        
    def update(self, dt):
        self.vel_y += self.gravity * dt
        self.vel_x += self.drift_force * dt  # Add horizontal drift
        
        # Add slight random motion
        self.vel_x += random.uniform(-20, 20) * dt
        self.vel_y += random.uniform(-20, 20) * dt
        
        # Limit velocity
        speed_squared = self.vel_x ** 2 + self.vel_y ** 2
        max_speed_squared = self.max_speed ** 2
        if speed_squared > max_speed_squared:
            scale = (self.max_speed / (speed_squared ** 0.5))
            self.vel_x *= scale
            self.vel_y *= scale
        
        # Update position
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        
        # Apply air resistance
        self.vel_x *= 0.99
        self.vel_y *= 0.99

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
