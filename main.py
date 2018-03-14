from board import Board
import curses

screen = curses.initscr()
curses.cbreak()

try:
    board = Board()

    while board.get_winner() == -1 and board.is_available_move():
        screen.erase()
        player = board.get_current_player()

        screen.addstr(board.get_board())

        if player == Board.PLAYER_X:
            play_message = "Player X move: "
        else:
            play_message = "Player O move: "

        screen.addstr(play_message)

        valid = False
        while not valid:
            move = int(screen.getstr(5, len(play_message), 1))

            if move in range(1, 10):
                move = move - 1
                valid = board.next_move(move)

                if not valid:
                    screen.addstr("That move is not allowed, please try again.")
            else:
                screen.addstr("Please choose a number between 1 and 9.")

    screen.erase()
    screen.addstr(board.get_board())
    if board.get_winner() == -1:
        screen.addstr("It's a draw")
    elif board.get_winner() == Board.PLAYER_X:
        screen.addstr("Winner is player X")
    else:
        screen.addstr("Winner is player O")

    text_exit = "Press enter to exit."
    screen.addstr("\n" + text_exit)
    screen.refresh()
    screen.getstr(6, len(text_exit), 0)

finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()
