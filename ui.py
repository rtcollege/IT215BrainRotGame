from settings import *
from data import Data
from debug import debug
from dropdown import Dropdown
from timer import Timer
from button import Button
from ballsimulation import BallSimulation
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
        self.ball_sim = BallSimulation(self.display_surface, self.sX, self.sY, self.data)

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

        #Improved height calculation for better adaptability.
        adjusted_height = self.font.size(resolution_options[0])[1] + 10  # Add padding

        self.resolution_dropdown = Dropdown(
            button_x + self.resolution_text.get_width() + int(40 * self.sX),
            res_y,
            dropdown_width,
            dropdown_height,
            resolution_options,
            self.font,
            current_res,
            adjusted_height #Pass adjusted height to Dropdown
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
        if self.data.health <= 0:
            # Draw the current state without updating
            # Draw status text
            status_x = int(20 * self.sX)
            status_y = int(20 * self.sY)
            spacing = int(40 * self.sY)

            health_text = self.ball_sim.font.render(f"Health: {self.data.health}", True, "white")
            currency_text = self.ball_sim.font.render(f"Currency: {self.data.currency}", True, "white")

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

        if self.current_scene == 'settings':
            self.resolution_dropdown.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event)


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
        elif self.resolution_dropdown.handle_event(mouse_pos):
            pass
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
        if self.data.health <= 0:
            if self.restart_button.check_input(mouse_pos):
                # Create fresh Data instance
                self.data = Data(self)
                # Reset ball simulation
                self.ball_sim = BallSimulation(self.display_surface, self.sX, self.sY, self.data)
                # Clear existing game state
                self.ball_sim.balls.clear()
                self.ball_sim.circles.clear()
                self.ball_sim.can_spawn_circles = True
                # Reset pause state
                self.is_paused = False
                # Force redraw
                self.draw_background()
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