
from settings import *
from timer import Timer
from button import Button

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font
        
        # Main menu setup
        self.title_text = self.font.render("Brain Rot Game", True, "white")
        self.title_rect = self.title_text.get_rect(midtop=(WINDOW_WIDTH/2, 100))
        
        # Create buttons
        button_y_start = 300
        button_y_spacing = 100
        
        self.play_button = Button(
            None, 
            (WINDOW_WIDTH/2, button_y_start), 
            "Play", 
            self.font, 
            "white", 
            "#b68f40"
        )
        
        self.settings_button = Button(
            None,
            (WINDOW_WIDTH/2, button_y_start + button_y_spacing),
            "Settings",
            self.font,
            "white",
            "#b68f40"
        )
        
        self.quit_button = Button(
            None,
            (WINDOW_WIDTH/2, button_y_start + 2 * button_y_spacing),
            "Quit",
            self.font,
            "white",
            "#b68f40"
        )

    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font
        self.title_font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", 60)  # Bigger font for titles
        self.current_scene = 'main_menu'
        self.difficulty = 'medium'
        self.volume = 50
        
        # Main menu setup
        self.title_text = self.title_font.render("Brain Rot Game", True, "white")
        self.title_rect = self.title_text.get_rect(midtop=(WINDOW_WIDTH/2, 100))
        
        # Create buttons
        button_y_start = 300
        button_y_spacing = 100
        
        self.play_button = Button(None, (WINDOW_WIDTH/2, button_y_start), "Play", self.font, "white", "#b68f40")
        self.settings_button = Button(None, (WINDOW_WIDTH/2, button_y_start + button_y_spacing), "Settings", self.font, "white", "#b68f40")
        self.quit_button = Button(None, (WINDOW_WIDTH/2, button_y_start + 2 * button_y_spacing), "Quit", self.font, "white", "#b68f40")
        
        # Settings scene setup
        self.settings_title = self.title_font.render("Settings", True, "white")
        self.settings_title_rect = self.settings_title.get_rect(midtop=(WINDOW_WIDTH/2, 100))
        
        # Volume slider
        self.volume_text = self.font.render("Volume", True, "white")
        self.volume_rect = pygame.Rect(WINDOW_WIDTH/2 - 100, 250, 200, 20)
        self.volume_slider = pygame.Rect(WINDOW_WIDTH/2 - 100 + (self.volume * 2), 245, 20, 30)
        
        # Difficulty buttons
        diff_y = 400
        self.easy_button = Button(None, (WINDOW_WIDTH/2 - 200, diff_y), "Easy", self.font, "white", "#b68f40")
        self.medium_button = Button(None, (WINDOW_WIDTH/2, diff_y), "Medium", self.font, "white", "#b68f40")
        self.hard_button = Button(None, (WINDOW_WIDTH/2 + 200, diff_y), "Hard", self.font, "white", "#b68f40")
        
        # Back button - positioned with safe padding from bottom-left corner
        padding = 60  # increased padding from window edges
        button_text = self.font.render("Back", True, "white")
        button_height = button_text.get_height()
        button_width = button_text.get_width()
        # Ensure button position respects minimum window boundaries
        x_pos = max(padding + button_width/2, button_width + padding)
        y_pos = min(WINDOW_HEIGHT - padding - button_height/2, WINDOW_HEIGHT - button_height - padding)
        self.back_button = Button(
            None, 
            (x_pos, y_pos), 
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
            self.quit_button.update(self.display_surface)
            
            # Update button colors based on hover
            self.play_button.change_color(mouse_pos)
            self.settings_button.change_color(mouse_pos)
            self.quit_button.change_color(mouse_pos)
            
        elif self.current_scene == 'settings':
            # Draw settings title
            self.display_surface.blit(self.settings_title, self.settings_title_rect)
            
            # Draw volume slider
            self.display_surface.blit(self.volume_text, (WINDOW_WIDTH/2 - 100, 220))
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
            
            # Update back button
            self.back_button.update(self.display_surface)
            self.back_button.change_color(mouse_pos)
            
            # Handle volume slider dragging
            if pygame.mouse.get_pressed()[0]:
                if self.volume_rect.collidepoint(mouse_pos):
                    self.volume = (mouse_pos[0] - (WINDOW_WIDTH/2 - 100)) // 2
                    self.volume = max(0, min(100, self.volume))
                    self.volume_slider.x = int(WINDOW_WIDTH/2 - 100 + (self.volume * 2))
