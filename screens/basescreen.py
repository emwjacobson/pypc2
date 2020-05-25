from .screen import Screen
# import pygame
# import math
# import time


class BaseScreen(Screen):

    def __init__(self, display):
        super().__init__(display)

    def render_screen(self, data):
        super().render_screen()
