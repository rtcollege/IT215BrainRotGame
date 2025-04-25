
from data import Data
from ball import Ball
from circle import Circle

class GameModel:
    def __init__(self):
        self.data = Data(None)  # UI will be set later
        self.balls = []
        self.circles = []
        self.base_radius = 150
        self.current_scene = 'main_menu'
        self.is_paused = False
        self.difficulty = 'medium'
        self.volume = 75

    def add_ball(self, x, y, radius):
        self.balls.append(Ball(x, y, radius))

    def add_circle(self, radius):
        self.circles.append(Circle(radius))

    def update(self, dt):
        for circle in self.circles:
            circle.update(dt)
        for ball in self.balls:
            ball.update(dt)
