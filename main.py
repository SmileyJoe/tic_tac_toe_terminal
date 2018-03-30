from board import Board
import curses

# initiate the curses lib so that we can work with the text on the screen properly
screen = curses.initscr()
curses.cbreak()

# everything is wrapped in a try so that we can reset the state of the terminal
# if the script crashes for any reason
try:
    screen.erase()
    # get the player count
    player_message = "How many players (1/2)? "
    screen.addstr(player_message)
    valid = False

    # keep asking until we get valid input
    while not valid:
        try:
            player_count = int(screen.getstr(0, len(player_message), 1))

            if player_count in range(1, 3):
                valid = True
            else:
                screen.addstr("Please enter either 1 or 2.")
        except ValueError:
            screen.addstr("Please enter either 1 or 2.")

    board = Board()

    # set the ai player if needed
    if player_count == 1:
        board.ai_player = Board.PLAYER_X

    screen.erase()
    # continue while there is no winner and there are moves available
    while board.get_winner() == -1 and board.is_available_move():
        # clear the screen on every turn so the new board can be drawn
        screen.erase()

        # play the ai turn
        if board.is_ai_player():
            board.ai_move()
        # play the users turn
        else:
            player = board.get_current_player()

            # add the board to the screen
            screen.addstr(board.get_board())

            if player == Board.PLAYER_X:
                play_message = "Player X move: "
            else:
                play_message = "Player O move: "

            # add the instructions to the screen
            screen.addstr(play_message)

            valid = False
            # continue asking until a valid move is entered from the player
            while not valid:
                try:
                    # get the users move
                    move = int(screen.getstr(5, len(play_message), 1))

                    # check if its a valid move
                    if move in range(1, 10):
                        # we subtract 1 as internally we use 0 as a base
                        move = move - 1
                        valid = board.next_move(move)

                        # if the move is not valid display an error, this will be if
                        # the spot is already played on
                        if not valid:
                            screen.addstr("That move is not allowed, please try again.")

                    # if the move isn't valid display an error
                    else:
                        screen.addstr("Please choose a number between 1 and 9.")

                # if anything other then a number is entered display an error
                except ValueError:
                    screen.addstr("Please enter a number.")

    # when the game is finished, erase the screen again so we can show winning results
    screen.erase()
    # add the completed board to the screen
    screen.addstr(board.get_board())
    # get the winning text to display
    if board.get_winner() == -1:
        screen.addstr("It's a draw")
    elif board.get_winner() == Board.PLAYER_X:
        screen.addstr("Winner is player X")
    else:
        screen.addstr("Winner is player O")

    # show instructions to end the game
    text_exit = "Press enter to exit."
    screen.addstr("\n" + text_exit)
    screen.refresh()
    screen.getstr(6, len(text_exit), 0)

# no matter what happens we need to end the curses library
# so that the terminal goes back to its normal state
finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()
