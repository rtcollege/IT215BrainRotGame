
import random
import pygame

class Circle:
    def __init__(self, radius, active=True):
        self.initial_radius = radius
        self.radius = radius
        self.active = active
        self.angle = random.randint(0, 360)
        self.rotation_speed = random.uniform(0.5, 2.0)
        self.gap_size = min(90, 30 + (radius / 2))
        self.shrink_rate = 5  # Units per second
        self.min_radius = 20  # Minimum radius allowed

    def update(self, dt):
        self.angle = (self.angle + self.rotation_speed) % 360
        if self.active and self.radius > self.min_radius:
            old_radius = self.radius
            self.radius = max(self.min_radius, self.radius - self.shrink_rate * dt)
            # Update gap size as circle shrinks
            self.gap_size = min(90, 30 + (self.radius / 2))
            
            # Check if circle has shrunk past padding threshold
            padding_threshold = self.line_thickness + 20  # Line thickness plus some padding
            if old_radius > (self.radius + padding_threshold):
                return True  # Signal to add new circle
        return False

    def is_in_gap(self, ball_angle):
        gap_start = self.angle
        gap_end = (self.angle + self.gap_size) % 360
        if gap_start < gap_end:
            return gap_start <= ball_angle <= gap_end
        else:
            return ball_angle >= gap_start or ball_angle <= gap_end

    def draw(self, surface, center_x, center_y, line_thickness, color, gfxdraw):
        if self.active:
            for i in range(line_thickness):
                gfxdraw.arc(surface, int(center_x), int(center_y),
                           int(self.radius - i),
                           int((self.angle + self.gap_size) % 360),
                           int((self.angle + 360) % 360),
                           color)
