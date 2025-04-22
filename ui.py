from settings import *
from timer import Timer
from button import Button

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.base_font_size = 40
        
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
                    for button, (width, height) in self.resolution_buttons:
                        if button.check_input(mouse_pos):
                            pygame.display.set_mode((width, height))
                            self.W_WIDTH = width
                            self.W_HEIGHT = height
                            self.sX = width / settings.BASE_WIDTH
                            self.sY = height / settings.BASE_HEIGHT
                            self.recalculate_layout()
                            slider_x = self.W_WIDTH // 2 - self.slider_width // 2 + int((self.volume / 100) * self.slider_width)
                            self.volume_slider.x = slider_x
                            break
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
        self.base_title_size = 60
        self.frames = frames
        self.current_scene = 'main_menu'
        self.previous_scene = 'main_menu'
        self.is_paused = False
        self.difficulty = 'medium'
        self.volume = 50
        self.W_WIDTH = WINDOW_WIDTH
        self.W_HEIGHT = WINDOW_HEIGHT
        self.sX = SCALE_X
        self.sY = SCALE_Y

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
        self.title_font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", int(self.base_title_size * min(self.sX, self.sY)))

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

        self.easy_button.update_font(self.font)
        self.easy_button.set_position((self.W_WIDTH // 2 - button_spacing, diff_y))

        self.medium_button.update_font(self.font)
        self.medium_button.set_position((self.W_WIDTH // 2, diff_y))

        self.hard_button.update_font(self.font)
        self.hard_button.set_position((self.W_WIDTH // 2 + button_spacing, diff_y))

        # Resolution section
        res_y = diff_y + int(100 * self.sY)
        self.resolution_text = self.font.render("Resolution:", True, "white")
        text_height = self.resolution_text.get_height()
        self.resolution_text_rect = self.resolution_text.get_rect(topleft=(button_x, res_y - text_height // 2))

        for i, (button, _) in enumerate(self.resolution_buttons):
            button.update_font(self.font)
            button.set_position((
                self.W_WIDTH // 2 + (i - len(self.resolution_buttons)/2 + 0.5) * button_spacing,
                res_y
            ))

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



    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()

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

            # Draw volume label and slider
            self.display_surface.blit(self.volume_text, self.volume_text_rect)
            self.display_surface.blit(self.difficulty_text, self.difficulty_text_rect)
            pygame.draw.rect(self.display_surface, "white", self.volume_rect, 2)
            pygame.draw.rect(self.display_surface, "white", self.volume_slider)

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

            # Draw resolution text and buttons
            self.display_surface.blit(self.resolution_text, self.resolution_text_rect)
            current_res = f"{self.W_WIDTH}x{self.W_HEIGHT}"
            for button, (width, height) in self.resolution_buttons:
                button.update(self.display_surface)
                if current_res == f"{width}x{height}":
                    pygame.draw.rect(self.display_surface, "white", button.rect, 3)

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
            if self.is_paused:
                # Draw semi-transparent overlay
                overlay = pygame.Surface((self.W_WIDTH, self.W_HEIGHT))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(128)
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