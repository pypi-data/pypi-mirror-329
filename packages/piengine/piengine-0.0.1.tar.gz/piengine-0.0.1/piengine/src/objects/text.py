import pygame
from .game_object import GameObject

pygame.font.init()

"""
    Text object class
    Contains a string
    and its position
"""
class Yazi(GameObject):

    def __init__(self, yazi: str = "'piengine' Oyunu", x: int = 0, y: int = 0, yazi_boyutu: int = 24) -> None:
        super().__init__(x, y)
        self.__original_text = yazi
        self.__font = pygame.font.Font(None, yazi_boyutu)
        self.__text_lines = self.__render_text(self.__original_text)

    def __render_text(self, text: str):
        lines = text.split('\n')
        rendered_lines = [self.__font.render(line, True, "white") for line in lines]
        return rendered_lines
    
    def ciz(self) -> None:
        screen = pygame.display.get_surface()
        for i, line in enumerate(self.__text_lines):
            screen.blit(line, (self.x, self.y + i * self.__font.get_linesize()))

    @property
    def yazi(self) -> str:
        return self.__original_text
    
    @yazi.setter
    def yazi(self, yeni_yazi: str) -> None:
        self.__original_text = yeni_yazi
        self.__text_lines = self.__render_text(self.__original_text)

    @property
    def font(self) -> pygame.font.Font:
        return self.__font
    
    @font.setter
    def font(self, yazi_boyutu: int) -> None:
        self.__font = pygame.font.Font(None, yazi_boyutu)
        self.__text_lines = self.__render_text(self.__original_text)
    
    @property
    def genislik(self) -> int:
        return max(line.get_width() for line in self.__text_lines)
    
    @property
    def yukseklik(self) -> int:
        return len(self.__text_lines) * self.__font.get_linesize()

    def __str__(self):
        return self.__original_text

