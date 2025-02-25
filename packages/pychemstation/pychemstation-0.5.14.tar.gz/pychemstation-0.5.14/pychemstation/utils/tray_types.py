from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Union


class Num(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9


class Plate(Enum):
    ONE = "1"
    TWO = "2"


class Letter(Enum):
    A = 8191
    B = 8255
    C = 8319
    D = 8383
    F = 8447


@dataclass
class FiftyFourVialPlate:
    plate: Plate
    letter: Letter
    num: Num

    def value(self) -> int:
        return self.letter.value + self.num.value


class TenVialColumn(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10


Tray = Union[FiftyFourVialPlate, TenVialColumn]