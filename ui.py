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
    def __init__(self, font, frames, data):
        self.display_surface = pygame.display.get_surface()
        self.base_font_size = 40
        self.frames = frames
        self.font = font
        self.data = data

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
            ('pause_main_menu_button', "Main Menu"),
            ('restart_button', "Restart")
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
        if self.ball_sim.health <= 0:
            # Draw the current state without updating
            # Draw status text
            status_x = int(20 * self.sX)
            status_y = int(20 * self.sY)
            spacing = int(40 * self.sY)

            health_text = self.ball_sim.font.render(f"Health: {self.ball_sim.health}", True, "white")
            currency_text = self.ball_sim.font.render(f"Currency: {self.ball_sim.currency}", True, "white")

            self.display_surface.blit(health_text, (status_x, status_y))
            self.display_surface.blit(currency_text, (status_x, status_y + spacing))

            # Draw level and experience bar
            # Experience bar
            exp_bar_width = int(300 * self.sX)
            exp_bar_height = int(20 * self.sY)
            exp_bar_x = self.ball_sim.box_x
            exp_bar_y = self.ball_sim.box_y - 50

            # Draw background
            exp_bar_bg = pygame.Rect(exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height)
            pygame.draw.rect(self.display_surface, "black", exp_bar_bg)
            pygame.draw.rect(self.display_surface, "white", exp_bar_bg, 2)

            # Draw progress
            exp_needed = self.data.get_exp_for_level(self.data.level)
            progress = self.data.experience / exp_needed
            if progress > 0:
                fill_width = int(exp_bar_width * progress)
                fill_rect = pygame.Rect(exp_bar_x, exp_bar_y, fill_width, exp_bar_height)
                pygame.draw.rect(self.display_surface, (255, 215, 0), fill_rect)  # Gold color

            # Draw all circles in their current state
            for circle in self.ball_sim.circles:
                circle.draw(self.display_surface, self.ball_sim.center_x, self.ball_sim.center_y,
                            self.ball_sim.line_thickness, (182, 143, 64), pygame.gfxdraw)

            # Draw all balls in their current state
            for ball in self.ball_sim.balls:
                ball.draw(self.display_surface)

            # Show game over overlay
            overlay = pygame.Surface((self.W_WIDTH, self.W_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.display_surface.blit(overlay, (0, 0))

            game_over_text = self.title_font.render("Game Over", True, "white")
            game_over_rect = game_over_text.get_rect(center=(self.W_WIDTH // 2, self.W_HEIGHT // 2 - 50))
            self.display_surface.blit(game_over_text, game_over_rect)

            # Position restart button below text
            self.restart_button.update_font(self.font)
            self.restart_button.set_position((self.W_WIDTH // 2 - self.restart_button.rect.width // 2, 
                                            self.W_HEIGHT // 2 + 50))
            self.restart_button.update(self.display_surface)
            self.restart_button.change_color(mouse_pos)
        elif not self.is_paused:
            # Draw level and experience bar
            # Experience bar
            exp_bar_width = int(300 * self.sX)
            exp_bar_height = int(20 * self.sY)
            exp_bar_x = self.ball_sim.center_x - exp_bar_width // 2
            exp_bar_y = self.ball_sim.box_y - 50

            # Draw background
            exp_bar_bg = pygame.Rect(exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height)
            pygame.draw.rect(self.display_surface, "black", exp_bar_bg)
            pygame.draw.rect(self.display_surface, "white", exp_bar_bg, 2)

            # Draw progress
            exp_needed = self.ball_sim.data.get_exp_for_level(self.ball_sim.data.level)
            progress = self.ball_sim.data.experience / exp_needed
            if progress > 0:
                fill_width = int(exp_bar_width * progress)
                fill_rect = pygame.Rect(exp_bar_x, exp_bar_y, fill_width, exp_bar_height)
                pygame.draw.rect(self.display_surface, (255, 215, 0), fill_rect)  # Gold color

            # Draw level text centered in exp bar
            level_text = self.ball_sim.font.render(f"Level: {self.ball_sim.data.level}", True, "white")
            level_rect = level_text.get_rect(center=(exp_bar_x + exp_bar_width // 2, exp_bar_y + exp_bar_height // 2))
            self.display_surface.blit(level_text, level_rect)

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
        if self.ball_sim.health <= 0:
            if self.restart_button.check_input(mouse_pos):
                # Reset game state
                self.ball_sim = BallSimulation(self.display_surface, self.sX, self.sY)
                self.is_paused = False
        elif self.is_paused:
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
        self.data = Data(None)  # Initialize with None since we don't need UI reference
        self.balls = []
        self.circles = []
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
        self.health = 100
        self.min_radius_time = 0  # Track time at minimum radius
        self.base_damage = 1  # Base damage per second
        self.currency = 0
        self.last_stat_update = pygame.time.get_ticks()
        self.stat_update_delay = 1000  # 1 second in milliseconds

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

        self.recalculate_layout(sX, sY)
        self.add_circle(sX, sY)

        self.angle_cache = {angle: (cos(radians(angle)), sin(radians(angle))) 
                           for angle in range(360)}
        self.spawn_pressed = False
        self.circle_pressed = False

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

        # Rescale all circles
        for circle in self.circles:
            # Scale radius directly from base radius
            new_initial = int(self.circle_base_radius * scale_factor)
            ratio = circle.radius / circle.initial_radius
            circle.radius = int(new_initial * ratio)
            circle.initial_radius = new_initial
            circle.min_radius = int(20 * scale_factor)  # Scale minimum radius too
            circle.line_thickness = self.line_thickness
            circle.scale_factor = scale_factor

        # Rescale all balls
        for ball in self.balls:
            ball.rescale(self.center_x, self.center_y, scale_factor, self.ball_base_radius)

        self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", 
                                   int(20 * scale_factor))

        # Position spawn button below circles
        button_y = self.box_y + self.box_height + int(30 * scale_factor)
        self.spawn_button.update_font(self.font)
        button_x = self.center_x - (self.spawn_button.rect.width // 2)
        self.spawn_button.set_position((button_x, button_y))

        # Position upgrade buttons on the right side
        upgrade_x = self.box_x + self.box_width + int(50 * scale_factor)
        upgrade_y = self.box_y
        upgrade_spacing = int(60 * scale_factor)

        for i, button in enumerate([self.multi_ball_button, self.shrink_reduction_button, 
                                  self.rotation_reduction_button, self.health_regen_button]):
            button.update_font(self.font)
            button.set_position((upgrade_x, upgrade_y + i * upgrade_spacing))

    def get_current_ball_cost(self):
        return int(self.base_ball_cost * (1 + len(self.balls) * 0.2))  # 20% increase per ball

    def spawn_ball(self, sX, sY):
        scale_factor = min(sX, sY)
        ball_radius = self.ball_base_radius * scale_factor
        # Spawn multiple balls based on upgrade level
        for _ in range(1 + self.data.multi_ball_level):
            self.balls.append(Ball(self.center_x, self.center_y, ball_radius, self.center_x, self.center_y))

    def enable_circle_spawn(self):
        self.can_spawn_circles = True

    def add_circle(self, sX, sY):
        if not self.can_spawn_circles:
            return
        active_circles = sum(1 for c in self.circles if c.active)
        max_circles = self.base_max_circles + (self.level - 1)
        if active_circles >= max_circles:
            return

        scaled_radius = int(self.circle_base_radius * min(sX, sY))
        new_circle = Circle(scaled_radius, self.line_thickness)
        if not new_circle.check_collision(self.circles):
            self.circles.append(new_circle)
            return True
        return False

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
                        # Check if this is the only active circle
                        self.can_spawn_circles = False
                        self.spawn_timer.activate()
                        circle.active = False
                        # Award experience based on circle size
                        # Award experience and currency based on circle size
                        exp_gain = int((circle.initial_radius - circle.radius) / 2)
                        currency_gain = int((circle.initial_radius - circle.radius) / 4)  # Half of exp gain
                        self.data.experience += max(10, exp_gain)
                        self.currency += max(5, currency_gain)  # Minimum 5 currency
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

            # Reflect normal component with bounce boost and minimal energy loss
            energy_loss = 0.995 - (0.02 * (len(colliding_circles) - 1))  # Less energy loss
            energy_loss = max(0.85, energy_loss)  # Higher minimum energy retention
            bounce_boost = 1.1  # Add extra energy on bounce
            norm_vel = -norm_vel * energy_loss * bounce_boost

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

            # Add minimal drag/friction
            drag = 0.995
            ball.vel_x *= drag
            ball.vel_y *= drag

    def update(self, dt, sX, sY):
        # Update level timer
        self.spawn_timer.update()

        # Apply health regeneration
        if self.health < 100:
            regen_amount = self.data.health_regen_level * 2 * dt  # 2 health per second per level
            self.health = min(100, self.health + regen_amount)

        # Update health and currency every second
        current_time = pygame.time.get_ticks()
        if current_time - self.last_stat_update >= self.stat_update_delay:
            # Update currency
            self.currency += 1

            # Check for minimum radius circles and update health with scaling damage
            has_min_radius = any(circle.active and circle.radius <= circle.min_radius for circle in self.circles)
            if has_min_radius:
                self.min_radius_time += self.stat_update_delay / 1000  # Convert to seconds
                damage = int(self.base_damage * (1 + self.min_radius_time / 5))  # Increase damage every 5 seconds
                self.health = max(0, self.health - damage)
            else:
                self.min_radius_time = 0  # Reset timer when no circles are at minimum radius

            self.last_stat_update = current_time

        # Draw status text
        status_x = int(20 * sX)
        status_y = int(20 * sY)
        spacing = int(40 * sY)

        health_text = self.font.render(f"Health: {self.health}", True, "white")
        currency_text = self.font.render(f"Currency: {self.currency}", True, "white")

        self.display_surface.blit(health_text, (status_x, status_y))
        self.display_surface.blit(currency_text, (status_x, status_y + spacing))

        # Draw level text within exp bar
        # Update and draw circles
        active_circles = [c for c in self.circles if c.active]
        if len(active_circles) == 0:
            if not self.circles:  # No circles at all
                if self.can_spawn_circles:
                    self.level += 1
                    max_circles = self.base_max_circles + (self.level - 1)
                    for _ in range(max_circles):
                        self.add_circle(sX, sY)
            else:  # Had circles but all were destroyed
                self.can_spawn_circles = False
                self.spawn_timer.activate()
                self.circles.clear()

        for circle in self.circles:
            circle.update(dt, self.circles, self.level)  # Pass level to circle update
            circle.draw(self.display_surface, self.center_x, self.center_y,
                        self.line_thickness, (182, 143, 64), pygame.gfxdraw)

        for ball in self.balls:
            ball.update(dt)

        self.handle_collisions()

        for ball in self.balls[:]:
            # Remove balls that hit the ground or outer ring
            if ball.y > self.display_surface.get_height():
                self.balls.remove(ball)
                # Refund half of the current ball cost
                refund = self.get_current_ball_cost() // 2
                self.currency += refund
            else:
                ball.draw(self.display_surface)

        self.add_circle(sX, sY)

        # Button UI
        self.spawn_button.update(self.display_surface)
        mouse_pos = pygame.mouse.get_pos()
        self.spawn_button.change_color(mouse_pos)
        if pygame.mouse.get_pressed()[0]:
            if self.spawn_button.check_input(mouse_pos) and not self.spawn_pressed:
                ball_cost = self.get_current_ball_cost()
                if self.currency >= ball_cost:
                    self.spawn_ball(sX, sY)
                    self.currency -= ball_cost
                    self.spawn_pressed = True
        else:
            self.spawn_pressed = False
            self.circle_pressed = False

        # Handle upgrade buttons
        upgrade_buttons = [
            (self.multi_ball_button, '_multi_ball_level'),
            (self.shrink_reduction_button, '_shrink_reduction_level'),
            (self.rotation_reduction_button, '_rotation_reduction_level'),
            (self.health_regen_button, '_health_regen_level')
        ]

        for button, attr in upgrade_buttons:
            # Get current level and cost
            current_level = getattr(self.data, attr)
            cost = self.data.get_upgrade_cost(current_level)

            # Update button text with cost
            button.text_input = f"{button.text_input.split(':')[0]}: {cost}"
            button.text = button.font.render(button.text_input, True, button.base_color)
            button.update(self.display_surface)
            button.change_color(mouse_pos)

            # Handle click
            if pygame.mouse.get_pressed()[0] and button.check_input(mouse_pos):
                if self.currency >= cost:
                    setattr(self.data, attr, current_level + 1)
                    self.currency -= cost