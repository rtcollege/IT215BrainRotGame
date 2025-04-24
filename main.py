
from settings import *
from data import Data
from debug import debug
from ui import UI


class Main:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Create the display surface
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game")

        # Create clock for framerate
        self.clock = pygame.time.Clock()

        # Load assets
        self.import_assets()

        # Initialize UI and Game
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.game = Game(self.ui)

    def import_assets(self):
        self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", 40)

        self.ui_frames = {
            'currency': pygame.image.load('graphics/ui/currency.png').convert_alpha()
        }

    def check_game_over(self):
        """Check for game over conditions"""
        pass

    def handle_events(self):
        """Handle all pygame events"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Pass events to UI
            self.ui.handle_events(event)

    def run(self):
        """Main game loop"""
        while True:
            # Delta time
            dt = self.clock.tick(FPS) / 1000

            # Handle events
            self.handle_events()

            # Update game state
            self.display_surface.fill("gray")
            self.game.update(dt)
            self.ui.update(dt)
            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()
