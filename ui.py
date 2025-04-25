from settings import *
from data import Data
from debug import debug
from dropdown import Dropdown
from timer import Timer
from button import Button
from ball import Ball
from circle import Circle
from math import sin, cos, radians, hypot, atan2, degrees
import random
import pygame.gfxdraw
import sys

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.base_font_size = 40
        self.frames = frames
        self.font = font

        # Core state
        self.current_scene = 'main_menu'
        self.previous_scene = 'main_menu'
        self.is_paused = False
        self.difficulty = 'medium'
        self.volume = 75

        # Window dimensions
        self.W_WIDTH = WINDOW_WIDTH
        self.W_HEIGHT = WINDOW_HEIGHT
        self.sX = SCALE_X
        self.sY = SCALE_Y

        # Initialize ball simulation
        self.ball_sim = BallSimulation(self.display_surface, self.sX, self.sY)

        # Initialize UI elements
        self.init_buttons()
        self.init_resolution_buttons()

        # Calculate initial layout
        self.recalculate_layout()

    def init_buttons(self):
        """Initialize all button objects"""
        button_configs = [
            ('play_button', "Play"),
            ('settings_button', "Settings"), 
            ('credits_button', "Credits"),
            ('quit_button', "Quit"),
            ('easy_button', "Easy"),
            ('medium_button', "Medium"), 
            ('hard_button', "Hard"),
            ('back_button', "Back"),
            ('resume_button', "Resume"),
            ('pause_settings_button', "Settings"),
            ('pause_credits_button', "Credits"),
            ('pause_main_menu_button', "Main Menu")
        ]

        for attr_name, text in button_configs:
            setattr(self, attr_name, Button(None, (0, 0), text, self.font, "white", "#b68f40"))

    def init_resolution_buttons(self):
        """Initialize resolution buttons"""
        self.resolution_buttons = []
        for width, height in RESOLUTIONS:
            btn = Button(None, (0, 0), f"{width}x{height}", self.font, "white", "#b68f40")
            self.resolution_buttons.append((btn, (width, height)))

    def recalculate_layout(self):
        """Recalculate all UI element positions and sizes"""
        # Layout constants
        button_x = int(50 * self.sX)
        button_y_start = int(300 * self.sY)
        button_y_spacing = int(100 * self.sY)

        # Update fonts
        self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", 
                                   int(self.base_font_size * min(self.sX, self.sY)))
        self.title_font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", 
                                         int(self.base_font_size * 1.5 * min(self.sX, self.sY)))

        # Initialize title texts
        self.title_text = self.title_font.render("Brain Rot Game", True, "white")
        self.title_rect = self.title_text.get_rect(topleft=(button_x, int(100 * self.sY)))
        
        # Update back button position to match main menu buttons
        back_button_x = int(50 * self.sX)  # Same as button_x
        back_button_y = button_y_start + 3 * button_y_spacing
        self.back_button = Button(None, (back_button_x, back_button_y), "Back", 
                                self.font, "white", "#b68f40")

        # Add difficulty text
        self.difficulty_text = self.font.render("Difficulty:", True, "white")
        text_height = self.difficulty_text.get_height()
        self.difficulty_text_rect = self.difficulty_text.get_rect(
            topleft=(back_button_x, int(400 * self.sY) - text_height/2))

        # Layout constants
        button_x = int(50 * self.sX)
        button_y_start = int(300 * self.sY)
        button_y_spacing = int(100 * self.sY)

        # Update main menu buttons
        menu_buttons = [self.play_button, self.settings_button, 
                       self.credits_button, self.quit_button]
        for i, button in enumerate(menu_buttons):
            button.update_font(self.font)
            button.set_position((button_x, button_y_start + i * button_y_spacing))

        # Update settings layout
        self.setup_volume_slider(button_x)
        self.setup_difficulty_buttons(button_x)
        self.setup_resolution_dropdown(button_x)

        # Update credits layout
        self.setup_credits_text(button_x)

        # Update pause menu layout
        self.setup_pause_menu(button_x, button_y_start, button_y_spacing)

        # Update ball simulation layout
        self.ball_sim.recalculate_layout(self.sX, self.sY)

        # Main menu title
        self.title_text = self.title_font.render("Brain Rot Game", True, "white")
        self.title_rect = self.title_text.get_rect(topleft=(button_x, int(100 * self.sY)))

        # Settings title
        self.settings_title = self.title_font.render("Settings", True, "white")
        self.settings_title_rect = self.settings_title.get_rect(topleft=(button_x, int(100 * self.sY)))

        # Credits title
        self.credits_title = self.title_font.render("Credits", True, "white")
        self.credits_title_rect = self.credits_title.get_rect(topleft=(button_x, int(100 * self.sY)))

        # Pause title
        self.pause_title = self.title_font.render("Paused", True, "white")
        self.pause_title_rect = self.pause_title.get_rect(topleft=(button_x, int(100 * self.sY)))


    def setup_volume_slider(self, button_x):
        """Set up volume slider elements"""
        volume_y = int(250 * self.sY)
        self.volume_text = self.font.render("Volume:", True, "white")
        text_height = self.volume_text.get_height()
        self.volume_text_rect = self.volume_text.get_rect(
            topleft=(button_x, volume_y - text_height // 2))

        self.slider_width = int(200 * self.sX)
        self.volume_rect = pygame.Rect(
            self.W_WIDTH // 2 - self.slider_width // 2, 
            volume_y,
            self.slider_width, 
            int(20 * self.sY)
        )

        slider_x = self.W_WIDTH // 2 - self.slider_width // 2 + int(
            (self.volume / 100) * self.slider_width)
        self.volume_slider = pygame.Rect(
            slider_x,
            volume_y - int(5 * self.sY),
            int(20 * self.sX),
            int(30 * self.sY)
        )

    def setup_difficulty_buttons(self, button_x):
        """Set up difficulty selection buttons"""
        diff_y = int(400 * self.sY)
        button_spacing = int(200 * self.sX)
        center_x = self.W_WIDTH / 2

        # Position difficulty text
        self.difficulty_text = self.font.render("Difficulty:", True, "white")
        text_height = self.difficulty_text.get_height()
        self.difficulty_text_rect = self.difficulty_text.get_rect(
            topleft=(button_x, diff_y - text_height/2))

        for button, x_offset in [(self.easy_button, -1), 
                                (self.medium_button, 0), 
                                (self.hard_button, 1)]:
            button.update_font(self.font)
            button.set_position((center_x + x_offset * button_spacing - 
                               button.text.get_width() // 2, diff_y))

    def setup_resolution_dropdown(self, button_x):
        """Set up resolution dropdown menu"""
        res_y = int(500 * self.sY)
        dropdown_width = int(220 * self.sX)
        dropdown_height = int(40 * self.sY)

        resolution_options = [f"{width}x{height}" for width, height in RESOLUTIONS]
        current_res = f"{self.W_WIDTH}x{self.W_HEIGHT}"

        self.resolution_text = self.font.render("Resolution:", True, "white")
        text_height = self.resolution_text.get_height()
        self.resolution_text_rect = self.resolution_text.get_rect(
            topleft=(button_x, res_y - text_height // 2))

        self.resolution_dropdown = Dropdown(
            button_x + self.resolution_text.get_width() + int(40 * self.sX),
            res_y,
            dropdown_width,
            dropdown_height,
            resolution_options,
            self.font,
            current_res
        )

        self.apply_button = Button(
            None,
            (self.resolution_dropdown.rect.right + int(20 * self.sX), res_y),
            "Apply", self.font, "white", "#b68f40")

    def setup_credits_text(self, button_x):
        credits_lines = [
            "Lead Developer: John Doe", "Art Director: Jane Smith",
            "Sound Designer: Mike Johnson", "Level Designer: Sarah Wilson"
        ]
        self.credits_texts = []
        self.credits_rects = []

        for i, line in enumerate(credits_lines):
            text = self.font.render(line, True, "white")
            rect = text.get_rect(center=(self.W_WIDTH // 2,
                                         self.W_HEIGHT // 2 - 100 +
                                         i * 50 * self.sY))
            self.credits_texts.append(text)
            self.credits_rects.append(rect)

    def setup_pause_menu(self, button_x, button_y_start, button_y_spacing):
        self.resume_button.update_font(self.font)
        self.pause_settings_button.update_font(self.font)
        self.pause_credits_button.update_font(self.font)
        self.pause_main_menu_button.update_font(self.font)

        self.resume_button.set_position((button_x, button_y_start))
        self.pause_settings_button.set_position((button_x, button_y_start + button_y_spacing))
        self.pause_credits_button.set_position((button_x, button_y_start + 2 * button_y_spacing))
        self.pause_main_menu_button.set_position((button_x, button_y_start + 3 * button_y_spacing))

    def update(self, dt):
        """Update UI state and render elements"""
        mouse_pos = pygame.mouse.get_pos()
        self.draw_background()

        scene_methods = {
            'main_menu': self.update_main_menu,
            'settings': self.update_settings,
            'credits': self.update_credits,
            'gameplay': self.update_gameplay
        }

        if self.current_scene in scene_methods:
            scene_methods[self.current_scene](mouse_pos, dt)

    def draw_background(self):
        """Draw gradient background"""
        background = pygame.Surface((self.W_WIDTH, self.W_HEIGHT))
        for y in range(self.W_HEIGHT):
            factor = y / self.W_HEIGHT
            color = pygame.Color(
                int(44 * (1 - factor) + 26 * factor),
                int(44 * (1 - factor) + 26 * factor),
                int(44 * (1 - factor) + 26 * factor)
            )
            pygame.draw.line(background, color, (0, y), (self.W_WIDTH, y))
        self.display_surface.blit(background, (0, 0))

    def update_main_menu(self, mouse_pos, dt):
        self.display_surface.blit(self.title_text, self.title_rect)
        for button in [self.play_button, self.settings_button, self.credits_button, self.quit_button]:
            button.update(self.display_surface)
            button.change_color(mouse_pos)

    def update_settings(self, mouse_pos, dt):
        self.display_surface.blit(self.settings_title, self.settings_title_rect)
        self.display_surface.blit(self.volume_text, self.volume_text_rect)
        self.display_surface.blit(self.difficulty_text, self.difficulty_text_rect)
        pygame.draw.rect(self.display_surface, "white", self.volume_rect, 2)
        pygame.draw.rect(self.display_surface, "white", self.volume_slider)

        # Handle continuous volume slider dragging
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            if self.volume_rect.collidepoint(mouse_pos) or self.volume_slider.collidepoint(mouse_pos):
                self.update_volume_from_mouse(mouse_pos[0])

        volume_value = self.font.render(f"{int(self.volume)}%", True, "white")
        volume_value_rect = volume_value.get_rect(midleft=(self.volume_rect.right + 20, self.volume_rect.centery))
        self.display_surface.blit(volume_value, volume_value_rect)

        self.display_surface.blit(self.resolution_text, self.resolution_text_rect)
        self.resolution_dropdown.draw(self.display_surface)
        self.apply_button.update(self.display_surface)
        self.apply_button.change_color(mouse_pos)

        for button in [self.easy_button, self.medium_button, self.hard_button]:
            button.update(self.display_surface)
        if self.difficulty == 'easy':
            pygame.draw.rect(self.display_surface, "white", self.easy_button.rect, 3)
        elif self.difficulty == 'medium':
            pygame.draw.rect(self.display_surface, "white", self.medium_button.rect, 3)
        elif self.difficulty == 'hard':
            pygame.draw.rect(self.display_surface, "white", self.hard_button.rect, 3)


        self.back_button.update(self.display_surface)
        self.back_button.change_color(mouse_pos)

    def update_credits(self, mouse_pos, dt):
        self.display_surface.blit(self.credits_title, self.credits_title_rect)
        for text, rect in zip(self.credits_texts, self.credits_rects):
            self.display_surface.blit(text, rect)
        self.back_button.update(self.display_surface)
        self.back_button.change_color(mouse_pos)

    def update_gameplay(self, mouse_pos, dt):
        if not self.is_paused:
            self.ball_sim.update(dt, self.sX, self.sY)
        else:
            overlay = pygame.Surface((self.W_WIDTH, self.W_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(96)
            self.display_surface.blit(overlay, (0, 0))
            self.display_surface.blit(self.pause_title, self.pause_title_rect)
            for button in [self.resume_button, self.pause_settings_button, self.pause_credits_button, self.pause_main_menu_button]:
                button.update(self.display_surface)
                button.change_color(mouse_pos)

    def handle_events(self, event):
        """Handle UI events"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.current_scene == 'gameplay':
                self.is_paused = not self.is_paused
            elif self.current_scene in ['settings', 'credits']:
                self.switch_scene(self.previous_scene)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event)

        if event.type == pygame.MOUSEBUTTONDOWN and self.current_scene == 'settings':
            self.resolution_dropdown.handle_event(event)


    def handle_mouse_click(self, event):
        """Handle mouse click events"""
        mouse_pos = pygame.mouse.get_pos()

        scene_handlers = {
            'main_menu': self.handle_main_menu_click,
            'settings': self.handle_settings_click,
            'credits': self.handle_credits_click,
            'gameplay': self.handle_gameplay_click
        }

        if self.current_scene in scene_handlers:
            scene_handlers[self.current_scene](mouse_pos)

    def handle_main_menu_click(self, mouse_pos):
        if self.play_button.check_input(mouse_pos):
            self.switch_scene('gameplay')
            self.is_paused = False
        elif self.settings_button.check_input(mouse_pos):
            self.switch_scene('settings')
        elif self.credits_button.check_input(mouse_pos):
            self.switch_scene('credits')
        elif self.quit_button.check_input(mouse_pos):
            pygame.quit()
            sys.exit()

    def handle_settings_click(self, mouse_pos):
        if self.back_button.check_input(mouse_pos):
            self.switch_scene(self.previous_scene)
        elif self.easy_button.check_input(mouse_pos):
            self.difficulty = 'easy'
        elif self.medium_button.check_input(mouse_pos):
            self.difficulty = 'medium'
        elif self.hard_button.check_input(mouse_pos):
            self.difficulty = 'hard'
        elif self.volume_rect.collidepoint(mouse_pos) or self.volume_slider.collidepoint(mouse_pos):
            # Update volume based on mouse position
            self.update_volume_from_mouse(mouse_pos[0])

    def update_volume_from_mouse(self, mouse_x):
        # Calculate volume based on mouse position relative to slider
        left_edge = self.W_WIDTH // 2 - self.slider_width // 2
        right_edge = left_edge + self.slider_width
        clamped_x = max(left_edge, min(right_edge, mouse_x))
        relative_x = clamped_x - left_edge
        self.volume = ((relative_x / self.slider_width) * 100)
        self.volume = max(0, min(100, self.volume))
        # Update slider position with proper scaling
        self.volume_slider.x = int(left_edge + (self.volume * self.slider_width / 100) - (self.volume_slider.width // 2))
        self.volume_slider.y = int(245 * self.sY)  # Update Y position with scaling

    def handle_settings_click(self, mouse_pos):
        if self.back_button.check_input(mouse_pos):
            self.switch_scene(self.previous_scene)
        elif self.easy_button.check_input(mouse_pos):
            self.difficulty = 'easy'
        elif self.medium_button.check_input(mouse_pos):
            self.difficulty = 'medium'
        elif self.hard_button.check_input(mouse_pos):
            self.difficulty = 'hard'
        elif self.volume_rect.collidepoint(mouse_pos) or self.volume_slider.collidepoint(mouse_pos):
            self.update_volume_from_mouse(mouse_pos[0])
        elif self.apply_button.check_input(mouse_pos):
            selected_res = self.resolution_dropdown.selected_option
            width, height = map(int, selected_res.split('x'))
            pygame.display.set_mode((width, height))
            self.W_WIDTH = width
            self.W_HEIGHT = height
            self.sX = width / BASE_WIDTH
            self.sY = height / BASE_HEIGHT
            self.recalculate_layout()
            slider_x = self.W_WIDTH // 2 - self.slider_width // 2 + int((self.volume / 100) * self.slider_width)
            self.volume_slider.x = slider_x


    def handle_credits_click(self, mouse_pos):
        if self.back_button.check_input(mouse_pos):
            self.switch_scene(self.previous_scene)

    def handle_gameplay_click(self, mouse_pos):
        if self.is_paused:
            if self.resume_button.check_input(mouse_pos):
                self.is_paused = False
            elif self.pause_settings_button.check_input(mouse_pos):
                self.switch_scene('settings')
            elif self.pause_credits_button.check_input(mouse_pos):
                self.switch_scene('credits')
            elif self.pause_main_menu_button.check_input(mouse_pos):
                self.switch_scene('main_menu')

    def switch_scene(self, new_scene):
        """Switch to a new scene"""
        self.previous_scene = self.current_scene
        self.current_scene = new_scene


class BallSimulation:
    """Handles ball physics simulation"""
    def __init__(self, display_surface, sX, sY):
        self.display_surface = display_surface
        self.balls = []
        self.circles = []
        self.base_radius = 150
        self.base_padding = 100
        self.base_box_width = self.base_radius * 2 + self.base_padding
        self.base_box_height = self.base_radius * 2 + self.base_padding
        self.base_box_x = 100
        self.cell_size = 50
        self.grid = {}

        self.spawn_button = Button(None, (0, 0), "Spawn Ball", 
                                 pygame.font.Font(None, 24), "white", "#b68f40")
        self.add_circle_button = Button(None, (0, 0), "Add Circle", 
                                      pygame.font.Font(None, 24), "white", "#b68f40")

        self.recalculate_layout(sX, sY)
        self.add_circle(sX, sY)

        self.angle_cache = {angle: (cos(radians(angle)), sin(radians(angle))) 
                           for angle in range(360)}
        self.spawn_pressed = False
        self.circle_pressed = False

    def recalculate_layout(self, sX, sY):
        """Recalculate simulation layout"""
        self.radius = int(self.base_radius * min(sX, sY))
        self.box_width = int(self.base_box_width * sX)
        self.box_height = int(self.base_box_height * sY)
        self.box_x = int(self.base_box_x * sX)
        self.box_y = (self.display_surface.get_height() - self.box_height) // 2
        self.center_x = self.box_x + self.box_width // 2
        self.center_y = self.box_y + self.box_height // 2
        self.line_thickness = max(1, int(6 * min(sX, sY)))

        self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", 
                                   int(20 * min(sX, sY)))

        button_spacing = int(30 * min(sX, sY))
        button_y = self.box_y + self.box_height + (button_spacing * 1.5)

        self.spawn_button.update_font(self.font)
        self.add_circle_button.update_font(self.font)

        self.spawn_button.set_position((self.box_x + button_spacing, button_y))
        self.add_circle_button.set_position(
            (self.box_x + button_spacing + self.spawn_button.rect.width + 
             button_spacing, button_y))

    def spawn_ball(self, sX, sY):
        ball_radius = int(6 * min(sX, sY))
        self.balls.append(Ball(self.center_x, self.center_y, ball_radius))

    def add_circle(self, sX, sY):
        active_circles = sum(1 for c in self.circles if c.active)
        if active_circles >= 7:
            return

        if not self.circles or active_circles == 0:
            self.circles.append(Circle(self.base_radius))
        else:
            active_radii = sorted([c.radius for c in self.circles if c.active], reverse=True)
            if not active_radii or active_radii[0] < self.base_radius:
                # If no active circles or largest active is smaller than base, add base sized circle
                self.circles.append(Circle(self.base_radius))
            else:
                # Find the largest gap in the sequence of radii
                new_radius = self.base_radius
                for i in range(len(active_radii)):
                    if i < len(active_radii) - 1:
                        gap = active_radii[i] - active_radii[i + 1]
                        if gap > 20:  # If there's a gap bigger than minimum step
                            new_radius = active_radii[i] - 20
                            break
                    else:  # Last element
                        new_radius = max(8, active_radii[i] - 20)

                if new_radius >= 7:  # Only add if radius is valid
                    self.circles.append(Circle(new_radius))

    def handle_collisions(self):
        for ball in self.balls[:]:
            dx = ball.x - self.center_x
            dy = ball.y - self.center_y
            dist = hypot(dx, dy)

            # Find all colliding circles
            colliding_circles = []
            for circle in self.circles:
                if not circle.active:
                    continue

                distance_to_ring = abs(dist - circle.radius)
                collision_margin = self.line_thickness + ball.radius

                if distance_to_ring <= collision_margin:
                    angle = (degrees(atan2(dy, dx)) + 360) % 360
                    if circle.is_in_gap(angle):
                        circle.active = False
                        break
                    colliding_circles.append((circle, distance_to_ring, collision_margin))

            if not colliding_circles:
                continue

            # Handle collision with the nearest circle
            nearest_circle = min(colliding_circles, key=lambda x: x[1])
            circle, distance_to_ring, collision_margin = nearest_circle

            # Calculate normalized direction vectors
            norm_dx = dx / dist
            norm_dy = dy / dist

            # Calculate tangent vector (perpendicular to normal)
            tang_dx = -norm_dy
            tang_dy = norm_dx

            # Decompose velocity into normal and tangential components
            norm_vel = ball.vel_x * norm_dx + ball.vel_y * norm_dy
            tang_vel = ball.vel_x * tang_dx + ball.vel_y * tang_dy

            # Reflect normal component with increased energy loss for multiple collisions
            energy_loss = 0.99 - (0.05 * (len(colliding_circles) - 1))  # More energy loss with more collisions
            energy_loss = max(0.5, energy_loss)  # Don't let it go below 0.5
            norm_vel = -norm_vel * energy_loss

            # Reconstruct velocity vector
            ball.vel_x = norm_vel * norm_dx + tang_vel * tang_dx
            ball.vel_y = norm_vel * norm_dy + tang_vel * tang_dy

            # Push ball out with increased push for multiple collisions
            penetration = collision_margin - distance_to_ring
            push_multiplier = 1 + (0.2 * (len(colliding_circles) - 1))  # Stronger push with more collisions
            if dist > circle.radius:  # Ball is outside ring
                ball.x -= norm_dx * (penetration + push_multiplier)
                ball.y -= norm_dy * (penetration + push_multiplier)
            else:  # Ball is inside ring
                ball.x += norm_dx * (penetration + push_multiplier)
                ball.y += norm_dy * (penetration + push_multiplier)

            # Clamp ball position to exactly the ring surface
            target_dist = circle.radius + (collision_margin if dist > circle.radius else -collision_margin)
            ball.x = self.center_x + norm_dx * target_dist
            ball.y = self.center_y + norm_dy * target_dist

            # Add drag/friction over time to slow balls
            drag = 0.98
            ball.vel_x *= drag
            ball.vel_y *= drag

    def update(self, dt, sX, sY):
        for circle in self.circles:
            circle.update(dt, self.circles)
            circle.draw(self.display_surface, self.center_x, self.center_y,
                        self.line_thickness, (182, 143, 64), pygame.gfxdraw)

        for ball in self.balls:
            ball.update(dt)

        self.handle_collisions()

        for ball in self.balls[:]:
            if ball.y > self.display_surface.get_height():
                self.balls.remove(ball)
            else:
                ball.draw(self.display_surface)

        # Button UI
        self.spawn_button.update(self.display_surface)
        self.add_circle_button.update(self.display_surface)
        mouse_pos = pygame.mouse.get_pos()
        self.spawn_button.change_color(mouse_pos)
        self.add_circle_button.change_color(mouse_pos)
        if pygame.mouse.get_pressed()[0]:
            if self.spawn_button.check_input(mouse_pos) and not self.spawn_pressed:
                self.spawn_ball(sX, sY)
                self.spawn_pressed = True
            if self.add_circle_button.check_input(mouse_pos) and not self.circle_pressed:
                self.add_circle(sX, sY)
                self.circle_pressed = True
        else:
            self.spawn_pressed = False
            self.circle_pressed = False