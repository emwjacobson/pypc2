# from pygame.surface import Surface
import pygame


class Screen:
    # display: Surface = None
    digital_font = "screens/fonts/Digital Play St.ttf"
    basic_font = "screens/fonts/Code New Roman.otf"
    scale_x, scale_y = (1, 1)

    def __init__(self):
        super().__init__()
        # self.display = display

    def render_screen(self, display):
        # Scale is calculated compared to a 1920x1080 screen
        self.scale_x, self.scale_y = (display.get_width() / 1920, display.get_height() / 1080)

    def render_font_top_center(self, display, font, text, text_size, color, position):
        """
        This positions the font from the middle of the top edge.
        """
        font = pygame.font.Font(font, int(text_size))
        font_surface = font.render(text, True, color)
        x, y = position
        display.blit(font_surface, (x - (font_surface.get_width() / 2), y))
        return font_surface.get_size()

    def render_font_center(self, display, font, text, text_size, color, position):
        """
        This renders the font centered at `position`. This means that if `text` is
        positioned at (0,0) the left and top half will be cut off.
        """
        font = pygame.font.Font(font, int(text_size))
        font_surface = font.render(text, True, color)
        x, y = position
        display.blit(font_surface, (x - (font_surface.get_width() / 2), y - (font_surface.get_height() / 2)))
        return font_surface.get_size()

    def render_font_right(self, display, font, text, text_size, color, position):
        """
        This renders text right aligned. `position` is the top right of the text.
        """
        font = pygame.font.Font(font, int(text_size))
        font_surface = font.render(text, True, color)
        x, y = position
        display.blit(font_surface, (x - font_surface.get_width(), y))
        return font_surface.get_size()

    def render_font(self, display, font, text, text_size, color, position):
        """
        This renders text right aligned. `position` is the top left of the text,
        like normal.
        """
        font = pygame.font.Font(font, int(text_size))
        font_surface = font.render(text, True, color)
        display.blit(font_surface, position)
        return font_surface.get_size()

    def render_lines(self, display, font, position, data, color, font_size, gap, renderer):
        cur_x, cur_y = position
        max_width = 0
        max_height = 0
        for d in data:
            w, h = renderer(display, font, d, font_size, color, (cur_x, cur_y))
            if w > max_width:
                max_width = w
            if h > max_height:
                max_height = h
            cur_y += (font_size + gap)
        return (max_width, max_height)

    def condence_string(self, text, limit):
        """
        Limits `text` to `limit` characters long.
        `limit` incluses the elipses (...)
        """
        if len(text) <= limit:
            return text
        return text[0:limit-3] + "..."
    
    def makeCircularGraph(self, amnt, thickness, color, radius):
            # The `circle` surface is the full circle that rotates depending on `amnt`
        circle = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            # The `graph` surface is the half-sized surface that only shows the top half of the bar.
        graph = pygame.Surface((radius*2, radius), pygame.SRCALPHA)
        pygame.draw.circle(circle, color, (circle.get_width() // 2, circle.get_height() // 2), radius, thickness, draw_top_right=False, draw_top_left=False, draw_bottom_left=True, draw_bottom_right=True)
        circle_rot = pygame.transform.rotate(circle, -180 * amnt)
            # Maniupulates the center variable to rotate around the center
        pos = circle_rot.get_rect(center=circle.get_rect().center)
        graph.blit(circle_rot, pos)
        return graph
