from settings import *
from data import Data
from debug import debug
from ui import UI
from ballsimulation import BallSimulation


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

        # Initialize data
        self.data = Data(None)  # Initialize Data without UI reference

        # Initialize UI and pass data reference
        self.ui = UI(self.font, self.ui_frames, self.data)

    def import_assets(self):
        self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", 40)

        self.ui_frames = {
            'currency': pygame.image.load('graphics/ui/currency.png').convert_alpha()
        }

    def check_game_over(self):
        """Check for game over conditions"""
        return self.ui.data.health <= 0 if hasattr(self.ui, 'ball_sim') else False

    def handle_events(self):
        """Handle all pygame events"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.ui.current_scene == 'gameplay':
                    self.ui.is_paused = not self.ui.is_paused
                elif self.ui.current_scene in ['settings', 'credits']:
                    self.ui.switch_scene(self.ui.previous_scene)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(mouse_pos)

    def handle_mouse_click(self, mouse_pos):
        """Handle mouse click events based on current scene"""
        current_scene = self.ui.current_scene
        
        if current_scene == 'main_menu':
            if self.ui.play_button.check_input(mouse_pos):
                self.ui.switch_scene('gameplay')
                self.ui.is_paused = False
            elif self.ui.settings_button.check_input(mouse_pos):
                self.ui.switch_scene('settings')
            elif self.ui.credits_button.check_input(mouse_pos):
                self.ui.switch_scene('credits')
            elif self.ui.quit_button.check_input(mouse_pos):
                pygame.quit()
                sys.exit()
                
        elif current_scene == 'settings':
            if self.ui.back_button.check_input(mouse_pos):
                self.ui.switch_scene(self.ui.previous_scene)
            elif self.ui.easy_button.check_input(mouse_pos):
                self.ui.difficulty = 'easy'
            elif self.ui.medium_button.check_input(mouse_pos):
                self.ui.difficulty = 'medium'
            elif self.ui.hard_button.check_input(mouse_pos):
                self.ui.difficulty = 'hard'
                
        elif current_scene == 'credits':
            if self.ui.back_button.check_input(mouse_pos):
                self.ui.switch_scene(self.ui.previous_scene)
                
        elif current_scene == 'gameplay':
            if self.ui.restart_button.check_input(mouse_pos):
                self.data = Data(self.ui)
                self.data.health = 100
                self.data.currency = 0
                self.ui.ball_sim = BallSimulation(self.display_surface, self.ui.sX, self.ui.sY, self.data)
                self.ui.is_paused = False
            elif self.ui.is_paused:
                if self.ui.resume_button.check_input(mouse_pos):
                    self.ui.is_paused = False
                elif self.ui.pause_settings_button.check_input(mouse_pos):
                    self.ui.switch_scene('settings')
                elif self.ui.pause_credits_button.check_input(mouse_pos):
                    self.ui.switch_scene('credits')
                elif self.ui.pause_main_menu_button.check_input(mouse_pos):
                    self.ui.switch_scene('main_menu')

    def run(self):
        """Main game loop"""
        while True:
            # Delta time
            dt = self.clock.tick(FPS) / 1000

            # Handle events
            self.handle_events()

            # Update game state
            self.display_surface.fill("gray")
            self.ui.update(dt)
            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()