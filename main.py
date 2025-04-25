import pygame
from settings import *
from models.game_model import GameModel
from views.game_view import GameView
from controllers.game_controller import GameController

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game")

        self.model = GameModel()
        self.view = GameView(self.model)
        self.controller = GameController(self.model, self.view)

    def run(self):
        self.controller.run()

if __name__ == '__main__':
    game = Game()
    game.run()