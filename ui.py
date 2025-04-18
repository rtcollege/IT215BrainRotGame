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
        self.recalculate_layout()

    def recalculate_layout(self):
        # Recalculate fonts
        self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", int(self.base_font_size * min(SCALE_X, SCALE_Y)))
        self.title_font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", int(self.base_title_size * min(SCALE_X, SCALE_Y)))

        # Main menu setup
        self.title_text = self.title_font.render("Brain Rot Game", True, "white")
        self.title_rect = self.title_text.get_rect(topleft=(50, 100))

        # Create buttons
        button_x = int(50 * SCALE_X)  # Left alignment position
        button_y_start = int(300 * SCALE_Y)
        button_y_spacing = int(100 * SCALE_Y)

        self.play_button = Button(None, (button_x, button_y_start), "Play", self.font, "white", "#b68f40")
        self.settings_button = Button(None, (button_x, button_y_start + button_y_spacing), "Settings", self.font, "white", "#b68f40")
        self.credits_button = Button(None, (button_x, button_y_start + 2 * button_y_spacing), "Credits", self.font, "white", "#b68f40")
        self.quit_button = Button(None, (button_x, button_y_start + 3 * button_y_spacing), "Quit", self.font, "white", "#b68f40")

        # Settings scene setup
        self.settings_title = self.title_font.render("Settings", True, "white")
        self.settings_title_rect = self.settings_title.get_rect(topleft=(50, 100))

        # Volume slider
        self.volume_text = self.font.render("Volume:", True, "white")
        text_height = self.volume_text.get_height()
        self.volume_text_rect = self.volume_text.get_rect(topleft=(50, (250 * SCALE_Y) - (text_height/2) * SCALE_Y))
        slider_width = int(200 * SCALE_X)
        slider_height = int(20 * SCALE_Y)
        slider_handle_width = int(20 * SCALE_X)
        slider_handle_height = int(30 * SCALE_Y)

        self.slider_width = int(200 * SCALE_X)
        self.volume = 50
        self.volume_slider = pygame.Rect(
            WINDOW_WIDTH/2 - self.slider_width/2 + (self.volume * self.slider_width/100),
            int(245 * SCALE_Y),
            slider_handle_width,
            slider_handle_height
        )


        self.volume_rect = pygame.Rect(WINDOW_WIDTH/2 - slider_width/2, int(250 * SCALE_Y), slider_width, slider_height)

        # Difficulty buttons
        diff_y = 400
        self.difficulty_text = self.font.render("Difficulty:", True, "white")
        text_height = self.difficulty_text.get_height()
        self.difficulty_text_rect = self.difficulty_text.get_rect(topleft=(50, (diff_y * SCALE_Y) - (text_height/2) * SCALE_Y))
        button_spacing = int(200 * SCALE_X)  # Consistent spacing between buttons
        self.easy_button = Button(None, (WINDOW_WIDTH/2 - button_spacing, int(diff_y * SCALE_Y)), "Easy", self.font, "white", "#b68f40")
        self.medium_button = Button(None, (WINDOW_WIDTH/2, int(diff_y * SCALE_Y)), "Medium", self.font, "white", "#b68f40")
        self.hard_button = Button(None, (WINDOW_WIDTH/2 + button_spacing, int(diff_y * SCALE_Y)), "Hard", self.font, "white", "#b68f40")

        # Resolution selector
        res_y = diff_y + int(100 * SCALE_Y)
        self.resolution_text = self.font.render("Resolution:", True, "white")
        text_height = self.resolution_text.get_height()
        self.resolution_text_rect = self.resolution_text.get_rect(topleft=(50, (res_y * SCALE_Y) - (text_height/2) * SCALE_Y))
        
        self.resolution_buttons = []
        current_res = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        for i, (width, height) in enumerate(RESOLUTIONS):
            res_button = Button(
                None, 
                (WINDOW_WIDTH/2 + (i - len(RESOLUTIONS)/2 + 0.5) * button_spacing, int(res_y * SCALE_Y)),
                f"{width}x{height}",
                self.font,
                "white",
                "#b68f40"
            )
            self.resolution_buttons.append((res_button, (width, height)))

        # Back button - positioned at the same x position as main menu buttons
        self.back_button = Button(
            None, 
            (button_x, button_y_start + 3 * button_y_spacing), 
            "Back", 
            self.font, 
            "white", 
            "#b68f40"
        )
        

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