from settings import *
from data import Data
from debug import debug
from timer import Timer
from ui import UI


class Game:
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

        # Initialize UI
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)

        
        
    def import_assets(self):
        self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", 40)
        
        self.ui_frames = {
            'currency': pygame.image.load('graphics/ui/currency.png').convert_alpha()
        }

    

    def check_game_over(self):
        """Check for game over conditions"""
        pass
    
    def run(self):
        """Main game loop"""
        while True:
            # Delta time
            dt = self.clock.tick(FPS) / 1000
            
            # Handle pygame events
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui.current_scene == 'main_menu':
                        if self.ui.play_button.check_input(mouse_pos):
                            print("Play clicked")
                            print("Difficulty:", self.ui.difficulty)
                            print("Volume:", self.ui.volume)
                        elif self.ui.settings_button.check_input(mouse_pos):
                            self.ui.current_scene = 'settings'
                        elif self.ui.quit_button.check_input(mouse_pos):
                            pygame.quit()
                            sys.exit()
                    elif self.ui.current_scene == 'settings':
                        if self.ui.easy_button.check_input(mouse_pos):
                            self.ui.difficulty = 'easy'
                        elif self.ui.medium_button.check_input(mouse_pos):
                            self.ui.difficulty = 'medium'
                        elif self.ui.hard_button.check_input(mouse_pos):
                            self.ui.difficulty = 'hard'
                        # Check resolution buttons
                        for button, (width, height) in self.ui.resolution_buttons:
                            if button.check_input(mouse_pos):
                                pygame.display.set_mode((width, height))
                                settings.WINDOW_WIDTH = width
                                settings.WINDOW_HEIGHT = height
                                settings.SCALE_X = width / settings.BASE_WIDTH
                                settings.SCALE_Y = height / settings.BASE_HEIGHT
                                self.ui = UI(self.font, self.ui_frames)
                                self.ui.current_scene = 'settings'
                                self.ui.difficulty = self.data.difficulty
                                break
                        elif self.ui.back_button.check_input(mouse_pos):
                            self.ui.current_scene = 'main_menu'
                    
            self.display_surface.fill("gray")
            self.ui.update(dt)
            pygame.display.update()
            

if __name__ == '__main__':
    game = Game()
    game.run()
