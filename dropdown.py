
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
        self.hover_index = -1
        
        # Create background rects for all options
        self.option_rects = []
        for i in range(len(options)):
            # Start options below the button
            y_pos = (y - (text_height + self.padding_y) // 2) + self.rect.height + (i * height)
            self.option_rects.append(
                pygame.Rect(x, y_pos, width, height)
            )
            
    def draw(self, surface):
        # Draw main button
        pygame.draw.rect(surface, "#4a4a4a", self.rect, 0, border_radius=10)
        pygame.draw.rect(surface, "#b68f40", self.rect, 2, border_radius=10)
        print("Drawing Dropdown...")

        # Draw selected option
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

        # Debugging if dropdown is open or closed
        print(f"Dropdown is {'open' if self.is_open else 'closed'}")

        # Draw dropdown options if open
        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = self.option_rects[i]
                if i == self.hover_index:
                    pygame.draw.rect(surface, "#5a5a5a", option_rect, 0, border_radius=10)
                else:
                    pygame.draw.rect(surface, "#4a4a4a", option_rect, 0, border_radius=10)
                pygame.draw.rect(surface, "#b68f40", option_rect, 2, border_radius=10)

                text = self.font.render(option, True, "#ffffff")
                text_rect = text.get_rect(midleft=(option_rect.x + self.padding_x//2, option_rect.centery))
                surface.blit(text, text_rect)
                
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(f"Clicked at {mouse_pos}")  # Debug click position

            # Check if click is within the main button
            if self.rect.collidepoint(mouse_pos):
                self.is_open = not self.is_open
                print(f"Dropdown {'opened' if self.is_open else 'closed'}")
                return True

            # If dropdown is open, check options and outside clicks
            if self.is_open:
                # Check if click is within any option
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_option = self.options[i]
                        self.is_open = False
                        print(f"Option {self.selected_option} selected.")
                        return True
                
                # If click is outside both the button and options, close the dropdown
                self.is_open = False
                print("Dropdown closed - clicked outside")
                return True
                
        return False
