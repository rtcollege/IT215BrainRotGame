import pygame
import pygame.gfxdraw
from math import sin, cos, radians, degrees, atan2
import random
from button import Button

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        angle = random.uniform(0, 2 * 3.14159)  # Random direction
        speed = random.uniform(1, 3)  # Random initial speed
        self.vel_x = cos(angle) * speed
        self.vel_y = sin(angle) * speed
        self.gravity = 1

    def update(self, dt):
        self.vel_y += self.gravity * dt
        self.x += self.vel_x * dt * 60
        self.y += self.vel_y * dt * 60

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

class BallSimulation:
    def __init__(self, display_surface, sX, sY):
        self.display_surface = display_surface
        self.base_radius = 150
        self.base_box_width = int(display_surface.get_width() / 3)  # One third of screen width
        self.base_box_height = int(display_surface.get_height() * 2/3 + display_surface.get_height() // 6)  # Two thirds of screen height
        self.base_box_x = 50  # Fixed left position
        self.angle = 0
        self.rotation_speed = 2
        self.color = (182, 143, 64)  # RGB values for #b68f40
        self.balls = []
        self.spawn_button = None
        self.recalculate_layout(sX, sY)

    def recalculate_layout(self, sX, sY):
        # Scale all dimensions
        self.radius = int(self.base_radius * min(sX, sY))
        self.box_width = int(self.base_box_width * sX)
        self.box_height = int(self.base_box_height * sY)
        self.box_x = int(self.base_box_x * sX)
        self.box_y = (self.display_surface.get_height() - self.box_height) // 2
        self.center_x = self.box_x + self.box_width // 2
        self.center_y = self.box_y + self.box_height // 2
        self.line_thickness = max(1, int(3 * min(sX, sY)))

        # Create spawn button
        from pygame.font import Font
        font = Font("graphics/ui/NeotriadFree-1jzAg.ttf", int(20 * min(sX, sY)))
        self.spawn_button = Button(None, 
                                 (self.box_x, self.box_y + self.box_height + 20), 
                                 "Spawn Ball", 
                                 font, 
                                 "white", 
                                 "#b68f40")

    def update(self, dt, sX, sY):
        # Draw container box with scaled thickness
        pygame.draw.rect(self.display_surface, '#cccccc', 
                        (self.box_x, self.box_y, self.box_width, self.box_height), 
                        max(1, int(1 * min(sX, sY))))

        # Update angle and draw hollow circle with cutout
        self.angle = (self.angle + self.rotation_speed) % 360
        start_angle = radians(self.angle)
        end_angle = radians((self.angle + 330) % 360)  # 330 degrees creates a 30-degree gap

        # Draw arc with scaled thickness
        for i in range(self.line_thickness):
            pygame.gfxdraw.arc(self.display_surface, 
                            self.center_x, 
                            self.center_y, 
                            self.radius - i, 
                            int(degrees(start_angle)), 
                            int(degrees(end_angle)), 
                            self.color)

        # Update and draw balls
        for ball in self.balls[:]:
            ball.update(dt)
            # Check collision with circle
            dx = ball.x - self.center_x
            dy = ball.y - self.center_y
            distance = (dx * dx + dy * dy) ** 0.5

            if distance > self.radius - ball.radius:
                # Calculate angle of ball relative to circle center
                ball_angle = (degrees(atan2(dy, dx)) + 360) % 360
                # Check if ball is not in the gap (gap is 30 degrees)
                gap_start = self.angle
                gap_end = (self.angle + 30) % 360
                in_gap = False
                
                if gap_start < gap_end:
                    in_gap = gap_start <= ball_angle <= gap_end
                else:  # Gap crosses 0 degrees
                    in_gap = ball_angle >= gap_start or ball_angle <= gap_end
                
                if not in_gap:
                    # Simple bounce
                    ball.vel_x *= -0.8
                    ball.vel_y *= -0.8
                    # Move ball back to circle boundary
                    ball.x = self.center_x + (dx / distance) * (self.radius - ball.radius)
                    ball.y = self.center_y + (dy / distance) * (self.radius - ball.radius)

            
            # Remove balls that are too far outside
            if distance > self.radius * 2:
                self.balls.remove(ball)
                continue

            ball.draw(self.display_surface)

        # Update and draw spawn button
        self.spawn_button.update(self.display_surface)
        mouse_pos = pygame.mouse.get_pos()
        self.spawn_button.change_color(mouse_pos)

        # Check for button click
        if pygame.mouse.get_pressed()[0] and self.spawn_button.check_input(mouse_pos):
            self.spawn_ball(sX, sY)

    def spawn_ball(self, sX, sY):
        ball_radius = int(10 * min(self.display_surface.get_width()/1920, self.display_surface.get_height()/1080))
        new_ball = Ball(self.center_x, self.center_y, ball_radius)
        self.balls.append(new_ball)