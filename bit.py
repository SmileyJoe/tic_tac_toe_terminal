# handles a lot of the bit shifting with static methods
class Bit:

    # position bits
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
    TEN = 0x0200

    POSITION_TWO = 0x000A

    """
    checks if a bit is set on the number
    
    :param number: the number to check against
    :param position: the bit position to check against
    :returns: boolean, true if the bit is set, false otherwise
    """
    @staticmethod
    def is_set(number, position):
        # to see if the bit is set, we and it with the number, if the
        # bit is not set 0 is returned as all checks will be 1 & 0 or 0 & 1
        return number & position != 0

    """
    sets a bit on a given number
    
    :param number: the number to set the bit on
    :param position: the position to set
    :param shift: whether to shift the position or not, this is used for storing
                    more then one set of data in a number
    :returns: the new number
    """
    @staticmethod
    def set(number, position, shift=0):
        # shift the position if needed
        if shift > 0:
            position = position << shift

        # we or the position bit on the number, by using or all the other bits
        # are left untouched
        number |= position

        return number

    """
    unset the bit from the number
    
    :param number: the number to unset the bit from
    :param position: the bit to unset
    :param shift: whether to shift the position or not, see set for more details
    :returns: the new number
    """
    @staticmethod
    def unset(number, position, shift=0):
        # shift the position if needed
        if shift > 0:
            position = position << shift

        # we and the negation of the position onto the number, this will
        # leave every bit the same with a 1 & 0 or 1 & 1 check, except the
        # position bit with a 0 & 1 or a 0 & 0 check
        number &= ~position

        return number
