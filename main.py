from board import Board

board = Board()
board.move(Board.PLAYER_X, 1)
board.move(Board.PLAYER_X, 4)
board.move(Board.PLAYER_X, 7)

board.move(Board.PLAYER_O, 2)
board.draw()
