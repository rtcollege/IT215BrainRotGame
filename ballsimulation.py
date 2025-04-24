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
        angle = random.uniform(0, 2 * 3.14159)
        speed = random.uniform(1, 3)
        self.vel_x = cos(angle) * speed
        self.vel_y = sin(angle) * speed
        self.gravity = 3
        # Store grid cell for spatial partitioning
        self.cell_x = 0
        self.cell_y = 0

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
        self.base_box_width = int(display_surface.get_width() / 3)
        self.base_box_height = int(display_surface.get_height() * 2/3 + display_surface.get_height() // 6)
        self.base_box_x = 50
        self.angle = 0
        self.rotation_speed = 1
        self.color = (182, 143, 64)
        self.balls = []
        self.circles = [{'radius': self.base_radius, 'active': True}] # Initialize with one circle
        self.spawn_button = None
        self.add_circle_button = None # Add a button for adding circles
        self.spawn_pressed = False
        self.circle_pressed = False

        # Grid parameters for spatial partitioning
        self.cell_size = 50  # Size of each grid cell
        self.grid = {}  # Dictionary to store balls in grid cells

        self.recalculate_layout(sX, sY)

        # Precalculate sin/cos values for rotation
        self.angle_cache = {}
        for angle in range(360):
            rad = radians(angle)
            self.angle_cache[angle] = (cos(rad), sin(rad))

    def get_grid_pos(self, x, y):
        return (int(x // self.cell_size), int(y // self.cell_size))

    def update_grid(self):
        self.grid.clear()
        for ball in self.balls:
            cell_x, cell_y = self.get_grid_pos(ball.x, ball.y)
            ball.cell_x, ball.cell_y = cell_x, cell_y
            cell_key = (cell_x, cell_y)
            if cell_key not in self.grid:
                self.grid[cell_key] = []
            self.grid[cell_key].append(ball)

    def get_nearby_balls(self, ball):
        nearby = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                cell_key = (ball.cell_x + dx, ball.cell_y + dy)
                if cell_key in self.grid:
                    nearby.extend(self.grid[cell_key])
        return nearby

    def recalculate_layout(self, sX, sY):
        self.radius = int(self.base_radius * min(sX, sY))
        self.box_width = int(self.base_box_width * sX)
        self.box_height = int(self.base_box_height * sY)
        self.box_x = int(self.base_box_x * sX)
        self.box_y = (self.display_surface.get_height() - self.box_height) // 2
        self.center_x = self.box_x + self.box_width // 2
        self.center_y = self.box_y + self.box_height // 2
        self.line_thickness = max(1, int(3 * min(sX, sY)))

        from pygame.font import Font
        font = Font("graphics/ui/NeotriadFree-1jzAg.ttf", int(20 * min(sX, sY)))
        self.spawn_button = Button(None, 
                                 (self.box_x, self.box_y + self.box_height + 20), 
                                 "Spawn Ball", 
                                 font, 
                                 "white", 
                                 "#b68f40")
        self.add_circle_button = Button(None, (self.box_x + self.spawn_button.rect.width + 20, self.box_y + self.box_height + 20), "Add Circle", font, "white", "#b68f40")


    def update(self, dt, sX, sY):
        pygame.draw.rect(self.display_surface, '#cccccc', 
                        (self.box_x, self.box_y, self.box_width, self.box_height), 
                        max(1, int(1 * min(sX, sY))))

        # Update rotating circle
        self.angle = (self.angle + self.rotation_speed) % 360
        cos_val, sin_val = self.angle_cache[self.angle]

        # Draw arc efficiently
        for i in range(self.line_thickness):
            for circle in self.circles:
                if circle['active']:
                    pygame.gfxdraw.arc(self.display_surface, 
                                    self.center_x, 
                                    self.center_y, 
                                    circle['radius'] - i, 
                                    self.angle, 
                                    (self.angle + 330) % 360, 
                                    self.color)

        # Update ball positions and grid
        for ball in self.balls[:]:
            ball.update(dt)
            
        self.update_grid()

        # Check collisions using spatial partitioning
        for ball in self.balls[:]:
            for circle_data in self.circles:
                if not circle_data['active']:
                    continue
                    
                dx = ball.x - self.center_x
                dy = ball.y - self.center_y
                distance_sq = dx * dx + dy * dy
                radius_diff = circle_data['radius'] - ball.radius
                
                if distance_sq > radius_diff * radius_diff:
                    # Calculate angle to check if ball is in gap
                    ball_angle = (degrees(atan2(dy, dx)) + 360) % 360
                    gap_start = self.angle
                    gap_end = (self.angle + 30) % 360
                    
                    in_gap = (gap_start < gap_end and gap_start <= ball_angle <= gap_end) or \
                            (gap_start > gap_end and (ball_angle >= gap_start or ball_angle <= gap_end))
                    
                    if not in_gap:
                        # Proper collision response
                        distance = distance_sq ** 0.5
                        normal_x = dx / distance
                        normal_y = dy / distance
                        
                        # Calculate reflection
                        dot_product = (ball.vel_x * normal_x + ball.vel_y * normal_y)
                        ball.vel_x = (ball.vel_x - 2 * dot_product * normal_x) * 0.8
                        ball.vel_y = (ball.vel_y - 2 * dot_product * normal_y) * 0.8
                        
                        # Prevent sticking by moving ball to circle boundary
                        ball.x = self.center_x + normal_x * radius_diff
                        ball.y = self.center_y + normal_y * radius_diff
            
            # Remove ball if it's too far from center
            dx = ball.x - self.center_x
            dy = ball.y - self.center_y
            if (dx * dx + dy * dy) > (self.radius * 2) * (self.radius * 2):
                self.balls.remove(ball)
                continue

            ball.draw(self.display_surface)


        self.spawn_button.update(self.display_surface)
        self.add_circle_button.update(self.display_surface) # Update the new button
        mouse_pos = pygame.mouse.get_pos()
        self.spawn_button.change_color(mouse_pos)
        self.add_circle_button.change_color(mouse_pos) # Change color for new button


        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed:
            if self.spawn_button.check_input(mouse_pos) and not self.spawn_pressed:
                self.spawn_ball(sX, sY)
                self.spawn_pressed = True
            if self.add_circle_button.check_input(mouse_pos) and not self.circle_pressed:
                self.add_circle(sX, sY)
                self.circle_pressed = True
        else:
            self.spawn_pressed = False
            self.circle_pressed = False


    def spawn_ball(self, sX, sY):
        ball_radius = int(10 * min(self.display_surface.get_width()/1920, self.display_surface.get_height()/1080))
        new_ball = Ball(self.center_x, self.center_y, ball_radius)
        self.balls.append(new_ball)

    def add_circle(self, sX, sY):
        if len(self.circles) >= 10:
            return  # Limit to 10 circles

        new_radius = max(10, self.circles[-1]['radius'] - 20)  # Reduce radius
        self.circles.append({'radius': new_radius, 'active': True})