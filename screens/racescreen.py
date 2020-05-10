from .screen import Screen
import pygame
import pygame.gfxdraw
import time
# import math


class RaceScreen(Screen):
    flash = True

    def __init__(self, flash=True):
        super().__init__()
        self.flash = flash

    def render_screen(self, data, display):
        super().render_screen(display)

        pct = data['carState']['mRpm']/data['carState']['mMaxRPM']

        # Flash screen
        if pct > 0.95:
            if self.flash:
                if int(time.time() * 10) % 2 == 0:
                    display.fill((100, 0, 0))
                else:
                    display.fill((0, 0, 0))
            else:
                display.fill((100, 0, 0))
        else:
            display.fill((0, 0, 0))

        # RPM Meter
        # p is the "percent" of the RPM to show the meter off the top.
        # eg. p = 0.25 with 8,000 redline will show the RPM bar from 6,000 - 8,000 RPM.
        # eg. p = 1 will show the entire RPM bar for the entire time.
        p = 0.3
        rpm_bar_height = 100 * self.scale_y
        if pct > (1 - p):
            t = (pct - (1 - p)) * (1/p)
            r = 255 * t if 255 * t <= 255 else 255 if 255 * t > 0 else 0
            g = 255 - (255 * t) if 255 - (255 * t) > 0 else 0
            color = (r, g, 0)
            pygame.draw.rect(display,
                             color,
                             (0, 0, display.get_width() * t, rpm_bar_height))

        # Current RPM, drawn in RPM bar
        rpm_x, rpm_y = self.render_font_top_center(display, self.basic_font,
                                                   "{:.0f}".format(data['carState']['mRpm']),
                                                   rpm_bar_height, (255, 255, 255),
                                                   (display.get_width() // 2, 5))

        # Current Speed
        meters = data['carState']['mSpeed']
        miles = meters / 0.44704
        _w, _h = self.render_font_top_center(display, self.basic_font,
                                             "{:.0f}".format(miles),
                                             self.scale_y * 100, (255, 255, 255),
                                             (display.get_width() // 2, rpm_bar_height))

        self.render_font_top_center(display, self.basic_font,
                                    "MPH",
                                    self.scale_y * 50, (255, 255, 255),
                                    (display.get_width() // 2, _h + rpm_bar_height))

        # Current Gear
        self.render_font_center(display, self.digital_font,
                                str(data['carState']['mGear']),
                                self.scale_y * 500, (255, 255, 255),
                                (display.get_width() // 2, display.get_height() // 2))

        # Boost Pressure

        #   Using arc. Looks really bad, has holes and gaps in lines, but best so far.
        # pygame.draw.arc(display, (255, 255, 255), (100, 100, 300, 300), 0, math.pi * pct, 50)

        #   gfxdraw circles. Doesnt allow for drawing semi-circles.
        # pygame.gfxdraw.aacircle(display, 100, 100, 50, (255, 255, 255))
        # pygame.gfxdraw.filled_circle(display, 100, 100, 50, (255, 255, 255))