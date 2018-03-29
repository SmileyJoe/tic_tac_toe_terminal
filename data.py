import json

from board import Board

board = Board()
data = {}

for i in range(0, 1000000):
    board.reset()
    temp = []
    while board.is_available_move() and board.get_winner() == -1:
        board.move_random()
        temp.append(board.status)

    winner = board.get_winner()
    num_moves = len(temp) - 1
    for j in range(0, num_moves):
        item = temp[j]
        next_item = temp[j + 1]
        score = 0

        if winner >= 0 and j + 1 == num_moves:
            score = 10
        elif winner >= 0 and j + 2 == num_moves:
            score = -10
        elif Board.get_player(next_item) == winner:
            score = 1
        else:
            score = -1

        if item in data:
            item_data = data.get(item)

            if next_item in item_data:
                next_item_data = item_data[next_item]
                average = next_item_data[0]
                total = next_item_data[1]
                count = next_item_data[2]

                total = total + score
                count = count + 1
                average = total/count

                item_data[next_item] = (average, total, count)
            else:
                item_data[next_item] = (score, score, 1)
        else:
            data[item] = {}
            data[item][next_item] = (score, score, 1)

json_data = json.dumps(data)

with open("./data/data.json", "w") as json_file:
    json_file.write(json_data)
