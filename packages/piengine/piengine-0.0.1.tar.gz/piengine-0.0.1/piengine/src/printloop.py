import pygame
import math
from .objects import Yazi

# Gradient colors
color1 = [45, 78, 181] # #2d4eb5
color2 = [68, 6, 144]  # #440690
gradient = True
window_margin = 20


def _setup(print_objs: list[Yazi]):
    pygame.init()
    # Get the maximum width of the texts
    _text_max_width = 0
    for obj in print_objs:
        _text_max_width = max(_text_max_width, obj.genislik)
    
    # Get the total height of the texts
    _total_text_height = max((len(print_objs) - 1), 0)
    x = window_margin
    y = window_margin
    for obj in print_objs:
        _total_text_height += obj.yukseklik
        obj.x = x
        obj.y = y
        y += obj.yukseklik

    # Set the display size
    sizes = (_text_max_width + window_margin * 2, _total_text_height + window_margin * 2)
    main_display = pygame.display.set_mode(sizes)

    pygame.display.set_caption("PiEngine")

    return main_display


def start(print_objs: list[Yazi]):
    screen = _setup(print_objs)
    clock = pygame.time.Clock()
    running = True
    dt = 0
    t = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ===== Gradient Background ===== #
        gradient_surface = pygame.Surface(screen.get_size())
        _draw_diagonal_gradient(gradient_surface, color1, color2, t)
        screen.blit(gradient_surface, (0, 0))

        # ===== Write Texts ===== #
        for obj in print_objs:
            obj.guncelle(dt)
            obj.ciz()

        # ===== Display ===== #
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        t += dt

    pygame.quit()


def _draw_diagonal_gradient(surface, color1, color2, t):
    c1 = (
        max(min(int(color1[0] * (math.sin(t) * 0.1 + 1)), 255), 0),
        max(min(int(color1[1] * (math.sin(t) * 0.1 + 1)), 255), 0),
        max(min(int(color1[2] * (math.sin(t) * 0.1 + 1)), 255), 0)
        )
    c2 = (
        max(min(int(color2[0] * (math.sin(t) * 0.1 + 1)), 255), 0),
        max(min(int(color2[1] * (math.sin(t) * 0.1 + 1)), 255), 0),
        max(min(int(color2[2] * (math.sin(t) * 0.1 + 1)), 255), 0)
        )

    width, height = surface.get_size()

    for y in range(height):
        for x in range(width):
            ratio = (x + y) / (width + height)
            r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
            g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
            b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
            surface.set_at((x, y), (r, g, b))

