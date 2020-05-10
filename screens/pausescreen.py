from .screen import Screen
# from .racescreen import RaceScreen
import pygame
# import math
# import time


class PauseScreen(Screen):

    def __init__(self):
        super().__init__()

    def render_screen(self, data, display, pip=None):
        super().render_screen(display)

        display.fill((10, 10, 10))
        # Render bottom left
        # items = ["Location:", "Length:", "Car:"]
        # #                                                   60 = font_size + gap
        # self.render_lines(display, self.basic_font,
        #                   (300, self.display.get_height() - (60 * len(items))),
        #                   items, (255, 255, 255), 60, 0,
        #                   self.render_font_right)

        items = ["{:.2f} km".format(data['eventInformation']['mTrackLength'] / 1000),
                 data['eventInformation']['mTranslatedTrackLocation'],
                 data['vehicleInformation']['mCarName']]
        # items = [self.condence_string(i, 15) for i in items]
        #                                                   60 = font_size + gap
        self.render_lines(display, self.basic_font,
                          (5, display.get_height() - (65 * len(items))),
                          items, (255, 255, 0), 60, 5,
                          self.render_font)

        # Render center
        items = []
        m = int(data['timings']['mPersonalFastestLapTime'] // 60)
        s = int(data['timings']['mPersonalFastestLapTime'] % 60)
        ms = int((data['timings']['mPersonalFastestLapTime'] % 1) * 1000)
        items.append("{}:{}.{}".format(m, s, ms))
        m = int(data['timings']['mWorldFastestLapTime'] // 60)
        s = int(data['timings']['mWorldFastestLapTime'] % 60)
        ms = int((data['timings']['mWorldFastestLapTime'] % 1) * 1000)
        items.append("{}:{}.{}".format(m, s, ms))

        # items = ["{:.0f}:{}".format(data['timings']['mPersonalFastestLapTime'] // 60, str(data['timings']['mPersonalFastestLapTime'] % 60).zfill(6)),
        #          "{:.0f}:{}".format(data['timings']['mWorldFastestLapTime'] // 60, str(data['timings']['mWorldFastestLapTime'] % 60).zfill(6))]
        width, height = self.render_lines(display, self.basic_font,
                                          (display.get_width(), 0),
                                          items, (255, 255, 255), 60, 0,
                                          self.render_font_right)

        items = ["PB ", "WB "]
        self.render_lines(display, self.basic_font,
                          (display.get_width() - width, 0),
                          items, (255, 255, 255), 60, 0,
                          self.render_font_right)

        # # Picture in Picture
        # ratio = 2/3
        # if pip:
        #     pip_surface = pygame.Surface((display.get_width() * ratio, display.get_height() * ratio))
        #     pip.render_screen(data, pip_surface)
        #     display.blit(pip_surface, (0, 0))

        # mini_surface = pygame.Surface((self.display.get_width() * (2/3), self.display.get_height() * (2/3)))
        # race_screen = RaceScreen(mini, False)
        # race_screen.render_screen(data)
        # self.display.blit(self.mini, (0, 0))
