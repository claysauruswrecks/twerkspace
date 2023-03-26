from enum import Enum, auto


class Size(Enum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


class Element:
    def __init__(self, input_string):
        self.input_string = input_string

    def parse(self):
        raise NotImplementedError("Subclasses should implement this method")
