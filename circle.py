
import random
import pygame

class Circle:
    def __init__(self, radius, active=True):
        self.radius = radius
        self.active = active
        self.angle = random.randint(0, 360)
        self.rotation_speed = random.uniform(0.5, 2.0)
        self.gap_size = min(90, 30 + (radius / 2))

    def update(self, dt):
        self.angle = (self.angle + self.rotation_speed) % 360

    def is_in_gap(self, ball_angle):
        gap_start = self.angle
        gap_end = (self.angle + self.gap_size) % 360
        if gap_start < gap_end:
            return gap_start <= ball_angle <= gap_end
        else:
            return ball_angle >= gap_start or ball_angle <= gap_end

    def recalculate_layout(self, sX, sY, base_radius):
        # Update gap size based on current radius
        self.gap_size = min(90, 30 + (self.radius / 2))

    def draw(self, surface, center_x, center_y, line_thickness, color, gfxdraw):
        if self.active:
            for i in range(line_thickness):
                gfxdraw.arc(surface, int(center_x), int(center_y),
                           int(self.radius - i),
                           int((self.angle + self.gap_size) % 360),
                           int((self.angle + 360) % 360),
                           color)
