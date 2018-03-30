# generates data to be used by the ai
#
# in short, random games are played, the moves are cycled and scores are assigned
# based on criteria, the move sets are sorted to bring the best next move to
# the top, this is then saved as a json file to be loaded in

import json

import operator

from board import Board

board = Board()
data = {}

for i in range(0, 1000000):
    # reset the board for each game
    board.reset()
    temp = []
    # play the entire game, stop when there is a winner or no more moves
    while board.is_available_move() and board.get_winner() == -1:
        # play a random move
        board.move_random()
        # add the move to the list
        temp.append(board.status)

    winner = board.get_winner()
    num_moves = len(temp) - 1
    # cycle the moves so we can process them
    for j in range(0, num_moves):
        item = temp[j]
        # we care about the next move as we want to build data on what move to make
        next_item = temp[j + 1]
        # this will be the points assigned to the next move
        score = 0

        # if there is a winner, and the next move is the last, the next move is
        # a winning move, so give it a higher score
        if winner >= 0 and j + 1 == num_moves:
            score = 10
        # if there is a winner, and the move after the next is a winning move
        # then the next move is a bad move, so give it a lower score
        elif winner >= 0 and j + 2 == num_moves:
            score = -10
        # if the player of the next move is the winner, but it is not the winning
        # move give it a low positive score as it leads to a winning path
        elif Board.get_player(next_item) == winner:
            score = 1
        # lastly we assign a low negative score as the any other move leads down a
        # loosing path
        else:
            score = -1

        # check if the move has already been played
        if item in data:
            item_data = data.get(item)

            # check if the next move has been played
            if next_item in item_data:
                next_item_data = item_data[next_item]
                average = next_item_data[0]
                total = next_item_data[1]
                count = next_item_data[2]

                total = total + score
                count = count + 1
                average = total/count

                # set the scores for the next move
                item_data[next_item] = (average, total, count)

            # if the next move hasn't been played, set the defaults
            # average = score, total = score, count = 1
            else:
                item_data[next_item] = (score, score, 1)

        # if the move hasn't been played, set it with default values
        # average = score, total = score, count = 1
        else:
            data[item] = {}
            data[item][next_item] = (score, score, 1)

# now that we have all the data we need to sort the next moves for each state
# by average score, with a higher score being a higher chance
# of winning
for item in data:
    item_data = data.get(item)

    # this changes the dict to a tuple (item_data.items()) so that it can
    # be sorted as dicts are orderless, the tuple is then in the state
    # 0: key - the state of the next move
    # 1: value - the tuple of average, total, count
    # when we use the item getter to get the value tuple and sort by it
    # it will by default take the first item in it, which is the average
    temp = sorted(item_data.items(), key=operator.itemgetter(1), reverse=True)
    data[item] = temp

# convert the sorted data to json
json_data = json.dumps(data)

# save the json string
with open("./data/data.json", "w") as json_file:
    json_file.write(json_data)
