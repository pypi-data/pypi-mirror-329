from ..objects import Yazi

print_objs: list[Yazi] = []

def game_print(*args: object, sep: str = ' ', end: str = '', **kwargs: object) -> None:
    """
        Print function for the game
        Adds the printed objects to the print_objs list
    """
    if kwargs.get('c', False):
        oprint(*args, sep=sep, end=end) # type: ignore
        return

    obj: str = (sep.join([str(o) for o in args]) + (end if end else '\n')).replace('\t', ' '*4)
    print_objs.append(Yazi(yazi=obj))

