import pygame
from .game import Oyun


def _setup(oyun: Oyun):
    pygame.init()
    
    sizes = (oyun.genislik, oyun.yukseklik)
    main_display = pygame.display.set_mode(sizes)

    pygame.display.set_caption(oyun.baslik)

    return main_display


def start(oyun: Oyun):
    screen = _setup(oyun)
    clock = pygame.time.Clock()
    running = True
    dt = 0
    t = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ===== Background ===== #
        screen.fill(oyun.arka_plan_rengi)

        # ===== Update Scene ===== #
        oyun.guncelle(dt)
        oyun.ciz()

        # ===== Display ===== #
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        t += dt

    pygame.quit()

