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

    @staticmethod
    def is_set(number, position):
        return number & position != 0

    @staticmethod
    def set(number, position, shift=0):
        if shift > 0:
            position = position << shift

        number |= position

        return number

    @staticmethod
    def unset(number, position, shift=0):
        if shift > 0:
            position = position << shift

        number &= ~position

        return number
