
import pygame

class Dropdown:
    def __init__(self, x, y, width, height, options, font, default_option=None):
        from settings import SCALE_X, SCALE_Y
        self.padding_x = int(40 * SCALE_X)
        self.padding_y = int(20 * SCALE_Y)
        
        # Calculate proper height based on text and padding
        text_height = font.render(options[0], True, "#ffffff").get_height()
        adjusted_height = text_height + self.padding_y
        
        self.rect = pygame.Rect(x, y, width, adjusted_height)
        self.options = options
        self.font = font
        self.is_open = False
        self.selected_option = default_option if default_option else options[0]
        self.option_height = adjusted_height
        self.hover_index = -1
        
        # Create background rects for all options
        self.option_rects = []
        for i in range(len(options)):
            self.option_rects.append(
                pygame.Rect(x, y + (i * height), width, height)
            )
            
    def draw(self, surface):
        # Draw main button
        pygame.draw.rect(surface, "#4a4a4a", self.rect, 0, border_radius=10)
        pygame.draw.rect(surface, "#b68f40", self.rect, 2, border_radius=10)
        
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
            if self.is_open:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_option = self.options[i]
                        self.is_open = False
                        return True
                self.is_open = False
            elif self.rect.collidepoint(mouse_pos):
                self.is_open = True
                
        elif event.type == pygame.MOUSEMOTION and self.is_open:
            mouse_pos = pygame.mouse.get_pos()
            self.hover_index = -1
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(mouse_pos):
                    self.hover_index = i
                    break
        return False
