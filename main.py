from board import Board

board = Board()
board.next_move(0)
board.next_move(1)
board.next_move(3)
board.next_move(6)
board.next_move(5)
board.next_move(7)
board.next_move(2)
board.next_move(8)
board.draw()

print(board.get_winner())
