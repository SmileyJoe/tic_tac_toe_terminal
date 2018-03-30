import json

from bit import Bit
import random


# handles the board state and the game logic
class Board:

    # player constants
    PLAYER_X = 0x0000
    PLAYER_O = 0x0001

    # data for the ai
    __data = None
    # position of the player bit in the status
    __player_bit = Bit.ONE
    # position of the start of the set mask in the status
    __position_set = Bit.POSITION_TWO
    # current state of the game
    _status = 0x0000
    # array of bits that represent the positions of the board
    __bits = [Bit.TWO, Bit.THREE, Bit.FOUR,
              Bit.FIVE, Bit.SIX, Bit.SEVEN,
              Bit.EIGHT, Bit.NINE, Bit.TEN]
    __full_mask = 0x03FF
    # used to check if any moves are available
    __full_mask_board = 0x03FE
    # state of the board for a single vertical win
    __winning_vertical = 0x0248
    # state of the board for a single horizontal win
    __winning_horizontal = 0x000E
    # all the winning states for the board, we shift the vertical and horizontal
    # states to cover all 3 possibilities
    __winning_combo = [__winning_vertical,
                       __winning_vertical >> 0x0001,
                       __winning_vertical >> 0x0002,
                       __winning_horizontal,
                       __winning_horizontal << 0x0003,
                       __winning_horizontal << 0x0006,
                       0x0222,
                       0x00A8]
    # what player the ai player is, x or o
    _ai_player = -1
    # format of the board
    __board = """    {0}   |   {1}   |   {2}   
-------------------------
    {3}   |   {4}   |   {5}   
-------------------------
    {6}   |   {7}   |   {8}   
"""

    """
    initiate the class
    """
    def __init__(self):
        # load the ai data
        with open('./data/data.json') as json_data:
            self.__data = json.load(json_data)
        # set the starting player at random
        self.__set_player(random.randint(0, 1))

    """
    get the current player based on the status
    
    :returns: the constant of the current player
    """
    def get_current_player(self):
        return self.get_player(self._status)

    """
    get the player based on the player bit
    
    :param data: the number to check the player bit on
    :returns: the constant representing a player, x or o
    """
    @staticmethod
    def get_player(data):
        # if the player bit is set then the current player is x, else it is o
        if Bit.is_set(data, Board.__player_bit):
            return Board.PLAYER_X
        else:
            return Board.PLAYER_O

    """
    play the next move
    
    :param position: the position of the next move
    :returns: boolean, true if the move was allowed, false otherwise
    """
    def next_move(self, position):
        return self.move(self.get_current_player(), position)

    """
    play the ai move
    
    :returns: boolean, true if the move was allowed, false otherwise
    """
    def ai_move(self):
        temp = str(self.status)

        # check if the status is in the data set
        if temp in self.__data:
            move_set = self.__data.get(temp)
            # get the status of the board that is the most favorable move
            next_status = int(move_set[0][0])
            # get the difference between the boards, this will be the next move to play
            next_move = (self.status & self.__full_mask_board) ^ (next_status & self.__full_mask_board)
            # play the next move
            return self.next_move(self.__bits.index(next_move))

        # play a random move if we have no data for this status
        else:
            return self.move_random()

    """
    play a random move
    
    :returns: boolean, true if the move was allowed, false otherwise
    """
    def move_random(self):
        if self.is_available_move():
            # keep trying until a valid move is made
            while not self.next_move(random.randint(0, 9)):
                # this is just here because something needs to be in the while
                found = True
            return True
        else:
            return False

    """
    make a move on the board
    
    :param player: the constant for the player who is making the move
    :param position: the position the player is making their move
    :returns: boolean, true if the move was allowed, false otherwise
    """
    def move(self, player, position):
        # check if the move is on the board
        if position not in range(0, 9):
            return False

        # get the bit for the move
        bit = self.__bits[position]

        # make sure the spot is available
        if Bit.is_set(self.__get_set(), bit):
            return False
        else:
            # player x is stored as 1, o as 0, so set or unset the bit accordingly
            if player == self.PLAYER_X:
                self._status = Bit.set(self._status, bit)
            else:
                self._status = Bit.unset(self._status, bit)

            # set the set bit by shifting the position and setting it
            self._status = Bit.set(self._status, bit, self.__position_set)
            # change the player
            self._status = self._status ^ 0x0001
            return True

    """
    get the current populated board
    
    :returns: the current populated board
    """
    def get_board(self):
        # create an empty list of the total number of blocks
        positions = []
        for i in range(0, 9):
            positions.append(' ')

        # add a symbol to the list where the player has played
        self.__update_positions(positions, self.__get_player_x(), 'x')
        self.__update_positions(positions, self.__get_player_o(), 'o')
        # format the board constant with the player symbols or blanks
        return self.__board.format(*positions)

    """
    get the winner if there is one
    
    :returns: the player constant that is the winner, -1 if there is no winner
    """
    def get_winner(self):
        if self.is_winner(self.__get_player_x()):
            return self.PLAYER_X
        elif self.is_winner(self.__get_player_o()):
            return self.PLAYER_O
        else:
            return -1

    """
    checks if there are any moves available
    
    :returns: true if there are, false otherwise
    """
    def is_available_move(self):
        # and the full board mask onto the set, if the result is the full mask
        # it means the set is full of 1's and so no moves are available
        return self.__get_set() & self.__full_mask_board != self.__full_mask_board

    """
    checks if the current player is the ai player
    
    :returns: true if it is, false otherwise
    """
    def is_ai_player(self):
        return self.get_current_player() == self.ai_player

    """
    reset the board to its starting position with a new random player
    """
    def reset(self):
        self._status = 0x0000
        self.__set_player(random.randint(0, 1))

    """
    gets the current status of the board
    
    :returns: the current status
    """
    @property
    def status(self):
        return self._status

    """
    gets the ai player
    
    :returns: constant for the ai player, x or o
    """
    @property
    def ai_player(self):
        return self._ai_player

    """
    sets the si player
    
    :param value: constant for the player that will be controlled by the ai
    """
    @ai_player.setter
    def ai_player(self, value):
        self._ai_player = value

    """
    checks if any winning combos are in the data
    
    :params player_data: the move set of the player
    :returns: true if the player has winning combos, false otherwise
    """
    @staticmethod
    def is_winner(player_data):
        for bit in Board.__winning_combo:
            if player_data & bit == bit:
                return True

        return False

    """
    get the moves the x player has made
    
    :returns: int of the players moves
    """
    def __get_player_x(self):
        return self._status & self.__get_set()

    """
    get the moves the o player has made
    
    :returns: int of the players moves
    """
    def __get_player_o(self):
        # we need to take the mask into account for this one as
        # an empty space and an o move are represented by 0's
        return (self._status ^ self.__get_set()) & self.__full_mask

    """
    get the bits that represent what positions are set
    
    :returns: int with the set positions
    """
    def __get_set(self):
        return self._status >> self.__position_set

    """
    adds the icon to the positions list if the player has made
    a move there
    
    :param positions: the list of all the moves
    :param player_data: the move set of the player to add
    :param icon: the character to display for the player
    """
    def __update_positions(self, positions, player_data, icon):
        for i in range(0, 9):
            bit = self.__bits[i]
            if Bit.is_set(player_data, bit):
                positions[i] = icon

    """
    sets the player
    
    :param player: the constant for the player to set
    """
    def __set_player(self, player):
        if player == self.PLAYER_X:
            self._status = Bit.set(self._status, self.__player_bit)
        else:
            self._status = Bit.unset(self._status, self.__player_bit)

    """
    logs the bits of an integer
    """
    def __log(self, data):
        print("{0:b}".format(data))
