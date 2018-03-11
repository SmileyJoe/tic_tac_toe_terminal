from pprint import pprint
from board import Board

board = Board()
board.move(Board.PLAYER_X, 3)
board.move(Board.PLAYER_O, 4)
board.move(Board.PLAYER_O, 4)
board.move(Board.PLAYER_O, 8)
board.move(Board.PLAYER_O, 9)
board.draw()
