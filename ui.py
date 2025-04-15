import settings
import sprites
import timer

class UI:
    def __init__(self):
        self.font = settings.FONT
        self.background_frame = sprites.BackgroundFrame()
        self.play_button = sprites.PlayButton()
        self.quit_button = sprites.QuitButton()