from settings import *
from data import Data
from debug import debug
from dropdown import Dropdown
from timer import Timer
from button import Button
from math import sin, cos, radians, degrees, atan2
import random
import pygame.gfxdraw


class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.base_font_size = 40
        self.frames = frames # Initialize frames here

        # Initialize ball simulation
        self.current_scene = 'main_menu'
        self.previous_scene = 'main_menu'
        self.is_paused = False
        self.difficulty = 'medium'
        self.volume = 75
        self.W_WIDTH = WINDOW_WIDTH
        self.W_HEIGHT = WINDOW_HEIGHT
        self.sX = SCALE_X
        self.sY = SCALE_Y
        self.ball_sim = BallSimulation(self.display_surface, self.sX, self.sY)
        self.ball_sim.recalculate_layout(self.sX, self.sY)  # Initial layout calculation



        # Create default font objects (will be scaled later)
        self.font = font
        self.title_font = font

        # Create buttons and elements
        self.play_button = Button(None, (0, 0), "Play", self.font, "white", "#b68f40")
        self.settings_button = Button(None, (0, 0), "Settings", self.font, "white", "#b68f40")
        self.credits_button = Button(None, (0, 0), "Credits", self.font, "white", "#b68f40")
        self.quit_button = Button(None, (0, 0), "Quit", self.font, "white", "#b68f40")
        self.easy_button = Button(None, (0, 0), "Easy", self.font, "white", "#b68f40")
        self.medium_button = Button(None, (0, 0), "Medium", self.font, "white", "#b68f40")
        self.hard_button = Button(None, (0, 0), "Hard", self.font, "white", "#b68f40")
        self.back_button = Button(None, (0, 0), "Back", self.font, "white", "#b68f40")

        self.resolution_buttons = []
        for (width, height) in RESOLUTIONS:
            btn = Button(None, (0, 0), f"{width}x{height}", self.font, "white", "#b68f40")
            self.resolution_buttons.append((btn, (width, height)))

        # Recalculate layout now that elements exist
        self.recalculate_layout()



    def recalculate_layout(self):
        # Update fonts with new scale
        self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", int(self.base_font_size * min(self.sX, self.sY)))
        self.title_font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", int(self.base_font_size * min(self.sX, self.sY)))

        # Layout positions
        button_x = int(50 * self.sX)
        button_y_start = int(300 * self.sY)
        button_y_spacing = int(100 * self.sY)

        # Main menu title
        self.title_text = self.title_font.render("Brain Rot Game", True, "white")
        self.title_rect = self.title_text.get_rect(topleft=(button_x, int(100 * self.sY)))

        # Main menu buttons
        self.play_button.update_font(self.font)
        self.play_button.set_position((button_x, button_y_start))

        self.settings_button.update_font(self.font)
        self.settings_button.set_position((button_x, button_y_start + button_y_spacing))

        self.credits_button.update_font(self.font)
        self.credits_button.set_position((button_x, button_y_start + 2 * button_y_spacing))

        self.quit_button.update_font(self.font)
        self.quit_button.set_position((button_x, button_y_start + 3 * button_y_spacing))

        # Settings title
        self.settings_title = self.title_font.render("Settings", True, "white")
        self.settings_title_rect = self.settings_title.get_rect(topleft=(button_x, int(100 * self.sY)))

        # Volume slider
        volume_y = int(250 * self.sY)
        self.volume_text = self.font.render("Volume:", True, "white")
        text_height = self.volume_text.get_height()
        self.volume_text_rect = self.volume_text.get_rect(topleft=(button_x, volume_y - text_height // 2))

        self.slider_width = int(200 * self.sX)
        slider_height = int(20 * self.sY)
        slider_handle_width = int(20 * self.sX)
        slider_handle_height = int(30 * self.sY)

        self.volume_rect = pygame.Rect(
            self.W_WIDTH // 2 - self.slider_width // 2,
            volume_y,
            self.slider_width,
            slider_height
        )
        # Calculate slider position based on volume percentage
        slider_x = self.W_WIDTH // 2 - self.slider_width // 2 + int((self.volume / 100) * self.slider_width)
        self.volume_slider = pygame.Rect(
            slider_x,
            volume_y + (slider_height // 2) - (slider_handle_height // 2),
            slider_handle_width,
            slider_handle_height
        )

        # Difficulty section
        diff_y = int(400 * self.sY)
        button_spacing = int(200 * self.sX)
        self.difficulty_text = self.font.render("Difficulty:", True, "white")
        text_height = self.difficulty_text.get_height()
        self.difficulty_text_rect = self.difficulty_text.get_rect(topleft=(button_x, diff_y - text_height // 2))

        # Position buttons evenly with equal spacing between centers
        self.easy_button.update_font(self.font)
        self.medium_button.update_font(self.font)
        self.hard_button.update_font(self.font)

        total_width = button_spacing * 2  # Total width between first and last button
        center_x = self.W_WIDTH/2

        self.easy_button.set_position(((center_x - (self.easy_button.text.get_width()) // 2) - button_spacing, diff_y))
        self.medium_button.set_position((center_x - (self.medium_button.text.get_width() // 2), diff_y))
        self.hard_button.set_position((center_x - (self.hard_button.text.get_width() // 2) + button_spacing, diff_y))

        # Resolution section
        res_y = diff_y + int(100 * self.sY)
        self.resolution_text = self.font.render("Resolution:", True, "white")
        text_height = self.resolution_text.get_height()
        self.resolution_text_rect = self.resolution_text.get_rect(topleft=(button_x, res_y - text_height // 2))

        # Create resolution options list
        resolution_options = [f"{width}x{height}" for width, height in RESOLUTIONS]
        current_res = f"{self.W_WIDTH}x{self.W_HEIGHT}"

        # Create dropdown menu
        dropdown_width = int(220 * self.sX)
        dropdown_height = int(40 * self.sY)  # Match button height
        spacing_after_text = int(40 * self.sX)  # Increase spacing after text
        self.resolution_dropdown = Dropdown(
            button_x + self.resolution_text.get_width() + spacing_after_text,
            res_y,
            dropdown_width,
            dropdown_height,
            resolution_options,
            self.font,
            current_res
        )


        # Create apply button
        self.apply_button = Button(
            None,
            (self.resolution_dropdown.rect.right + int(20 * self.sX), res_y),
            "Apply",
            self.font,
            "white",
            "#b68f40"
        )

        # Back button (same position as quit)
        self.back_button.update_font(self.font)
        self.back_button.set_position((button_x, button_y_start + 3 * button_y_spacing))

        # Credits scene setup
        self.credits_title = self.title_font.render("Credits", True, "white")
        self.credits_title_rect = self.credits_title.get_rect(topleft=(button_x, int(100 * self.sY)))

        # Pause menu setup
        self.pause_title = self.title_font.render("Paused", True, "white")
        self.pause_title_rect = self.pause_title.get_rect(topleft=(button_x, int(100 * self.sY)))
        self.resume_button = Button(None, (button_x, button_y_start), "Resume", self.font, "white", "#b68f40")
        self.pause_settings_button = Button(None, (button_x, button_y_start + button_y_spacing), "Settings", self.font, "white", "#b68f40")
        self.pause_credits_button = Button(None, (button_x, button_y_start + 2 * button_y_spacing), "Credits", self.font, "white", "#b68f40")
        self.pause_main_menu_button = Button(None, (button_x, button_y_start + 3 * button_y_spacing), "Main Menu", self.font, "white", "#b68f40")

        # Credits text
        credits_lines = ["Lead Developer: John Doe",
                        "Art Director: Jane Smith",
                        "Sound Designer: Mike Johnson",
                        "Level Designer: Sarah Wilson"]
        self.credits_texts = []
        self.credits_rects = []

        for i, line in enumerate(credits_lines):
            text = self.font.render(line, True, "white")
            rect = text.get_rect(center=(self.W_WIDTH//2, self.W_HEIGHT//2 - 100 + i * 50 * self.sY))
            self.credits_texts.append(text)
            self.credits_rects.append(rect)

        # Recalculate ball simulation layout
        self.ball_sim.recalculate_layout(self.sX, self.sY)



    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()

        # Create gradient background
        background = pygame.Surface((self.W_WIDTH, self.W_HEIGHT))
        color1 = pygame.Color("#2c2c2c")
        color2 = pygame.Color("#1a1a1a")
        for y in range(self.W_HEIGHT):
            color = pygame.Color(
                int(color1.r + (color2.r - color1.r) * y/self.W_HEIGHT),
                int(color1.g + (color2.g - color1.g) * y/self.W_HEIGHT),
                int(color1.b + (color2.b - color1.b) * y/self.W_HEIGHT)
            )
            pygame.draw.line(background, color, (0, y), (self.W_WIDTH, y))
        self.display_surface.blit(background, (0, 0))


        if self.current_scene == 'main_menu':
            # Draw title
            self.display_surface.blit(self.title_text, self.title_rect)

            # Update and draw buttons
            self.play_button.update(self.display_surface)
            self.settings_button.update(self.display_surface)
            self.credits_button.update(self.display_surface)
            self.quit_button.update(self.display_surface)

            # Update button colors based on hover
            self.play_button.change_color(mouse_pos)
            self.settings_button.change_color(mouse_pos)
            self.credits_button.change_color(mouse_pos)
            self.quit_button.change_color(mouse_pos)

        elif self.current_scene == 'settings':
            # Draw settings title
            self.display_surface.blit(self.settings_title, self.settings_title_rect)

            # Draw volume label, slider and value
            self.display_surface.blit(self.volume_text, self.volume_text_rect)
            self.display_surface.blit(self.difficulty_text, self.difficulty_text_rect)
            pygame.draw.rect(self.display_surface, "white", self.volume_rect, 2)
            pygame.draw.rect(self.display_surface, "white", self.volume_slider)

            # Display volume value
            volume_value = self.font.render(f"{int(self.volume)}%", True, "white")
            volume_value_rect = volume_value.get_rect(midleft=(self.volume_rect.right + 20, self.volume_rect.centery))
            self.display_surface.blit(volume_value, volume_value_rect)

            # Handle slider dragging
            if pygame.mouse.get_pressed()[0]:
                if self.volume_rect.collidepoint(mouse_pos):
                    self.volume = (mouse_pos[0] - (self.W_WIDTH/2 - self.slider_width/2)) / (self.slider_width/100)
                    self.volume = max(0, min(100, self.volume))
                    self.volume_slider.x = int(self.W_WIDTH/2 - self.slider_width/2 + (self.volume * self.slider_width/100))

            # Draw difficulty buttons
            self.easy_button.update(self.display_surface)
            self.medium_button.update(self.display_surface)
            self.hard_button.update(self.display_surface)

            # Draw button borders based on selection
            if self.difficulty == 'easy':
                pygame.draw.rect(self.display_surface, "white", self.easy_button.rect, 3)
            elif self.difficulty == 'medium':
                pygame.draw.rect(self.display_surface, "white", self.medium_button.rect, 3)
            elif self.difficulty == 'hard':
                pygame.draw.rect(self.display_surface, "white", self.hard_button.rect, 3)

            # Draw resolution text and dropdown
            self.display_surface.blit(self.resolution_text, self.resolution_text_rect)
            self.resolution_dropdown.draw(self.display_surface)
            self.apply_button.update(self.display_surface)
            self.apply_button.change_color(mouse_pos)

            # Update back button
            self.back_button.update(self.display_surface)
            self.back_button.change_color(mouse_pos)

        elif self.current_scene == 'credits':
            # Draw credits title
            self.display_surface.blit(self.credits_title, self.credits_title_rect)

            # Draw credits text
            for text, rect in zip(self.credits_texts, self.credits_rects):
                self.display_surface.blit(text, rect)

            # Update back button
            self.back_button.update(self.display_surface)
            self.back_button.change_color(mouse_pos)

        elif self.current_scene == 'gameplay':
            if not self.is_paused:
                self.ball_sim.update(dt, self.sX, self.sY)

            if self.is_paused:
                # Draw semi-transparent overlay
                overlay = pygame.Surface((self.W_WIDTH, self.W_HEIGHT))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(96)  # Reduced opacity from 128 to 96
                self.display_surface.blit(overlay, (0, 0))

                # Draw pause menu
                self.display_surface.blit(self.pause_title, self.pause_title_rect)
                self.resume_button.update(self.display_surface)
                self.pause_settings_button.update(self.display_surface)
                self.pause_credits_button.update(self.display_surface)
                self.pause_main_menu_button.update(self.display_surface)

                # Update button colors
                self.resume_button.change_color(mouse_pos)
                self.pause_settings_button.change_color(mouse_pos)
                self.pause_credits_button.change_color(mouse_pos)
                self.pause_main_menu_button.change_color(mouse_pos)

            # Handle volume slider dragging
            if pygame.mouse.get_pressed()[0]:
                if self.volume_rect.collidepoint(mouse_pos):
                    self.volume = (mouse_pos[0] - (self.W_WIDTH/2 - self.slider_width/2)) // (self.slider_width/100)
                    self.volume = max(0, min(100, self.volume))
                    self.volume_slider.x = int(self.W_WIDTH/2 - self.slider_width/2 + (self.volume * self.slider_width/100))

    def handle_events(self, event):
        """Handle UI-specific events"""
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.current_scene == 'gameplay':
                self.is_paused = not self.is_paused
            elif self.current_scene in ['settings', 'credits']:
                temp_scene = self.current_scene
                self.current_scene = self.previous_scene
                self.previous_scene = temp_scene

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_scene == 'main_menu':
                if self.play_button.check_input(mouse_pos):
                    self.previous_scene = self.current_scene
                    self.current_scene = 'gameplay'
                    self.is_paused = False
                elif self.settings_button.check_input(mouse_pos):
                    self.previous_scene = self.current_scene
                    self.current_scene = 'settings'
                elif self.credits_button.check_input(mouse_pos):
                    self.previous_scene = self.current_scene
                    self.current_scene = 'credits'
                elif self.quit_button.check_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
            elif self.current_scene == 'settings' or self.current_scene == 'credits':
                if self.back_button.check_input(mouse_pos):
                    temp_scene = self.current_scene
                    self.current_scene = self.previous_scene
                    self.previous_scene = temp_scene
                elif self.current_scene == 'settings':
                    if self.easy_button.check_input(mouse_pos):
                        self.difficulty = 'easy'
                    elif self.medium_button.check_input(mouse_pos):
                        self.difficulty = 'medium'
                    elif self.hard_button.check_input(mouse_pos):
                        self.difficulty = 'hard'
                    elif pygame.mouse.get_pressed()[0]:
                        if self.volume_rect.collidepoint(mouse_pos):
                            self.volume = (mouse_pos[0] - (self.W_WIDTH/2 - self.slider_width/2)) / (self.slider_width/100)
                            self.volume = max(0, min(100, self.volume))
                            self.volume_slider.x = int(self.W_WIDTH/2 - self.slider_width/2 + (self.volume * self.slider_width/100))
                    # Handle resolution dropdown
                    self.resolution_dropdown.handle_event(event)
                    if self.apply_button.check_input(mouse_pos):
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
            elif self.current_scene == 'gameplay' and self.is_paused:
                if self.resume_button.check_input(mouse_pos):
                    self.is_paused = False
                elif self.pause_settings_button.check_input(mouse_pos):
                    self.previous_scene = 'gameplay'
                    self.current_scene = 'settings'
                elif self.pause_credits_button.check_input(mouse_pos):
                    self.previous_scene = 'gameplay'
                    self.current_scene = 'credits'
                elif self.pause_main_menu_button.check_input(mouse_pos):
                    self.current_scene = 'main_menu'

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
        self.cell_x = 0
        self.cell_y = 0
        self.passed_circles = set()  # Track which circles the ball has passed through

    def update(self, dt):
        self.vel_y += self.gravity * dt
        self.x += self.vel_x * dt * 60
        self.y += self.vel_y * dt * 60

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

class Circle:
    def __init__(self, radius, active=True):
        self.radius = radius
        self.active = active
        self.angle = random.randint(0, 360)  # Random starting angle
        self.rotation_speed = random.uniform(0.5, 2.0)  # Random rotation speed
        self.gap_size = min(120, 30 + (radius / 2))  # Gap size proportional to radius

    def update(self, dt):
        self.angle = (self.angle + self.rotation_speed) % 360

    def is_in_gap(self, ball_angle):
        gap_start = self.angle
        gap_end = (self.angle + self.gap_size) % 360
        return (gap_start < gap_end and gap_start <= ball_angle <= gap_end) or \
               (gap_start > gap_end and (ball_angle >= gap_start or ball_angle <= gap_end))

    def draw(self, surface, center_x, center_y, line_thickness, color, gfxdraw):
        if self.active:
            for i in range(line_thickness):
                gfxdraw.arc(surface, 
                           int(center_x), 
                           int(center_y), 
                           int(self.radius - i), 
                           int(self.angle), 
                           int((self.angle + (360 - self.gap_size)) % 360), 
                           color)


class BallSimulation:
    def __init__(self, display_surface, sX, sY):
        self.display_surface = display_surface
        self.base_radius = 150
        self.base_padding = 100  # Padding around the circle
        self.base_box_width = self.base_radius * 2 + self.base_padding
        self.base_box_height = self.base_radius * 2 + self.base_padding
        self.base_box_x = 100
        self.angle = 0
        self.rotation_speed = 1
        self.color = (182, 143, 64)
        self.balls = []
        self.circles = []  # Initialize empty
        self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", int(20 * min(sX, sY)))

        self.spawn_button = Button(None, 
             (0,0), 
             "Spawn Ball", 
             self.font, 
             "white", 
             "#b68f40")
        self.add_circle_button = Button(None, 
                  (0,0), 
                  "Add Circle", 
                  self.font, 
                  "white", 
                  "#b68f40")

        # Add base circle
        self.add_circle(1, 1)  # Initial scaling factors don't matter for first circle
        self.spawn_pressed = False
        self.circle_pressed = False
        self.recalculate_layout(sX, sY)



    def recalculate_layout(self, sX, sY):
        self.radius = int(self.base_radius * min(sX, sY))
        self.box_width = int(self.base_box_width * sX)
        self.box_height = int(self.base_box_height * sY)
        self.box_x = int(self.base_box_x * sX)
        self.box_y = (self.display_surface.get_height() - self.box_height) // 2
        self.center_x = self.box_x + self.box_width // 2
        self.center_y = self.box_y + self.box_height // 2
        self.line_thickness = max(1, int(3 * min(sX, sY)))
        
        button_spacing = int(30 * min(sX, sY))  # Reduced spacing between buttons
        button_y = self.box_y + self.box_height + (button_spacing * 1.5) + self.spawn_button.rect.height  # Position below box with proper height offset
        
        # Update existing buttons with new positions
        self.spawn_button.set_position((self.box_x + button_spacing, button_y))
        self.add_circle_button.set_position((self.box_x + button_spacing + self.spawn_button.rect.width + button_spacing, button_y))
        
        # Update button fonts in case of resolution change
        self.spawn_button.update_font(self.font)
        self.add_circle_button.update_font(self.font) 

    def spawn_ball(self, sX, sY):
        ball_radius = int(10 * min(self.display_surface.get_width()/1920, self.display_surface.get_height()/1080))
        new_ball = Ball(self.center_x, self.center_y, ball_radius)
        self.balls.append(new_ball)

    def add_circle(self, sX, sY):
        active_circles = sum(1 for circle in self.circles if circle.active)
        if active_circles >= 10:
            return
        if len(self.circles) == 0 or active_circles == 0:
            # Base case - first circle or all circles broken
            self.circles.append(Circle(self.base_radius))
        else:
            # Get the last active circle's radius
            last_active_radius = next((circle.radius for circle in reversed(self.circles) if circle.active), self.base_radius)
            new_radius = max(10, last_active_radius - 20)
            self.circles.append(Circle(new_radius))

    def update(self, dt, sX, sY):
        padding = int(50 * min(sX, sY))  # Add padding proportional to circle size
        pygame.draw.rect(self.display_surface, '#cccccc', 
                        (self.box_x - padding, self.box_y - padding, 
                         self.box_width + 2*padding, self.box_height + 2*padding), 
                        max(1, int(2 * min(sX, sY))))

        for circle in self.circles:
            circle.update(dt)
            circle.draw(self.display_surface, self.center_x, self.center_y, 
                       self.line_thickness, self.color, pygame.gfxdraw)

        for ball in self.balls[:]:
            ball.update(dt)
            
            # Calculate distance and angle from center for each ball
            dx = ball.x - self.center_x
            dy = ball.y - self.center_y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            angle = (degrees(atan2(dy, dx)) + 360) % 360
            
            # Check collision with each circle
            for i, circle in enumerate(self.circles):
                if circle.active:
                    # Only check collision if we haven't passed this circle yet
                    if i not in ball.passed_circles:
                        if abs(distance - circle.radius) < ball.radius:
                            if not circle.is_in_gap(angle):
                                # Ball hit the circle - remove it
                                if ball in self.balls:
                                    self.balls.remove(ball)
                                break
                            else:
                                # Ball passed through gap
                                ball.passed_circles.add(i)
                                
            # Remove balls that go too far from the center
            max_distance = self.radius * 2
            if distance > max_distance:
                if ball in self.balls:
                    self.balls.remove(ball)

            ball.draw(self.display_surface)

