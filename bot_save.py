from collections import defaultdict
from copy import deepcopy

# red, blue, green, yellow loc
# wall loc
# target loc

players = ("red", "blue", "green", "yellow")
MAP_SIZE = (16, 16)
cache = defaultdict(list)
COORD = tuple[int, int]

def calculate(player_loc: dict[str, COORD], horizontal_walls: dict[int, COORD], vertical_walls: dict[int, COORD], target_loc: COORD, target_color: str):
    boards = [player_loc]
    next_boards = []
    count_ = 1
    found = False

    while True:
        # calculate next board status
        current = boards.pop()
        # print("current:", current, "-------------------------")
        current_path = cache[frozenset(current.items())]

        # make walls from players
        player_vertical_walls = defaultdict(list)
        player_horizontal_walls = defaultdict(list)
        for player, (x, y) in current.items():
            if x > 0:
                player_vertical_walls[player].append((x - 1, y))
            if x < MAP_SIZE[0] - 1:
                player_vertical_walls[player].append((x, y))
            if y > 0:
                player_horizontal_walls[player].append((x, y - 1))
            if y < MAP_SIZE[1] - 1:
                player_horizontal_walls[player].append((x, y))

        # print("horizontal:", player_horizontal_walls)
        # print("vertical:", player_vertical_walls)        

        

        # check if in cache
        # if len(cache[frozenset(current.items())]) != 0:
        #     continue
        
        for player in players:
            # print(f"----- player : {player} -----")
            player_x, player_y = current[player]

            current_horizontal_walls = deepcopy(horizontal_walls)
            current_vertical_walls = deepcopy(vertical_walls)
            for _player, value in player_horizontal_walls.items():
                if _player != player:
                    for coord in value:
                        current_horizontal_walls[coord[0]].append(coord)

            for _player, value in player_vertical_walls.items():
                if _player != player:
                    for coord in value:
                        current_vertical_walls[coord[1]].append(coord)


            for direction, direction_char in zip([(0, 1), (0, -1), (1, 0), (-1, 0)], ["down", "up", "right", "left"]):
                # move to direction
                if direction == (0, 1):
                    # down
                    walls_in_direction = list(filter(lambda c: c[0] >= player_x, current_vertical_walls[player_y]))
                    if len(walls_in_direction) == 0:
                        move_at = (player_x, MAP_SIZE[1] - 1)
                    else:
                        end_wall = min(walls_in_direction, key=lambda c: c[0])
                        move_at = (player_x, end_wall[1])
                elif direction == (0, -1):
                    # up
                    walls_in_direction = list(filter(lambda c: c[0] < player_x, current_vertical_walls[player_y]))
                    if len(walls_in_direction) == 0:
                        move_at = (player_x, 0)
                    else:
                        end_wall = max(walls_in_direction, key=lambda c: c[0])
                        move_at = (player_x, end_wall[1] + 1)
                elif direction == (1, 0):
                    # right
                    walls_in_direction = list(filter(lambda c: c[1] >= player_y, current_horizontal_walls[player_x]))
                    if len(walls_in_direction) == 0:
                        move_at = (MAP_SIZE[0] - 1, player_y)
                    else:
                        end_wall = min(walls_in_direction, key=lambda c: c[1])
                        move_at = (end_wall[0], player_y)
                elif direction == (-1, 0):
                    # left
                    walls_in_direction = list(filter(lambda c: c[1] < player_y, current_horizontal_walls[player_x]))
                    if len(walls_in_direction) == 0:
                        move_at = (0, player_y)
                    else:
                        end_wall = max(walls_in_direction, key=lambda c: c[1])
                        move_at = (end_wall[0] + 1, player_y)
                print(walls_in_direction, end_wall)
                print(f"{direction_char}: {(player_x, player_y)} -> {move_at}")
                # print(walls_in_direction)
                # print(player, (player_x, player_y), move_at)
                # print(player, move_at)

                if move_at == (player_x, player_y):
                    continue
                next_board = deepcopy(current)
                next_board[player] = move_at
                # print("next_board:", next_board)
                if next_board == current or len(cache[frozenset(next_board.items())]) != 0 or next_board in next_boards:
                    # print("rejected:", cache[frozenset(next_board.items())])
                    continue

                next_boards.append(next_board)
                cache[frozenset(next_board.items())].append(current_path + [player + " " + direction_char])

                # found answer
                if next_board[target_color] == target_loc:
                    found = True
                    answer = cache[frozenset(next_board.items())]
                    break

            if found:
                break

        if found:
            print("length :", count_ + 1)
            # print(" -> ".join(answer))
            print(answer)
            break

        if len(boards) == 0:
            # input()
            if len(next_boards) == 0:
                print("impossible location")
                break
            boards = next_boards
            next_boards = []
            count_ += 1
            print(f"Finding path with length {count_}..")
            


if __name__ == "__main__":
    player_loc = {"red": (3, 7), "blue": (13, 7), "green": (6, 6), "yellow": (6, 4)}
    horizontal_wall_loc = [(0, 1), (0, 13), (3, 4), (3, 7), (3, 13), (5, 5), (5, 7), (5, 13), (6, 3), (6, 10), (6, 12), (7, 6), (7, 8), (8, 0), (8, 6), (8, 8), (8, 12), (10, 11), (11, 9), (12, 13), (13, 7), (14, 1), (14, 6), (15, 3), (15, 13)]
    vertical_wall_loc = [(2, 0), (2, 7), (3, 4), (3, 13), (4, 0), (4, 14), (5, 4), (5, 6), (5, 8), (5, 12), (6, 7), (6, 8), (6, 10), (8, 1), (8, 7), (8, 8), (8, 13), (9, 12), (10, 9), (10, 15), (12, 7), (12, 13), (12, 15), (13, 2), (14, 6)]
    # target_loc = (6, 12)
    target_loc = (0, 13)
    target_color = "red"

    horizontal_walls = defaultdict(list)
    for wall in horizontal_wall_loc:
        horizontal_walls[wall[0]].append(wall)
    # print("horizontal_walls", horizontal_walls)

    vertical_walls = defaultdict(list)
    for wall in vertical_wall_loc:
        vertical_walls[wall[1]].append(wall)
    # print("vertical_walls", vertical_walls)

    calculate(player_loc, horizontal_walls, vertical_walls, target_loc, target_color)