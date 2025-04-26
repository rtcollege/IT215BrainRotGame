
import random
import pygame

class Circle:
    def __init__(self, radius, line_thickness, active=True):
        self.initial_radius = radius
        self.radius = radius
        self.active = active
        self.angle = random.randint(0, 360)
        self.rotation_speed = random.uniform(0.5, 2.0)
        self.gap_size = min(90, 30 + (radius / 2))
        self.shrink_rate = 15  # Units per second
        self.min_radius = 20  # Minimum radius allowed
        self.line_thickness = line_thickness
        self.scale_factor = 1.0
        self.respawn_timer = 0
        self.respawn_delay = 1.0  # 1 second delay before respawning

    def check_collision(self, other_circles):
        if not other_circles:
            return False
            
        for circle in other_circles:
            if not circle.active or circle == self:
                continue

            base_collision_threshold = self.line_thickness * 4
            collision_threshold = base_collision_threshold * self.scale_factor
            
            radii_diff = abs(self.radius - circle.radius)
            if radii_diff < collision_threshold:
                if self.radius >= circle.radius:
                    return True
                    
                # Quick check for space below
                target_radius = self.radius - collision_threshold
                return any(
                    other != self and other != circle and 
                    other.active and 
                    abs(other.radius - target_radius) < collision_threshold
                    for other in other_circles
                )
        return False

    def update(self, dt, other_circles=None, level=1):
        # Update respawn timer if inactive
        if not self.active:
            if self.respawn_timer > 0:
                self.respawn_timer = max(0, self.respawn_timer - dt)
                if self.respawn_timer == 0:
                    self.active = True
            return

        # Rotation speed remains constant regardless of level
        self.angle = (self.angle + self.rotation_speed) % 360
        if self.active and self.radius > self.min_radius:
            # Store current radius
            current_radius = self.radius
            # Calculate potential new radius with level scaling
            shrink_rate = self.shrink_rate * (1 + (level - 1) * 0.2)  # Only shrink rate scales with level
            new_radius = max(self.min_radius, self.radius - shrink_rate * dt)

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
