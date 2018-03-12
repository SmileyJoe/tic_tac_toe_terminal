from bit import Bit
import random


class Board:

    PLAYER_X = 0x0000
    PLAYER_O = 0x0001

    POSITION_IS_SET = Bit.POSITION_TWO

    __status = Bit()
    __bits = [Bit.ONE, Bit.TWO, Bit.THREE,
              Bit.FOUR, Bit.FIVE, Bit.SIX,
              Bit.SEVEN, Bit.EIGHT, Bit.NINE]
    __full_mask = 0x03FF
    __winning_vertical = 0x0124
    __winning_horizontal = 0x0007
    __winning_combo = [__winning_vertical,
                       __winning_vertical >> 0x0001,
                       __winning_vertical >> 0x0002,
                       __winning_horizontal,
                       __winning_horizontal << 0x0003,
                       __winning_horizontal << 0x0006,
                       0x0111,
                       0x0054]

    __board = """
    {0}   |   {1}   |   {2}   
-------------------------
    {3}   |   {4}   |   {5}   
-------------------------
    {6}   |   {7}   |   {8}   
        """

    def __init__(self):
        self.__set_player(random.randint(0, 1))

    def get_player(self):
        if self.__status.is_set(Bit.ZERO):
            return self.PLAYER_X
        else:
            return self.PLAYER_O

    def move(self, player, position):
        if position not in range(0, 9):
            return False

        bit = self.__bits[position]

        if self.__status.is_set(bit):
            return False
        else:
            if player == self.PLAYER_X:
                self.__status.set(bit)
            else:
                self.__status.unset(bit)
            self.__status.set(bit, self.POSITION_IS_SET)
            self.__set_player(player)
            return True

    def draw(self):
        positions = []
        for i in range(0, 9):
            positions.append(' ')

        self.__update_positions(positions, self.__get_player_x(), 'x')
        self.__update_positions(positions, self.__get_player_o(), 'o')
        print (self.__board.format(*positions))

    def get_winner(self):
        if self.__is_winner(self.__get_player_x()):
            return self.PLAYER_X
        elif self.__is_winner(self.__get_player_o()):
            return self.PLAYER_O
        else:
            return -1

    def __is_winner(self, player_data):
        for bit in self.__winning_combo:
            if player_data & bit == bit:
                return True

        return False

    def __get_player_x(self):
        return self.__status.get_value() & self.__get_set()

    def __get_player_o(self):
        return (self.__status.get_value() ^ self.__get_set()) & self.__full_mask

    def __get_set(self):
        return self.__status.get_value() >> self.POSITION_IS_SET

    def __update_positions(self, positions, player_data, icon):
        for i in range(0, 9):
            bit = self.__bits[i]
            if player_data & bit != 0:
                positions[i] = icon

    def __set_player(self, player):
        if player == self.PLAYER_X:
            self.__status.set(Bit.ZERO)
        else:
            self.__status.unset(Bit.ZERO)
