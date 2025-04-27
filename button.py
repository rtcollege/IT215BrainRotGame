import pygame


class Button:
    def __init__(self, image, position, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.font = font
        self.base_color = "#ffffff"  # White text
        self.hovering_color = "#b68f40"  # Warm gold hover color
        self.button_color = "#4a4a4a"  # Button background color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        
        # Add padding to text area
        from settings import SCALE_X, SCALE_Y
        self.padding_x = int(40 * SCALE_X)
        self.padding_y = int(20 * SCALE_Y)
        
        if self.image is not None:
            self.image = pygame.transform.scale(self.image, 
                (self.text.get_width() + self.padding_x, self.text.get_height() + self.padding_y))
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = pygame.Rect(
                self.x_pos,
                self.y_pos - (self.text.get_height() + self.padding_y) // 2,
                self.text.get_width() + self.padding_x,
                self.text.get_height() + self.padding_y
            )
        
        self.text_rect = self.text.get_rect(midleft=(self.x_pos + self.padding_x//2, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        else:
            # Draw button with consistent background and outline
            pygame.draw.rect(screen, self.button_color, self.rect, 0, border_radius=10)
            pygame.draw.rect(screen, self.hovering_color, self.rect, 2, border_radius=10)
        screen.blit(self.text, self.text_rect)

    def check_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            
    def set_position(self, new_pos):
        self.x_pos = new_pos[0]
        self.y_pos = new_pos[1]
        if self.image is not None:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = pygame.Rect(
                self.x_pos,
                self.y_pos - (self.text.get_height() + self.padding_y) // 2,
                self.text.get_width() + self.padding_x,
                self.text.get_height() + self.padding_y
            )
        self.text_rect = self.text.get_rect(midleft=(self.x_pos + self.padding_x//2, self.y_pos))

    def update_font(self, new_font):
        self.font = new_font
        self.text = self.font.render(self.text_input, True, self.base_color)

        # Update the rect based on new text size
        if self.image is not None:
            self.image = pygame.transform.scale(self.image, 
                (self.text.get_width() + self.padding_x, self.text.get_height() + self.padding_y))
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = pygame.Rect(
                self.x_pos,
                self.y_pos - (self.text.get_height() + self.padding_y) // 2,
                self.text.get_width() + self.padding_x,
                self.text.get_height() + self.padding_y
            )

        # Recalculate the text_rect position after font change
        self.text_rect = self.text.get_rect(midleft=(self.x_pos + self.padding_x//2, self.y_pos))

