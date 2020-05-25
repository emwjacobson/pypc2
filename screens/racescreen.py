from .screen import Screen
import pygame
import pygame.gfxdraw
import time
import math


class RaceScreen(Screen):
    flash = True
            # absolute max of [x, z, y] acceleration
    accel = [5, 5, 5]

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
                                self.scale_y * 400, (255, 255, 255),
                                                            # This offset corrects the font being offcenter for some reason.
                                ((display.get_width() // 2) + (20 * self.scale_x), display.get_height() // 2))



        # Acceleration graph
            # x is left/right, z is up/down, y is forward/backwards. All relative to the player sitting in the car.
        x, z, y = [(i / 9.81) for i in data['motionAndDeviceRelated']['mLocalAcceleration']]
        ex, ez, ey = self.accel
        radius = self.scale_y * 200
        if math.fabs(x) > ex and math.fabs(x) < 5:
            print("ex: {}".format(x))
            ex = int(math.fabs(x) + 2)
        if math.fabs(y) > ey and math.fabs(y) < 5:
            print("ey: {}".format(y))
            ey = int(math.fabs(y) + 1)
        if math.fabs(z) > ez and math.fabs(z) < 5:
            ez = int(math.fabs(z) + 1)
        # self.accel = [i if i > 0 else 1 for i in [ex, ey, ez]]
        self.accel = [ex, ez, ey]

            # Create a surface to draw the gauge on to simplify things a little
        gauge = pygame.Surface((int(radius * 2), int(radius * 2)), pygame.SRCALPHA)
            # Outer ring
        pygame.draw.circle(gauge, (9, 180, 227), (gauge.get_width() // 2, gauge.get_height() // 2), radius, 5)
            # Inner Horizontal/Vertical lines
        pygame.draw.line(gauge, (9, 180, 227), (gauge.get_width() // 2, 0), (gauge.get_width() // 2, gauge.get_height())) 
        pygame.draw.line(gauge, (9, 180, 227), (0, gauge.get_height() // 2), (gauge.get_width(), gauge.get_height() // 2))
            # Inner rings
        m = max(ex, ey)
        for i in range(1, m+1):
            pygame.draw.circle(gauge, (9, 180, 227), (gauge.get_width() // 2, gauge.get_height() // 2), (radius * (i / m)), 1)
            self.render_font(gauge, self.basic_font, str(i), int(self.scale_y * 25), (255, 255, 255), ((gauge.get_height() // 2) - (radius * (i / m) - 5), gauge.get_width() // 2))
            # Current G-force dot
        pygame.draw.circle(gauge, (255, 255, 255), ((gauge.get_width() // 2) + int(radius * (x / ex)), (gauge.get_height() // 2) - int(radius * (y / ey))), 5)
            # Current G-force values
        d = [
            "x: {:.2f}".format(math.fabs(x)),
            "y: {:.2f}".format(math.fabs(y))
        ]
        self.render_lines(gauge, self.basic_font, (gauge.get_width(), gauge.get_height() - (2 * 25)), d, (255, 255, 255),
                          20, 5, self.render_font_right)

            # Draw gauge onto main screen
        display.blit(gauge, (display.get_width() - gauge.get_width(), display.get_height() - gauge.get_height()))



        # Gas and Break Bars
            # Could probably do this with just 1 surface, and using the `area` parameter of the .blit() function.
        gas = data['unfilteredInput']['mUnfilteredThrottle']
        brake = data['unfilteredInput']['mUnfilteredBrake']
        radius = self.scale_y * 270
        gas_graph = self.makeCircularGraph(gas, 15, (0, 170, 0), radius)
        gas_graph = pygame.transform.rotate(gas_graph, -90)
        gas_graph = pygame.transform.flip(gas_graph, False, True)
        brake_graph = self.makeCircularGraph(brake, 15, (170, 0, 0), radius)
        brake_graph = pygame.transform.rotate(brake_graph, 90)
        display.blit(brake_graph, ((display.get_width() // 2) - brake_graph.get_width(), (display.get_height() // 2) - (brake_graph.get_height() // 2)))
        display.blit(gas_graph, ((display.get_width() // 2), (display.get_height() // 2) - (gas_graph.get_height() // 2)))

        # TODO: Remove this, only keeping it to show the center of the screen.
        pygame.draw.circle(display, (255, 0, 0), display.get_rect().center, 5)