
import pygame
import sys

class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.clock = pygame.time.Clock()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.view.ui.handle_events(event)

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000
            self.handle_events()
            self.model.update(dt)
            self.view.render(dt)
