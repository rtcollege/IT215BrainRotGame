import settings
from settings import *
from data import Data
from debug import debug
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.ui.current_scene == 'gameplay':
                        self.ui.is_paused = not self.ui.is_paused
                    elif self.ui.current_scene in ['settings', 'credits']:
                        # Store current scene before changing
                        temp_scene = self.ui.current_scene
                        self.ui.current_scene = self.ui.previous_scene
                        self.ui.previous_scene = temp_scene

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui.current_scene == 'main_menu':
                        if self.ui.play_button.check_input(mouse_pos):
                            self.ui.previous_scene = self.ui.current_scene
                            self.ui.current_scene = 'gameplay'
                            self.ui.is_paused = False
                        elif self.ui.settings_button.check_input(mouse_pos):
                            self.ui.previous_scene = self.ui.current_scene
                            self.ui.current_scene = 'settings'
                        elif self.ui.credits_button.check_input(mouse_pos):
                            self.ui.previous_scene = self.ui.current_scene
                            self.ui.current_scene = 'credits'
                        elif self.ui.quit_button.check_input(mouse_pos):
                            pygame.quit()
                            sys.exit()
                    elif self.ui.current_scene == 'settings' or self.ui.current_scene == 'credits':
                        if self.ui.back_button.check_input(mouse_pos):
                            # Store current scene before changing
                            temp_scene = self.ui.current_scene
                            self.ui.current_scene = self.ui.previous_scene
                            self.ui.previous_scene = temp_scene
                        elif self.ui.current_scene == 'settings' and self.ui.easy_button.check_input(mouse_pos):
                            self.ui.difficulty = 'easy'
                        elif self.ui.medium_button.check_input(mouse_pos):
                            self.ui.difficulty = 'medium'
                        elif self.ui.hard_button.check_input(mouse_pos):
                            self.ui.difficulty = 'hard'
                    elif self.ui.current_scene == 'gameplay' and self.ui.is_paused:
                        if self.ui.resume_button.check_input(mouse_pos):
                            self.ui.is_paused = False
                        elif self.ui.pause_settings_button.check_input(mouse_pos):
                            self.ui.previous_scene = 'gameplay'
                            self.ui.current_scene = 'settings'
                        elif self.ui.pause_credits_button.check_input(mouse_pos):
                            self.ui.previous_scene = 'gameplay'
                            self.ui.current_scene = 'credits'
                        elif self.ui.pause_main_menu_button.check_input(mouse_pos):
                            self.ui.current_scene = 'main_menu'
                        for button, (width, height) in self.ui.resolution_buttons:
                            if button.check_input(mouse_pos):
                                pygame.display.set_mode((width, height))
                                self.ui.W_WIDTH = width
                                self.ui.W_HEIGHT = height
                                self.ui.sX = width / settings.BASE_WIDTH
                                self.ui.sY = height / settings.BASE_HEIGHT
                                self.ui.recalculate_layout()
                                # Update volume slider position using UI's values
                                slider_x = self.ui.W_WIDTH // 2 - self.ui.slider_width // 2 + int((self.ui.volume / 100) * self.ui.slider_width)
                                self.ui.volume_slider.x = slider_x
                                break

            self.display_surface.fill("gray")
            self.ui.update(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()