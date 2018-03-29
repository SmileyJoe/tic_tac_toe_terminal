# TIC-TAC-TOE #

Tic-tac-toe that can be played in the terminal.

## What's happening ##

This is simple tic-tac-toe that runs in the terminal, it uses only bit wise operations to handle the moves and the state of the board, this means that we can represent the board with a single int at any point.

The "ai" decides what move to play based on data build from 1 000 000 random games, because the board is represented by a single int it's possible to easily see the next best move.

### Board state ###

As mentioned the state of the board is saved as an int and bitwise operations are used to make player moves, the bits are used as follows:

From right to left

- 0: player bit, keeps track of whose turn it is.
- 1-9: board state, these represent the positions on the board, a 1 represents an `x` is in that block, a 0 represents an `o` is in that block (the mask, explained below is needed for this).
- 10-20: these are mask bits, a 1 represents the block has data, this is needed to tell what blocks have `o` in it.

### AI ###

The `data.py` script builds up a json file that the ai player uses to pick a move, a bunch of random games are played, currently 1 000 000, and a score is assigned to a move based on the following:

- The next move is a winning move, add 10 points.
- The move after the next is a winning move, subtract 10 points, we don't want the ai to play this move as it means the board has been left open for a wining move.
- The next move is played by the winning player, add 1 point as this is potentially building a path to a winning move.
- If none of the above match, subtract 1 as this is not a favorable move.

This score is then added to the cumulative score for that move from that board state and an average is calculated.

The move sets are then sorted by this average with the higher average being the higher chance of leading to a winning move/being a winning move.

## Why do this ##

There where a few personal challenges in this for me:

1. Create a tic-tac-toe game without using an array to store the game board.
2. Use python, which is currently on my learning list.
3. Handling content in the terminal, user input, rewriting the terminal etc.
4. Google as little as possible, the only things that where googled where python related, writing to the terminal, accepting user input, bitwise operators, sorting a dict etc, nothing on tic-tac-toe or building the decision tree/making an ai was googled.

## Setup ##

1. Clone the repo
2. Run `python main.py`

### Creating a new data set ###

Running `python data.py` will build a new data set for the ai, it is set to run 1 000 000 times, however, this can be changed in the file, the fewer the amount of base games the dumber the ai will be.