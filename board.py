from bit import Bit
import random


class Board:

    PLAYER_X = 0
    PLAYER_O = 1

    __status = Bit()
    __bits = [Bit.ONE, Bit.TWO, Bit.THREE,
              Bit.FOUR, Bit.FIVE, Bit.SIX,
              Bit.SEVEN, Bit.EIGHT, Bit.NINE]
    __player_x = Bit()
    __player_o = Bit()

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
                self.__player_x.set(bit)
            else:
                self.__player_o.set(bit)
            self.__status.set(bit)
            self.__set_player(player)
            return True

    def draw(self):
        positions = []
        for i in range(0, 9):
            positions.append(' ')

        self.__update_positions(positions, self.__player_x, 'x')
        self.__update_positions(positions, self.__player_o, 'o')
        print (self.__board.format(*positions))

    def __update_positions(self, positions, player_data, icon):
        for i in range(0, 9):
            bit = self.__bits[i]
            if player_data.is_set(bit):
                positions[i] = icon

    def __set_player(self, player):
        if player == self.PLAYER_X:
            self.__status.set(Bit.ZERO)
        else:
            self.__status.unset(Bit.ZERO)
