from bit import Bit
import random


class Board:

    PLAYER_X = 0x0000
    PLAYER_O = 0x0001

    __player_bit = Bit.ONE
    __position_set = Bit.POSITION_TWO
    __status = 0x0000
    __bits = [Bit.TWO, Bit.THREE, Bit.FOUR,
              Bit.FIVE, Bit.SIX, Bit.SEVEN,
              Bit.EIGHT, Bit.NINE, Bit.TEN]
    __full_mask = 0x03FF
    __full_mask_board = 0x03FE
    __winning_vertical = 0x0248
    __winning_horizontal = 0x000E
    __winning_combo = [__winning_vertical,
                       __winning_vertical >> 0x0001,
                       __winning_vertical >> 0x0002,
                       __winning_horizontal,
                       __winning_horizontal << 0x0003,
                       __winning_horizontal << 0x0006,
                       0x0222,
                       0x00A8]

    __board = """    {0}   |   {1}   |   {2}   
-------------------------
    {3}   |   {4}   |   {5}   
-------------------------
    {6}   |   {7}   |   {8}   
"""

    def __init__(self):
        self.__set_player(random.randint(0, 1))

    def get_current_player(self):
        if Bit.is_set(self.__status, self.__player_bit):
            return self.PLAYER_X
        else:
            return self.PLAYER_O

    def next_move(self, position):
        return self.move(self.get_current_player(), position)

    def move(self, player, position):
        if position not in range(0, 9):
            return False

        bit = self.__bits[position]

        if Bit.is_set(self.__get_set(), bit):
            return False
        else:
            if player == self.PLAYER_X:
                self.__status = Bit.set(self.__status, bit)
            else:
                self.__status = Bit.unset(self.__status, bit)

            self.__status = Bit.set(self.__status, bit, self.__position_set)
            self.__status = self.__status ^ 0x0001
            return True

    def get_board(self):
        positions = []
        for i in range(0, 9):
            positions.append(' ')

        self.__update_positions(positions, self.__get_player_x(), 'x')
        self.__update_positions(positions, self.__get_player_o(), 'o')
        return self.__board.format(*positions)

    def get_winner(self):
        if self.__is_winner(self.__get_player_x()):
            return self.PLAYER_X
        elif self.__is_winner(self.__get_player_o()):
            return self.PLAYER_O
        else:
            return -1

    def is_available_move(self):
        return self.__get_set() & self.__full_mask_board != self.__full_mask_board

    def __is_winner(self, player_data):
        for bit in self.__winning_combo:
            if player_data & bit == bit:
                return True

        return False

    def __get_player_x(self):
        return self.__status & self.__get_set()

    def __get_player_o(self):
        return (self.__status ^ self.__get_set()) & self.__full_mask

    def __get_set(self):
        return self.__status >> self.__position_set

    def __update_positions(self, positions, player_data, icon):
        for i in range(0, 9):
            bit = self.__bits[i]
            if Bit.is_set(player_data, bit):
                positions[i] = icon

    def __set_player(self, player):
        if player == self.PLAYER_X:
            self.__status = Bit.set(self.__status, self.__player_bit)
        else:
            self.__status = Bit.unset(self.__status, self.__player_bit)

    def __log(self, data):
        print("{0:b}".format(data))
