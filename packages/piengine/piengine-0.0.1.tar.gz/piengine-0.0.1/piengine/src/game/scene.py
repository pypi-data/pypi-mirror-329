from ..base import Drawable, Updateable
from ..objects import GameObject
from ..events import KlavyeOlayi, FareOlayi, EventHandler

"""
    Sahne sınıfı, oyunun içindeki objeleri tutar ve bunları günceller ve çizer.
"""
class Sahne(EventHandler, Drawable, Updateable):
    def __init__(self, isim: str = 'normal sahne', oyun_objeleri: GameObject = []) -> None:
        self.__isim = isim
        self.__game_objects: list[GameObject] = oyun_objeleri

    def guncelle(self, dt: float) -> None:
        for obje in self.__game_objects:
            obje.guncelle(dt)

    def ciz(self) -> None:
        for obje in self.__game_objects:
            obje.ciz()

    def klavye_olayi(self, olay: KlavyeOlayi) -> None:
        for obje in self.__game_objects:
            obje.klavye_olayi(olay)

    def fare_olayi(self, olay: FareOlayi) -> None:
        for obje in self.__game_objects:
            obje.fare_olayi(olay)

    def ekle(self, nesne: GameObject) -> None:
        self.__game_objects.append(nesne)

    @property
    def objeler(self) -> list[GameObject]:
        return self.__game_objects

    @property
    def isim(self) -> str:
        return self.__isim

    @isim.setter
    def isim(self, value: str) -> None:
        self.__isim = value

    def __iter__(self):
        return iter(self.__game_objects)

    def __str__(self):
        return self.__isim

