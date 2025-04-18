from settings import *
from timer import Timer
from button import Button

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.base_font_size = 40
        self.base_title_size = 60
        self.frames = frames
        self.current_scene = 'main_menu'
        self.difficulty = 'medium'
        self.volume = 50

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
        self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", int(self.base_font_size * min(SCALE_X, SCALE_Y)))
        self.title_font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", int(self.base_title_size * min(SCALE_X, SCALE_Y)))

        # Update font in all buttons
        for button in [self.play_button, self.settings_button, self.credits_button, self.quit_button,
                       self.easy_button, self.medium_button, self.hard_button, self.back_button]:
            button.font = self.font
            button.text = button.font.render(button.text_input, True, button.base_color)
            button.set_position((button.x_pos, button.y_pos))  # Recalculate rects

        for res_button, _ in self.resolution_buttons:
            res_button.font = self.font
            res_button.text = res_button.font.render(res_button.text_input, True, res_button.base_color)
            res_button.set_position((res_button.x_pos, res_button.y_pos))


        # Layout positions
        button_x = int(50 * SCALE_X)
        button_y_start = int(300 * SCALE_Y)
        button_y_spacing = int(100 * SCALE_Y)

        # Main menu title
        self.title_text = self.title_font.render("Brain Rot Game", True, "white")
        self.title_rect = self.title_text.get_rect(topleft=(button_x, int(100 * SCALE_Y)))

        # Main menu buttons
        self.play_button.set_position((button_x, button_y_start))
        self.settings_button.set_position((button_x, button_y_start + button_y_spacing))
        self.credits_button.set_position((button_x, button_y_start + 2 * button_y_spacing))
        self.quit_button.set_position((button_x, button_y_start + 3 * button_y_spacing))

        # Settings title
        self.settings_title = self.title_font.render("Settings", True, "white")
        self.settings_title_rect = self.settings_title.get_rect(topleft=(button_x, int(100 * SCALE_Y)))

        # Volume slider
        volume_y = int(250 * SCALE_Y)
        self.volume_text = self.font.render("Volume:", True, "white")
        text_height = self.volume_text.get_height()
        self.volume_text_rect = self.volume_text.get_rect(topleft=(button_x, volume_y - text_height // 2))

        self.slider_width = int(200 * SCALE_X)
        slider_height = int(20 * SCALE_Y)
        slider_handle_width = int(20 * SCALE_X)
        slider_handle_height = int(30 * SCALE_Y)

        self.volume_rect = pygame.Rect(
            WINDOW_WIDTH // 2 - self.slider_width // 2,
            volume_y,
            self.slider_width,
            slider_height
        )
        self.volume_slider = pygame.Rect(
            WINDOW_WIDTH // 2 - self.slider_width // 2 + (self.volume * self.slider_width // 100),
            volume_y + (slider_height // 2) - (slider_handle_height // 2),
            slider_handle_width,
            slider_handle_height
        )

        # Difficulty section
        diff_y = int(400 * SCALE_Y)
        button_spacing = int(200 * SCALE_X)
        self.difficulty_text = self.font.render("Difficulty:", True, "white")
        text_height = self.difficulty_text.get_height()
        self.difficulty_text_rect = self.difficulty_text.get_rect(topleft=(button_x, diff_y - text_height // 2))

        self.easy_button.set_position((WINDOW_WIDTH // 2 - button_spacing, diff_y))
        self.medium_button.set_position((WINDOW_WIDTH // 2, diff_y))
        self.hard_button.set_position((WINDOW_WIDTH // 2 + button_spacing, diff_y))

        # Resolution section
        res_y = diff_y + int(100 * SCALE_Y)
        self.resolution_text = self.font.render("Resolution:", True, "white")
        text_height = self.resolution_text.get_height()
        self.resolution_text_rect = self.resolution_text.get_rect(topleft=(button_x, res_y - text_height // 2))

        for i, (button, _) in enumerate(self.resolution_buttons):
            button.set_position((
                WINDOW_WIDTH // 2 + (i - len(self.resolution_buttons)/2 + 0.5) * button_spacing,
                res_y
            ))

        # Back button (same position as quit)
        self.back_button.set_position((button_x, button_y_start + 3 * button_y_spacing))



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
            current_res = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
            for button, (width, height) in self.resolution_buttons:
                button.update(self.display_surface)
                if current_res == f"{width}x{height}":
                    pygame.draw.rect(self.display_surface, "white", button.rect, 3)

            # Update back button
            self.back_button.update(self.display_surface)
            self.back_button.change_color(mouse_pos)

            # Handle volume slider dragging
            if pygame.mouse.get_pressed()[0]:
                if self.volume_rect.collidepoint(mouse_pos):
                    self.volume = (mouse_pos[0] - (WINDOW_WIDTH/2 - self.slider_width/2)) // (self.slider_width/100)
                    self.volume = max(0, min(100, self.volume))
                    self.volume_slider.x = int(WINDOW_WIDTH/2 - self.slider_width/2 + (self.volume * self.slider_width/100))