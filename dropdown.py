import pygame

class Dropdown:
    def __init__(self, x, y, width, height, options, font, selected_option):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.font = font
        self.selected_option = selected_option
        self.is_open = False
        self.option_rects = []
        self.hover_index = -1
        self.padding_x = 10
        self.setup_option_rects()

    def setup_option_rects(self):
        """Set up the positions and dimensions of the option buttons in the dropdown."""
        self.option_rects = []
        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height * (i + 1), self.rect.width, self.rect.height)
            self.option_rects.append(option_rect)

    def handle_event(self, event):
        """Handle user interaction with the dropdown."""
        print("Dropdown handle_event called")
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"Click position: {event.pos}")
            print(f"Dropdown rect: {self.rect}")
            if self.rect.collidepoint(event.pos):
                print("Dropdown clicked!")
                self.toggle_dropdown()
                print(f"Dropdown is now {'open' if self.is_open else 'closed'}")
            if self.is_open:
                print("Checking option rects...")
                for i, option_rect in enumerate(self.option_rects):
                    print(f"Option {i} rect: {option_rect}")
                    if option_rect.collidepoint(event.pos):
                        print(f"Option {i} selected: {self.options[i]}")
                        self.select_option(i)
                        break

    def toggle_dropdown(self):
        """Toggle the dropdown state (open/close)."""
        self.is_open = not self.is_open

    def select_option(self, index):
        """Select a resolution option from the dropdown."""
        self.selected_option = self.options[index]
        self.is_open = False  # Close the dropdown after selection
        print(f"Resolution selected: {self.selected_option}")

    def draw(self, surface):
        """Draw the dropdown and its options on the surface."""
        # Draw the main dropdown button
        pygame.draw.rect(surface, "#4a4a4a", self.rect, 0, border_radius=10)
        pygame.draw.rect(surface, "#b68f40", self.rect, 2, border_radius=10)

        # Draw selected option text
        text = self.font.render(self.selected_option, True, "#ffffff")
        text_rect = text.get_rect(midleft=(self.rect.x + self.padding_x, self.rect.centery))
        surface.blit(text, text_rect)

        # Draw the dropdown arrow
        arrow_points = [
            (self.rect.right - 20, self.rect.centery - 5),
            (self.rect.right - 10, self.rect.centery + 5),
            (self.rect.right - 30, self.rect.centery + 5)
        ]
        pygame.draw.polygon(surface, "#ffffff", arrow_points)

        # Draw the dropdown options if open
        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = self.option_rects[i]
                # Draw the option button
                if i == self.hover_index:
                    pygame.draw.rect(surface, "#5a5a5a", option_rect, 0, border_radius=10)
                else:
                    pygame.draw.rect(surface, "#4a4a4a", option_rect, 0, border_radius=10)
                pygame.draw.rect(surface, "#b68f40", option_rect, 2, border_radius=10)

                # Render and draw option text
                option_text = self.font.render(option, True, "#ffffff")
                option_text_rect = option_text.get_rect(midleft=(option_rect.x + self.padding_x, option_rect.centery))
                surface.blit(option_text, option_text_rect)

    def update(self, mouse_pos):
        """Update the hover index based on mouse position."""
        self.hover_index = -1
        if self.is_open:
            for i, option_rect in enumerate(self.option_rects):
                if option_rect.collidepoint(mouse_pos):
                    self.hover_index = i
                    break
