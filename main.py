from board import Board

board = Board()
print(board.get_board())

while board.get_winner() == -1 and board.is_available_move():
    player = board.get_current_player()

    if player == Board.PLAYER_X:
        play_message = "Player X move: "
    else:
        play_message = "Player O move: "

    valid = False
    while not valid:
        move = int(input(play_message))

        if move in range(1, 10):
            move = move - 1
            valid = board.next_move(move)

            if not valid:
                print("That move is not allowed, please try again.")
        else:
            print("Please choose a number between 1 and 9.")

    print(board.get_board())

if board.get_winner() == -1:
    print("It's a draw")
elif board.get_winner() == Board.PLAYER_X:
    print("Winner is player X")
else:
    print("Winner is player O")
