from board import Board

board = Board()
board.move(Board.PLAYER_X, 2)
board.move(Board.PLAYER_X, 4)
board.move(Board.PLAYER_X, 6)

board.move(Board.PLAYER_O, 0)
board.move(Board.PLAYER_O, 3)
board.move(Board.PLAYER_O, 5)
board.draw()

print(board.get_winner())
