from ..base import Drawable, Updateable
from ..events import KlavyeOlayi, FareOlayi, EventHandler

"""
    Base class for all game objects
    Includes basic properties and methods
"""
class GameObject(EventHandler, Drawable, Updateable):

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x
    
    @x.setter
    def x(self, value: int) -> None:
        self.__x = value
    
    @property
    def y(self) -> int:
        return self.__y
    
    @y.setter
    def y(self, value: int) -> None:
        self.__y = value
    
    def __str__(self) -> str:
        return f"({self.__x}, {self.__y})"

