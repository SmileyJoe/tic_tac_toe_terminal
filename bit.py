from pprint import pprint


class Bit:

    ZERO = 0x0000
    ONE = 0x0001
    TWO = 0x0002
    THREE = 0x0004
    FOUR = 0x0008
    FIVE = 0x0010
    SIX = 0x0020
    SEVEN = 0x0040
    EIGHT = 0x0080
    NINE = 0x0100

    POSITION_TWO = 0x000A

    __value = 0

    def __init__(self):
        self.__value = self.ZERO

    def set(self, position, shift=0):
        if shift > 0:
            position = position << shift

        self.__value |= position

    def unset(self, position, shift=0):
        if shift > 0:
            position = position << shift

        self.__value &= ~position

    def is_set(self, position):
        return self.__value & position != 0

    def log(self):
        pprint("{0:b}".format(self.__value))

    def __str__(self):
        return "{0:b}".format(self.__value)

    def get_value(self):
        return self.__value
