
import pygame

class Dropdown:
    def __init__(self, x, y, width, height, options, font, default_option=None):
        from settings import SCALE_X, SCALE_Y
        self.padding_x = int(40 * SCALE_X)
        self.padding_y = int(20 * SCALE_Y)

        # Calculate proper height based on text and padding
        text_height = font.render(options[0], True, "#ffffff").get_height()
        adjusted_height = text_height + self.padding_y

        self.rect = pygame.Rect(x, (y - (text_height + self.padding_y) // 2), width, adjusted_height)
        self.options = options
        self.font = font
        self.is_open = False
        self.selected_option = default_option if default_option else options[0]
        self.option_height = adjusted_height

        # Create button rects for all options
        self.option_rects = []
        self.option_buttons = []
        for i in range(len(options)):
            # Start options below the button
            y_pos = self.rect.bottom + (i * adjusted_height)
            option_rect = pygame.Rect(x, y_pos, width, adjusted_height)
            self.option_rects.append(option_rect)
            
            # Create text surface for each option
            text = font.render(options[i], True, "#ffffff")
            text_rect = text.get_rect(midleft=(x + 10, y_pos + adjusted_height // 2))
            self.option_buttons.append((text, text_rect, option_rect))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check if main button is clicked
            if self.rect.collidepoint(mouse_pos):
                self.is_open = not self.is_open
                return True

            # If dropdown is open, check for option clicks
            if self.is_open:
                for i, (_, _, button_rect) in enumerate(self.option_buttons):
                    if button_rect.collidepoint(mouse_pos):
                        self.selected_option = self.options[i]
                        self.is_open = False
                        return True

                # Click outside both button and options - close dropdown
                self.is_open = False
                return True

        return False

    def draw(self, surface):
        # Draw main button
        pygame.draw.rect(surface, "#4a4a4a", self.rect, 0, border_radius=10)
        pygame.draw.rect(surface, "#b68f40", self.rect, 2, border_radius=10)

        # Draw selected option text
        text = self.font.render(self.selected_option, True, "#ffffff")
        text_rect = text.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        surface.blit(text, text_rect)

        # Draw dropdown arrow
        arrow_points = [
            (self.rect.right - 20, self.rect.centery - 5),
            (self.rect.right - 10, self.rect.centery + 5),
            (self.rect.right - 30, self.rect.centery + 5)
        ]
        pygame.draw.polygon(surface, "#ffffff", arrow_points)

        # Draw options if dropdown is open
        if self.is_open:
            for text_surf, text_rect, button_rect in self.option_buttons:
                # Draw button background
                pygame.draw.rect(surface, "#4a4a4a", button_rect, 0, border_radius=10)
                pygame.draw.rect(surface, "#b68f40", button_rect, 2, border_radius=10)
                
                # Draw option text
                surface.blit(text_surf, text_rect)
