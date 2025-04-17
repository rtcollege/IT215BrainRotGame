
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

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        
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
