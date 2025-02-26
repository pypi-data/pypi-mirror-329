
from .src.game import (
    Oyun,
    Sahne
    )

from .src.objects import (
    GameObject,
    Yazi,
    Nesne
    )

from .src.events import (
    FareOlayi,
    KlavyeOlayi
    )

from .src.print import (
    game_print,
    print_objs
    )


def baslat(oyun: Oyun = None):
    if len(print_objs) > 0:
        from .src.printloop import start
        start(print_objs)
    
    if oyun:
        from .src.mainloop import start
        start(oyun)


# Bind print to game_print
import builtins
builtins.oprint = print
oprint = print
builtins.print = game_print
print = game_print
