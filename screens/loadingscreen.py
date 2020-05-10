from .screen import Screen
# import pygame
# import math
# import time


class LoadingScreen(Screen):

    def __init__(self):
        super().__init__()

    def render_screen(self, data, display):
        super().render_screen(display)

        display.get_size()
        x, y = display.get_size()
        self.render_font_center(display, self.basic_font,
                                "Loading...", 200, (255, 255, 255),
                                (x // 2, y // 2))
