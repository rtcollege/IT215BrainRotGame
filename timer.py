from pygame.time import get_ticks

class Timer:
def __init__(self, duration, function=None):
    self.duration = duration
    self.function = function
    self.active = False
    self.start_ticks = 0

def activate(self):
    self.active = True
    self.start_ticks = get_ticks()

def deactivate(self):
    self.active = False

def update(self):
    if self.active:
        now = get_ticks()
        if now - self.start_ticks > self.duration:
            if self.function:
                self.function()
            self.deactivate()