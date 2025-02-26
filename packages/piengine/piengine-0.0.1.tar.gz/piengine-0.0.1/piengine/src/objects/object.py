import pygame
from .game_object import GameObject
import os

"""
    Graphical object class
    Contains an image
    and its position
"""
class Nesne(GameObject):

    def __init__(self, gorsel: str, x: int = 0, y: int = 0, genislik: int = 100, yukseklik: int = 100) -> None:
        super().__init__(x, y)
        self.__img_path = gorsel
        self.__width = genislik
        self.__height = yukseklik
        if os.path.exists(self.__img_path):
            self.__img = pygame.image.load(self.__img_path)
            self.__img = pygame.transform.scale(self.__img, (genislik, yukseklik))
        else:
            self.__img = pygame.Surface((genislik, yukseklik))
            self.__img.fill((255, 0, 0))

    def ciz(self) -> None:
        screen = pygame.display.get_surface()
        screen.blit(self.__img, (self.x, self.y))

    @property
    def gorsel(self) -> str:
        return self.__img_path

    @gorsel.setter
    def gorsel(self, value: str) -> None:
        self.__img_path = value
        if os.path.exists(self.__img_path):
            self.__img = pygame.image.load(self.__img_path)
            self.__img = pygame.transform.scale(self.__img, (self.__width, self.__height))
        else:
            self.__img = pygame.Surface((self.__width, self.__height))
            self.__img.fill((255, 0, 0))
    
    @property
    def genislik(self) -> int:
        return self.__width
    
    @genislik.setter
    def genislik(self, value: int) -> None:
        self.__width = value
        self.__img = pygame.transform.scale(self.__img, (self.__width, self.__height))

    @property
    def yukseklik(self) -> int:
        return self.__height
    
    @yukseklik.setter
    def yukseklik(self, value: int) -> None:
        self.__height = value
        self.__img = pygame.transform.scale(self.__img, (self.__width, self.__height))

    def __str__(self):
        return self.__img_path

