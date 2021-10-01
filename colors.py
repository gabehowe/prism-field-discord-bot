import enum

import colorama
from colorama import Fore, Style


class Color(enum.Enum):
    WHITE = Fore.WHITE
    BLUE = Fore.BLUE
    GREEN = Fore.GREEN
    WARNING = Fore.YELLOW
    RED = Fore.RED
    ENDCOLOR = Style.RESET_ALL


def printc(color: Color, string: str):
    colorama.init()
    print(color.value + string + Style.RESET_ALL)
