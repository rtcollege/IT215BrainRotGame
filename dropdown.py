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

        # Create background rects for all options
        self.option_rects = []
        for i in range(len(options)):
            # Start options below the button
            y_pos = self.rect.bottom + (i * adjusted_height)
            self.option_rects.append(
                pygame.Rect(x, y_pos, width, adjusted_height)
            )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(f"Dropdown clicked at {mouse_pos}")

            # Check if main button is clicked
            if self.rect.collidepoint(mouse_pos):
                self.is_open = not self.is_open
                print(f"Main dropdown button clicked. Is open: {self.is_open}")
                return True

            # If dropdown is open, check for option clicks
            if self.is_open:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_option = self.options[i]
                        self.is_open = False
                        print(f"Selected option: {self.selected_option}")
                        return True

                # Click outside both button and options - close dropdown
                self.is_open = False
                print("Clicked outside dropdown - closing")
                return True

        return False

    def draw(self, surface):
        print(f"Drawing dropdown - Is open: {self.is_open}, Selected: {self.selected_option}")
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
            for i, (option, rect) in enumerate(zip(self.options, self.option_rects)):
                # Draw option background
                pygame.draw.rect(surface, "#4a4a4a", rect, 0, border_radius=10)
                pygame.draw.rect(surface, "#b68f40", rect, 2, border_radius=10)

                # Draw option text
                text = self.font.render(option, True, "#ffffff")
                text_rect = text.get_rect(midleft=(rect.x + 10, rect.centery))
                surface.blit(text, text_rect)