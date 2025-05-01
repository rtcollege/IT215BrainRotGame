from settings import *
from data import Data
from timer import Timer
from button import Button
from ball import Ball
from circle import Circle
from particle import Particle
from math import sin, cos, radians, hypot, atan2, degrees
import random
import pygame.gfxdraw

class BallSimulation:
    """Handles ball physics simulation"""
    def __init__(self, display_surface, sX, sY, data):
        self.display_surface = display_surface
        self.data = data  # Use the passed data reference
        self.balls = []
        self.circles = []
        self.particles = [] # Initialize particles list
        self.circle_base_radius = 200
        self.ball_base_radius = 6
        self.base_padding = 100
        self.base_box_width = self.circle_base_radius * 2 + self.base_padding
        self.base_box_height = self.circle_base_radius * 2 + self.base_padding
        self.base_box_x = 100
        self.cell_size = 50
        self.grid = {}
        self.level = 1
        self.base_max_circles = 3  # Starting maximum number of circles
        self.base_ball_cost = 2
        self.can_spawn_circles = True
        self.spawn_timer = Timer(100, self.enable_circle_spawn)  # 1 second pause between levels
        self.min_radius_time = 0  # Track time at minimum radius
        self.base_damage = 1  # Base damage per second
        self.last_stat_update = pygame.time.get_ticks()
        self.stat_update_delay = 1000  # 1 second in milliseconds

        # Initialize buttons
        self.init_buttons()

        self.recalculate_layout(sX, sY)
        self.add_circle(sX, sY)

        self.angle_cache = {angle: (cos(radians(angle)), sin(radians(angle))) 
                          for angle in range(360)}
        self.button_pressed = False

    def init_buttons(self):
        """Initialize all buttons"""
        self.spawn_button = Button(None, (0, 0), "Spawn Ball", 
                                 pygame.font.Font(None, 24), "white", "#b68f40")

        # Initialize upgrade buttons
        self.multi_ball_button = Button(None, (0, 0), "Multi-Ball", 
                                      pygame.font.Font(None, 24), "white", "#b68f40")
        self.shrink_reduction_button = Button(None, (0, 0), "Shrink Reduction", 
                                            pygame.font.Font(None, 24), "white", "#b68f40")
        self.rotation_reduction_button = Button(None, (0, 0), "Rotation Reduction", 
                                              pygame.font.Font(None, 24), "white", "#b68f40")
        self.health_regen_button = Button(None, (0, 0), "Health Regen", 
                                        pygame.font.Font(None, 24), "white", "#b68f40")

    def recalculate_layout(self, sX, sY):
        """Recalculate simulation layout"""
        scale_factor = min(sX, sY)
        self.radius = int(self.circle_base_radius * scale_factor)
        self.box_width = int(self.base_box_width * sX)
        self.box_height = int(self.base_box_height * sY)
        self.box_x = int(self.base_box_x * sX)
        self.box_y = (self.display_surface.get_height() - self.box_height) // 2
        self.center_x = self.box_x + self.box_width // 2
        self.center_y = self.box_y + self.box_height // 2
        self.line_thickness = max(1, int(6 * scale_factor))
        self.scale_factor = scale_factor

        self.rescale_circles()
        self.rescale_balls()
        self.update_button_positions()

    def rescale_circles(self):
        """Rescale all circles based on new dimensions"""
        for circle in self.circles:
            new_initial = int(self.circle_base_radius * self.scale_factor)
            ratio = circle.radius / circle.initial_radius
            circle.radius = int(new_initial * ratio)
            circle.initial_radius = new_initial
            circle.min_radius = int(20 * self.scale_factor)
            circle.line_thickness = self.line_thickness
            circle.scale_factor = self.scale_factor

    def rescale_balls(self):
        """Rescale all balls based on new dimensions"""
        for ball in self.balls:
            ball.rescale(self.center_x, self.center_y, self.scale_factor, self.ball_base_radius)

    def update_button_positions(self):
        """Update positions of all buttons"""
        self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", 
                                   int(20 * self.scale_factor))

        # Position spawn button below circles
        button_y = self.box_y + self.box_height + int(30 * self.scale_factor)
        self.spawn_button.update_font(self.font)
        button_x = self.center_x - self.spawn_button.rect.width
        self.spawn_button.set_position((button_x, button_y))

        # Position upgrade buttons on the right side
        upgrade_x = self.box_x + self.box_width + int(50 * self.scale_factor)
        upgrade_y = self.box_y
        upgrade_spacing = int(60 * self.scale_factor)

        for i, button in enumerate([self.multi_ball_button, self.shrink_reduction_button, 
                                  self.rotation_reduction_button, self.health_regen_button]):
            button.update_font(self.font)
            button.set_position((upgrade_x, upgrade_y + i * upgrade_spacing))

    def enable_circle_spawn(self):
        """Enable circle spawning"""
        self.can_spawn_circles = True

    def get_current_ball_cost(self):
        """Calculate current ball cost"""
        return int(self.base_ball_cost * (1 + len(self.balls) * 0.2))

    def spawn_ball(self, sX, sY):
        """Spawn a new ball"""
        scale_factor = min(sX, sY)
        ball_radius = self.ball_base_radius * scale_factor
        for _ in range(1 + self.data.multi_ball_level):
            self.balls.append(Ball(self.center_x, self.center_y, ball_radius, 
                                 self.center_x, self.center_y))

    def add_circle(self, sX, sY):
        """Add a new circle to the game"""
        if not self.can_spawn_circles:
            return False

        active_circles = sum(1 for c in self.circles if c.active)
        max_circles = self.base_max_circles + (self.data.level - 1)
        if active_circles >= max_circles:
            return False

        scaled_radius = int(self.circle_base_radius * min(sX, sY))
        new_circle = Circle(scaled_radius, self.line_thickness, level=self.data.level)
        if not new_circle.check_collision(self.circles):
            self.circles.append(new_circle)
            return True
        return False

    def handle_collisions(self):
        """Handle ball collisions with circles"""
        for ball in self.balls[:]:
            dx = ball.x - self.center_x
            dy = ball.y - self.center_y
            dist = hypot(dx, dy)

            colliding_circles = []
            for circle in self.circles:
                if not circle.active:
                    continue

                distance_to_ring = abs(dist - circle.radius)
                collision_margin = self.line_thickness + ball.radius

                if distance_to_ring <= collision_margin:
                    angle = (degrees(atan2(dy, dx)) + 360) % 360
                    if circle.is_in_gap(angle):
                        self.handle_circle_destruction(circle)
                        break
                    colliding_circles.append((circle, distance_to_ring, collision_margin))

            if colliding_circles:
                self.resolve_collision(ball, colliding_circles)

    def handle_circle_destruction(self, circle):
        """Handle destroying a circle"""
        circle.active = False
        self.circles.remove(circle)  # Remove the inactive circle completely
        exp_gain = int((circle.initial_radius - circle.radius) / 2)
        currency_gain = int((circle.initial_radius - circle.radius) / 8)
        self.data.experience += max(10, exp_gain)
        self.data.currency += max(1, currency_gain)

        # Spawn particles
        for _ in range(25): # Spawn 30 particles
            angle = random.uniform(0, 2 * 3.14159)
            radius = circle.radius + random.uniform(0, 20) # Radius slightly outside circle
            x = self.center_x + radius * cos(angle)
            y = self.center_y + radius * sin(angle)
            self.particles.append(Particle(x, y, circle.color, self.scale_factor))

        # Check if we need to spawn new circles
        active_circles = [c for c in self.circles if c.active]
        if not active_circles:
            self.can_spawn_circles = False
            self.spawn_timer.activate()

    def resolve_collision(self, ball, colliding_circles):
        """Resolve ball collision with circles"""
        nearest_circle = min(colliding_circles, key=lambda x: x[1])
        circle, distance_to_ring, collision_margin = nearest_circle
        
        # Play bounce sound
        if 'bounce' in self.data.ui.music_manager.sounds:
            self.data.ui.music_manager.sounds['bounce'].play()

        dx = ball.x - self.center_x
        dy = ball.y - self.center_y
        dist = hypot(dx, dy)

        # Calculate collision response
        norm_dx = dx / dist
        norm_dy = dy / dist
        tang_dx = -norm_dy
        tang_dy = norm_dx

        norm_vel = ball.vel_x * norm_dx + ball.vel_y * norm_dy
        tang_vel = ball.vel_x * tang_dx + ball.vel_y * tang_dy

        energy_loss = max(0.85, 0.995 - (0.02 * (len(colliding_circles) - 1)))
        bounce_boost = 1.1
        norm_vel = -norm_vel * energy_loss * bounce_boost

        ball.vel_x = norm_vel * norm_dx + tang_vel * tang_dx
        ball.vel_y = norm_vel * norm_dy + tang_vel * tang_dy

        # Handle ball position
        penetration = collision_margin - distance_to_ring
        push_multiplier = 1 + (0.2 * (len(colliding_circles) - 1))

        if dist > circle.radius:
            ball.x -= norm_dx * (penetration + push_multiplier)
            ball.y -= norm_dy * (penetration + push_multiplier)
        else:
            ball.x += norm_dx * (penetration + push_multiplier)
            ball.y += norm_dy * (penetration + push_multiplier)

        target_dist = circle.radius + (collision_margin if dist > circle.radius else -collision_margin)
        ball.x = self.center_x + norm_dx * target_dist
        ball.y = self.center_y + norm_dy * target_dist

        # Apply drag
        ball.vel_x *= 0.995
        ball.vel_y *= 0.995

    def update(self, dt, sX, sY):
        """Update game state"""
        self.spawn_timer.update()
        self.update_health_and_currency(dt)
        self.draw_status_text(sX, sY)
        self.update_circles_and_balls(dt, sX, sY)
        self.handle_buttons()

    def update_health_and_currency(self, dt):
        """Update health and currency values"""
        if self.data.health < 100:
            regen_amount = self.data.health_regen_level * 2 * dt
            self.data.health = min(100, self.data.health + regen_amount)

        current_time = pygame.time.get_ticks()
        if current_time - self.last_stat_update >= self.stat_update_delay:
            self.data.currency += 1
            self.update_damage()
            self.last_stat_update = current_time

    def update_damage(self):
        """Update damage from minimum radius circles"""
        has_min_radius = any(circle.active and circle.radius <= circle.min_radius 
                           for circle in self.circles)
        if has_min_radius:
            self.min_radius_time += self.stat_update_delay / 1000
            damage = int(self.base_damage * (1 + self.min_radius_time / 5))
            self.data.health = max(0, self.data.health - damage)
        else:
            self.min_radius_time = 0

    def draw_status_text(self, sX, sY):
        """Draw health and currency status"""
        status_x = int(20 * sX)
        status_y = int(20 * sY)
        spacing = int(40 * sY)

        health_text = self.font.render(f"Health: {int(self.data.health)}", True, "white")
        currency_text = self.font.render(f"Currency: {self.data.currency}", True, "white")

        self.display_surface.blit(health_text, (status_x, status_y))
        self.display_surface.blit(currency_text, (status_x, status_y + spacing))

    def update_circles_and_balls(self, dt, sX, sY):
        """Update and draw circles and balls"""
        active_circles = [c for c in self.circles if c.active]

        if not active_circles and self.can_spawn_circles:
            max_circles = self.base_max_circles + (self.data.level - 1)
            for _ in range(max_circles):
                self.add_circle(sX, sY)
        elif not active_circles:
            self.circles.clear()

        for circle in self.circles:
            circle.update(dt, self.circles, self.data.level)
            circle.draw(self.display_surface, self.center_x, self.center_y,
                      self.line_thickness, circle.color, pygame.gfxdraw)

        for ball in self.balls[:]:
            ball.update(dt)
            if ball.y > self.display_surface.get_height():
                self.balls.remove(ball)
                refund = self.get_current_ball_cost() // 8
                self.data.currency += refund
            else:
                ball.draw(self.display_surface)

        self.particles = [p for p in self.particles if p.is_alive()] #remove dead particles
        for particle in self.particles:
            particle.update(dt)
            particle.draw(self.display_surface) #Draw particles

        self.handle_collisions()
        self.add_circle(sX, sY)

    def handle_buttons(self):
        """Handle button updates and interactions"""
        mouse_pos = pygame.mouse.get_pos()

        # Spawn button
        self.spawn_button.update(self.display_surface)
        self.spawn_button.change_color(mouse_pos)

        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Always update and draw buttons regardless of pressed state
        upgrade_buttons = [
            (self.multi_ball_button, '_multi_ball_level'),
            (self.shrink_reduction_button, '_shrink_reduction_level'),
            (self.rotation_reduction_button, '_rotation_reduction_level'),
            (self.health_regen_button, '_health_regen_level')
        ]

        for button, attr in upgrade_buttons:
            current_level = getattr(self.data, attr)
            cost = self.data.get_upgrade_cost(current_level)

            button.text_input = button.text_input.split(':')[0]
            button.update(self.display_surface)
            button.change_color(mouse_pos)

            # Draw cost text
            cost_text = self.font.render(str(cost), True, "white")
            cost_x = button.rect.right + 20
            cost_y = button.rect.centery - cost_text.get_height() // 2
            self.display_surface.blit(cost_text, (cost_x, cost_y))

        # Update spawn button and show cost
        self.spawn_button.update(self.display_surface)
        self.spawn_button.change_color(mouse_pos)
        
        # Display ball cost
        ball_cost = self.get_current_ball_cost()
        cost_text = self.font.render(f"Cost: {ball_cost}", True, "white")
        cost_x = self.spawn_button.rect.right + int(20 * self.scale_factor)
        cost_y = self.spawn_button.rect.centery - cost_text.get_height() // 2
        self.display_surface.blit(cost_text, (cost_x, cost_y))

        if not mouse_pressed:
            self.button_pressed = False
        elif not self.button_pressed:
            # Handle spawn button click
            if self.spawn_button.check_input(mouse_pos):
                ball_cost = self.get_current_ball_cost()
                if self.data.currency >= ball_cost:
                    self.spawn_ball(self.scale_factor, self.scale_factor)
                    self.data.currency -= ball_cost
                    self.button_pressed = True

            # Handle upgrade button clicks
            for button, attr in upgrade_buttons:
                if button.check_input(mouse_pos):
                    current_level = getattr(self.data, attr)
                    cost = self.data.get_upgrade_cost(current_level)
                    if self.data.currency >= cost:
                        setattr(self.data, attr, current_level + 1)
                        self.data.currency -= cost
                        self.button_pressed = True
                        break

    def draw(self):
        """Draw the simulation"""
        # Draw circles
        for circle in self.circles:
            circle.draw(self.display_surface, self.center_x, self.center_y,
                       self.line_thickness, circle.color, pygame.gfxdraw)

        # Draw balls
        for ball in self.balls:
            ball.draw(self.display_surface)

        # Draw particles
        for particle in self.particles:
            particle.draw(self.display_surface)