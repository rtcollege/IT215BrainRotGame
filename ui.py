from settings import *
from data import Data
from debug import debug
from dropdown import Dropdown
from timer import Timer
from button import Button
from ballsimulation import BallSimulation


class UI:

    def __init__(self, font, frames, data):
        # Core initialization
        self.display_surface = pygame.display.get_surface()
        self.base_font_size = 40
        self.frames = frames
        self.font = font
        self.data = data

        # State variables
        self.current_scene = 'main_menu'
        self.previous_scene = 'main_menu'
        self.is_paused = False
        self.difficulty = 'medium'
        self.volume = 75

        # Window properties
        self.W_WIDTH = WINDOW_WIDTH
        self.W_HEIGHT = WINDOW_HEIGHT
        self.sX = SCALE_X
        self.sY = SCALE_Y

        # Initialize components
        self.ball_sim = BallSimulation(self.display_surface, self.sX, self.sY,
                                       self.data)
        self.init_buttons()
        self.init_resolution_buttons()
        self.recalculate_layout()

    def init_buttons(self):
        """Initialize all UI buttons"""
        buttons = [('play_button', "Play"), ('settings_button', "Settings"),
                   ('credits_button', "Credits"), ('quit_button', "Quit"),
                   ('easy_button', "Easy"), ('medium_button', "Medium"),
                   ('hard_button', "Hard"), ('back_button', "Back"),
                   ('resume_button', "Resume"),
                   ('pause_settings_button', "Settings"),
                   ('pause_credits_button', "Credits"),
                   ('pause_main_menu_button', "Main Menu"),
                   ('restart_button', "Restart")]
        for attr_name, text in buttons:
            setattr(self, attr_name,
                    Button(None, (0, 0), text, self.font, "white", "#b68f40"))

    def init_resolution_buttons(self):
        """Initialize resolution selection buttons"""
        self.resolution_buttons = []
        for width, height in RESOLUTIONS:
            btn = Button(None, (0, 0), f"{width}x{height}", self.font, "white",
                         "#b68f40")
            self.resolution_buttons.append((btn, (width, height)))

    def recalculate_layout(self):
        """Recalculate UI element positions and sizes"""
        # Layout constants
        button_x = int(50 * self.sX)
        button_y_start = int(300 * self.sY)
        button_y_spacing = int(100 * self.sY)

        # Update fonts
        self.font = pygame.font.Font(
            "graphics/ui/NeotriadFree-1jzAg.ttf",
            int(self.base_font_size * min(self.sX, self.sY)))
        self.title_font = pygame.font.Font(
            "graphics/ui/NeotriadFree-1jzAg.ttf",
            int(self.base_font_size * 1.5 * min(self.sX, self.sY)))

        # Initialize titles
        self.setup_titles(button_x)

        back_button_x = int(50 * self.sX)  # Same as button_x
        back_button_y = button_y_start + 3 * button_y_spacing
        self.back_button = Button(None, (back_button_x, back_button_y), "Back",
                                  self.font, "white", "#b68f40")

        # Update main menu buttons
        menu_buttons = [
            self.play_button, self.settings_button, self.credits_button,
            self.quit_button
        ]
        for i, button in enumerate(menu_buttons):
            button.update_font(self.font)
            button.set_position(
                (button_x, button_y_start + i * button_y_spacing))

        # Update settings layout
        self.setup_volume_slider(button_x)
        self.setup_difficulty_buttons(button_x)
        self.setup_resolution_dropdown(button_x)
        self.setup_credits_text(button_x)
        self.setup_pause_menu(button_x, button_y_start, button_y_spacing)

        # Update ball simulation layout
        self.ball_sim.recalculate_layout(self.sX, self.sY)

    def setup_titles(self, button_x):
        """Set up all scene titles"""
        titles = {
            'main': "Brain Rot Game",
            'settings': "Settings",
            'credits': "Credits",
            'pause': "Paused"
        }
        y_pos = int(100 * self.sY)

        for name, text in titles.items():
            title_text = self.title_font.render(text, True, "white")
            setattr(self, f"{name}_title", title_text)
            setattr(self, f"{name}_title_rect",
                    title_text.get_rect(topleft=(button_x, y_pos)))

    def setup_volume_slider(self, button_x):
        """Set up volume control elements"""
        volume_y = int(250 * self.sY)
        self.volume_text = self.font.render("Volume:", True, "white")
        text_height = self.volume_text.get_height()
        self.volume_text_rect = self.volume_text.get_rect(
            topleft=(button_x, volume_y - text_height // 2))

        self.slider_width = int(200 * self.sX)
        self.volume_rect = pygame.Rect(
            self.W_WIDTH // 2 - self.slider_width // 2, volume_y,
            self.slider_width, int(20 * self.sY))

        slider_x = self.W_WIDTH // 2 - self.slider_width // 2 + int(
            (self.volume / 100) * self.slider_width)
        self.volume_slider = pygame.Rect(slider_x, volume_y - int(5 * self.sY),
                                         int(20 * self.sX), int(30 * self.sY))

    def setup_difficulty_buttons(self, button_x):
        """Set up difficulty selection buttons"""
        diff_y = int(400 * self.sY)
        button_spacing = int(200 * self.sX)
        center_x = self.W_WIDTH / 2

        self.difficulty_text = self.font.render("Difficulty:", True, "white")
        text_height = self.difficulty_text.get_height()
        self.difficulty_text_rect = self.difficulty_text.get_rect(
            topleft=(button_x, diff_y - text_height // 2))

        diff_buttons = [(self.easy_button, -1), (self.medium_button, 0),
                        (self.hard_button, 1)]

        for button, x_offset in diff_buttons:
            button.update_font(self.font)
            button.set_position((center_x + x_offset * button_spacing -
                                 button.text.get_width() // 2, diff_y))

    def setup_resolution_dropdown(self, button_x):
        """Set up resolution selection dropdown"""
        res_y = int(500 * self.sY)
        dropdown_width = int(220 * self.sX)
        dropdown_height = int(60 * self.sY)
        # Scale padding based on window size

        resolution_options = [
            f"{width}x{height}" for width, height in RESOLUTIONS
        ]
        current_res = f"{self.W_WIDTH}x{self.W_HEIGHT}"

        self.resolution_text = self.font.render("Resolution:", True, "white")
        text_height = self.resolution_text.get_height()
        self.resolution_text_rect = self.resolution_text.get_rect(
            topleft=(button_x, res_y - text_height // 2))

        # Initialize dropdown with the current resolution
        self.resolution_dropdown = Dropdown(
            button_x + self.resolution_text.get_width() + int(40 * self.sX),
            res_y - dropdown_height // 2,  # Center vertically
            dropdown_width,
            dropdown_height,
            resolution_options,
            self.font,
            current_res)

        # Setup apply button
        self.apply_button = Button(
            None,
            (self.resolution_dropdown.rect.right + int(20 * self.sX), 
             res_y),
            "Apply",
            self.font,
            "white",
            "#b68f40")

        # Setup resolution buttons below dropdown
        button_spacing = int(200 * self.sX)
        res_button_y = res_y + dropdown_height + int(20 * self.sY)
        center_x = self.W_WIDTH / 2

        self.resolution_buttons = []
        for i, (width, height) in enumerate(RESOLUTIONS):
            btn = Button(
                None,
                (center_x + (i - len(RESOLUTIONS)/2 + 0.5) * button_spacing,
                 res_button_y),
                f"{width}x{height}",
                self.font,
                "white",
                "#b68f40")
            self.resolution_buttons.append((btn, (width, height)))

    def setup_credits_text(self, button_x):
        """Set up credits text"""
        credits_lines = [
            "Lead Developer: Ryan Tiedeman",
            "Art Director: Ryan Tiedeman",
            "Sound Designer: Ryan Tiedeman (There is no sound)",
            "Level Designer: Ryan Tiedeman"
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
        """Set up pause menu buttons"""
        pause_buttons = [(self.resume_button, 0),
                         (self.pause_settings_button, 1),
                         (self.pause_credits_button, 2),
                         (self.pause_main_menu_button, 3)]

        for button, i in pause_buttons:
            button.update_font(self.font)
            button.set_position(
                (button_x, button_y_start + i * button_y_spacing))

    def draw_background(self):
        """Draw gradient background"""
        background = pygame.Surface((self.W_WIDTH, self.W_HEIGHT))
        for y in range(self.W_HEIGHT):
            factor = y / self.W_HEIGHT
            color = pygame.Color(int(44 * (1 - factor) + 26 * factor),
                                 int(44 * (1 - factor) + 26 * factor),
                                 int(44 * (1 - factor) + 26 * factor))
            pygame.draw.line(background, color, (0, y), (self.W_WIDTH, y))
        self.display_surface.blit(background, (0, 0))

    def update(self, dt):
        """Update UI state and render elements"""
        mouse_pos = pygame.mouse.get_pos()
        self.draw_background()

        scenes = {
            'main_menu': self.update_main_menu,
            'settings': self.update_settings,
            'credits': self.update_credits,
            'gameplay': self.update_gameplay
        }

        if self.current_scene in scenes:
            scenes[self.current_scene](mouse_pos, dt)

    def update_main_menu(self, mouse_pos, dt):
        """Update main menu scene"""
        self.display_surface.blit(self.main_title, self.main_title_rect)
        for button in [
                self.play_button, self.settings_button, self.credits_button,
                self.quit_button
        ]:
            button.update(self.display_surface)
            button.change_color(mouse_pos)

    def update_settings(self, mouse_pos, dt):
        """Update settings scene"""
        self.display_surface.blit(self.settings_title,
                                  self.settings_title_rect)
        self.display_surface.blit(self.volume_text, self.volume_text_rect)
        self.display_surface.blit(self.difficulty_text,
                                  self.difficulty_text_rect)

        # Draw volume controls
        pygame.draw.rect(self.display_surface, "white", self.volume_rect, 2)
        pygame.draw.rect(self.display_surface, "white", self.volume_slider)

        # Update dropdown hover states
        self.resolution_dropdown.update(mouse_pos)

        # Handle volume slider
        if pygame.mouse.get_pressed()[0]:
            if self.volume_rect.collidepoint(
                    mouse_pos) or self.volume_slider.collidepoint(mouse_pos):
                self.update_volume_from_mouse(mouse_pos[0])

        # Display volume value
        volume_value = self.font.render(f"{int(self.volume)}%", True, "white")
        volume_value_rect = volume_value.get_rect(
            midleft=(self.volume_rect.right + 20, self.volume_rect.centery))
        self.display_surface.blit(volume_value, volume_value_rect)

        # Draw resolution controls with debug outline
        self.display_surface.blit(self.resolution_text,
                                  self.resolution_text_rect)
        self.resolution_dropdown.draw(self.display_surface)
        
        self.apply_button.update(self.display_surface)
        self.apply_button.change_color(mouse_pos)

        # Draw difficulty buttons
        for button in [self.easy_button, self.medium_button, self.hard_button]:
            button.update(self.display_surface)

        # Highlight selected difficulty
        selected_button = getattr(self, f"{self.difficulty}_button")
        pygame.draw.rect(self.display_surface, "white", selected_button.rect,
                         3)

        self.back_button.update(self.display_surface)
        self.back_button.change_color(mouse_pos)

    def update_credits(self, mouse_pos, dt):
        """Update credits scene"""
        self.display_surface.blit(self.credits_title, self.credits_title_rect)
        for text, rect in zip(self.credits_texts, self.credits_rects):
            self.display_surface.blit(text, rect)
        self.back_button.update(self.display_surface)
        self.back_button.change_color(mouse_pos)

    def update_gameplay(self, mouse_pos, dt):
        """Update gameplay scene"""
        if self.data.health <= 0:
            self.handle_game_over(mouse_pos)
        elif not self.is_paused:
            self.handle_active_gameplay(dt)
        else:
            self.handle_paused_gameplay(mouse_pos)

    def handle_game_over(self, mouse_pos):
        """Handle game over state"""
        self.draw_status_info()
        self.draw_experience_bar()

        # Show game over overlay
        overlay = pygame.Surface((self.W_WIDTH, self.W_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.display_surface.blit(overlay, (0, 0))

        game_over_text = self.title_font.render("Game Over", True, "white")
        game_over_rect = game_over_text.get_rect(center=(self.W_WIDTH // 2,
                                                         self.W_HEIGHT // 2 -
                                                         50))
        self.display_surface.blit(game_over_text, game_over_rect)

        self.restart_button.set_position(
            (self.W_WIDTH // 2 - self.restart_button.rect.width // 2,
             self.W_HEIGHT // 2 + 50))
        self.restart_button.update(self.display_surface)
        self.restart_button.change_color(mouse_pos)

    def handle_active_gameplay(self, dt):
        """Handle active gameplay state"""
        self.draw_experience_bar()
        self.ball_sim.update(dt, self.sX, self.sY)

    def handle_paused_gameplay(self, mouse_pos):
        """Handle paused gameplay state"""
        overlay = pygame.Surface((self.W_WIDTH, self.W_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(96)
        self.display_surface.blit(overlay, (0, 0))
        self.display_surface.blit(self.pause_title, self.pause_title_rect)

        for button in [
                self.resume_button, self.pause_settings_button,
                self.pause_credits_button, self.pause_main_menu_button
        ]:
            button.update(self.display_surface)
            button.change_color(mouse_pos)

    def draw_status_info(self):
        """Draw health and currency status"""
        status_x = int(20 * self.sX)
        status_y = int(20 * self.sY)
        spacing = int(40 * self.sY)

        health_text = self.ball_sim.font.render(f"Health: {self.data.health}",
                                                True, "white")
        currency_text = self.ball_sim.font.render(
            f"Currency: {self.data.currency}", True, "white")

        self.display_surface.blit(health_text, (status_x, status_y))
        self.display_surface.blit(currency_text,
                                  (status_x, status_y + spacing))

    def draw_experience_bar(self):
        """Draw experience bar"""
        exp_bar_width = int(300 * self.sX)
        exp_bar_height = int(20 * self.sY)
        exp_bar_x = self.ball_sim.center_x - exp_bar_width // 2
        exp_bar_y = self.ball_sim.box_y - 50

        # Background
        exp_bar_bg = pygame.Rect(exp_bar_x, exp_bar_y, exp_bar_width,
                                 exp_bar_height)
        pygame.draw.rect(self.display_surface, "black", exp_bar_bg)
        pygame.draw.rect(self.display_surface, "white", exp_bar_bg, 2)

        # Progress
        exp_needed = self.data.get_exp_for_level(self.data.level)
        progress = self.data.experience / exp_needed
        if progress > 0:
            fill_width = int(exp_bar_width * progress)
            fill_rect = pygame.Rect(exp_bar_x, exp_bar_y, fill_width,
                                    exp_bar_height)
            pygame.draw.rect(self.display_surface, (255, 215, 0), fill_rect)

        # Level text
        level_text = self.ball_sim.font.render(f"Level: {self.data.level}",
                                               True, "white")
        level_rect = level_text.get_rect(
            center=(exp_bar_x + exp_bar_width // 2,
                    exp_bar_y + exp_bar_height // 2))
        self.display_surface.blit(level_text, level_rect)

    def update_volume_from_mouse(self, mouse_x):
        """Update volume based on mouse position"""
        left_edge = self.W_WIDTH // 2 - self.slider_width // 2
        right_edge = left_edge + self.slider_width
        clamped_x = max(left_edge, min(right_edge, mouse_x))
        relative_x = clamped_x - left_edge
        self.volume = max(0, min(100, (relative_x / self.slider_width) * 100))

        self.volume_slider.x = int(left_edge +
                                   (self.volume * self.slider_width / 100) -
                                   (self.volume_slider.width // 2))
        self.volume_slider.y = int(245 * self.sY)

    def handle_events(self, event):
        """Handle UI events"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.handle_escape_key()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_scene == 'settings':
                self.resolution_dropdown.handle_event(event)
                if not (self.resolution_dropdown.rect.collidepoint(event.pos) or 
                        (self.resolution_dropdown.is_open and any(rect.collidepoint(event.pos) 
                                                                for rect in self.resolution_dropdown.option_rects))):
                    self.handle_mouse_click(event)
                return
            self.handle_mouse_click(event)

    def handle_escape_key(self):
        """Handle escape key press"""
        if self.current_scene == 'gameplay':
            self.is_paused = not self.is_paused
        elif self.current_scene in ['settings', 'credits']:
            self.switch_scene(self.previous_scene)

    def handle_mouse_click(self, event):
        """Handle mouse click events"""
        mouse_pos = event.pos
        scene_handlers = {
            'main_menu': self.handle_main_menu_click,
            'settings': self.handle_settings_click,
            'credits': self.handle_credits_click,
            'gameplay': self.handle_gameplay_click
        }

        if self.current_scene in scene_handlers:
            scene_handlers[self.current_scene](event, mouse_pos)

    def handle_main_menu_click(self, event, mouse_pos):
        """Handle main menu click events"""
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

    def handle_settings_click(self, event, mouse_pos):
        """Handle settings click events"""
        if self.back_button.check_input(mouse_pos):
            res_str = self.resolution_dropdown.selected_option
            if res_str:
                width, height = map(int, res_str.split('x'))
                self.W_WIDTH = width
                self.W_HEIGHT = height
                self.sX = width / BASE_WIDTH
                self.sY = height / BASE_HEIGHT
                self.recalculate_layout()
            self.switch_scene(self.previous_scene)
        elif self.easy_button.check_input(mouse_pos):
            self.difficulty = 'easy'
        elif self.medium_button.check_input(mouse_pos):
            self.difficulty = 'medium'
        elif self.hard_button.check_input(mouse_pos):
            self.difficulty = 'hard'
        elif self.volume_rect.collidepoint(
                mouse_pos) or self.volume_slider.collidepoint(mouse_pos):
            self.update_volume_from_mouse(mouse_pos[0])
        elif self.apply_button.check_input(mouse_pos):
            self.apply_resolution_change()

    def handle_credits_click(self, event, mouse_pos):
        """Handle credits click events"""
        if self.back_button.check_input(mouse_pos):
            self.switch_scene(self.previous_scene)

    def handle_gameplay_click(self, event, mouse_pos):
        """Handle gameplay click events"""
        if self.data.health <= 0:
            if self.restart_button.check_input(mouse_pos):
                self.restart_game()
        elif self.is_paused:
            self.handle_pause_menu_click(mouse_pos)

    def handle_pause_menu_click(self, mouse_pos):
        """Handle pause menu click events"""
        if self.resume_button.check_input(mouse_pos):
            self.is_paused = False
        elif self.pause_settings_button.check_input(mouse_pos):
            self.switch_scene('settings')
        elif self.pause_credits_button.check_input(mouse_pos):
            self.switch_scene('credits')
        elif self.pause_main_menu_button.check_input(mouse_pos):
            self.switch_scene('main_menu')

    def restart_game(self):
        """Restart the game"""
        self.data = Data(self)
        self.ball_sim = BallSimulation(self.display_surface, self.sX, self.sY,
                                       self.data)
        self.ball_sim.balls.clear()
        self.ball_sim.circles.clear()
        self.ball_sim.can_spawn_circles = True
        self.is_paused = False
        self.draw_background()

    def apply_resolution_change(self):
        """Apply selected resolution change"""
        if not self.resolution_dropdown.selected_option:
            return

        selected_res = self.resolution_dropdown.selected_option
        width, height = map(int, selected_res.split('x'))

        # Only update if resolution actually changed
        if width != self.W_WIDTH or height != self.W_HEIGHT:
            pygame.display.set_mode((width, height))
            self.W_WIDTH = width
            self.W_HEIGHT = height
            self.sX = width / BASE_WIDTH
            self.sY = height / BASE_HEIGHT
            self.recalculate_layout()

    def switch_scene(self, new_scene):
        """Switch to a new scene"""
        self.previous_scene = self.current_scene
        self.current_scene = new_scene