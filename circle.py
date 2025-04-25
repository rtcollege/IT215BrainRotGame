
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

    def check_collision(self, other_circles):
        for circle in other_circles:
            if circle != self and circle.active:
                # Calculate the difference between the radii
                radii_diff = abs(self.radius - circle.radius)
                # If the difference is less than minimum spacing, there's a collision
                if radii_diff < 15:  # Minimum spacing between circles
                    return True
        return False

    def update(self, dt, other_circles=None):
        self.angle = (self.angle + self.rotation_speed) % 360
        if self.active and self.radius > self.min_radius:
            # Store current radius
            current_radius = self.radius
            # Calculate potential new radius
            new_radius = max(self.min_radius, self.radius - self.shrink_rate * dt)

            # Temporarily set the radius to test for collisions
            self.radius = new_radius
            if other_circles and self.check_collision(other_circles):
                # If collision detected, revert to previous radius
                self.radius = current_radius


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
