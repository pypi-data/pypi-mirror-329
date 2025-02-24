"""Color(Enum) class and built in methods for formatting"""
# For dict/r.json type hinting
from typing import Type, TypeVar

# Enum type for colors
from enum import Enum


class Color(Enum):
    """Color Enum class we can use to instead of literals. Includes a format method.

    Constants:
        GREEN
        ORANGE
        ORANGE_TOO
        RED

    Methods:
        __str__(self) -> str
        format_color(cls, string: str, color: Type[COLORT] = None) ->str
    """

    GREEN = "0"
    ORANGE, ORANGE_TOO = "1", "2"
    RED = "3"

    def __str__(self):
        return self.value

    COLORT = TypeVar("ColorT", bound="Color")

    @classmethod
    def format_color(cls, string: str, color: Type[COLORT] = None) -> str:
        """Give each pollen value an appropriate color in the table

        Input Arguments: `string` to colorise, and `Color` as defined in the parent class
        Returns: `string` with additional ASCII color codes.
        """
        green = "\033[92m"
        orange = "\033[93m"
        red = "\033[91m"
        endc = "\033[0m"

        if color == cls.GREEN:
            return green + string + endc
        if color in (cls.ORANGE, cls.ORANGE_TOO):
            return orange + string + endc
        if color == cls.RED:
            return red + string + endc
        return string
