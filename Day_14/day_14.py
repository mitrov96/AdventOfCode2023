import os

# Parse input file
input = open("input_day_14.txt")
lines = input.readlines()
input.close()
height = len(lines)
width = len(lines[0]) - 1

# Read the input. Grab the coordinates of any blocked cell (sphere or cubed rocks) and also track the rock coordinates specifically
blocked = set()
rocks = set()
for row in range(len(lines)):
    for column in range(len(lines[row].strip())):
        if lines[row][column] != '.':
            blocked.add((row, column))
        if lines[row][column] == 'O':
            rocks.add((row, column))


# Tilt will move the rocks in the given direction
def tilt(rocks, direction):
    global height, width, blocked
    rocks_after_move = set()

    # Depending on the direction, the rocks will be sorted differently for movement. (Top ones move first if rolling north, for example)
    if direction == 'N':
        rocks.sort()
    elif direction == 'S':
        rocks.sort(reverse=True)
    elif direction == 'W':
        rocks.sort(key=lambda x: x[1])
    else:
        rocks.sort(key=lambda x: x[1], reverse=True)

    # Track each rock's starting position
    for rock in rocks:
        rock_row, rock_col = rock
        new_rock_row, new_rock_col = rock_row, rock_col

        # Try to move the rock in the given direction until it hits something
        if direction == 'N':
            while new_rock_row > 0:
                if (new_rock_row - 1, rock_col) not in blocked:
                    new_rock_row -= 1
                else:
                    break
        if direction == 'S':
            while new_rock_row < height - 1:
                if (new_rock_row + 1, rock_col) not in blocked:
                    new_rock_row += 1
                else:
                    break
        if direction == 'W':
            while new_rock_col > 0:
                if (rock_row, new_rock_col - 1) not in blocked:
                    new_rock_col -= 1
                else:
                    break
        if direction == 'E':
            while new_rock_col < width - 1:
                if (rock_row, new_rock_col + 1) not in blocked:
                    new_rock_col += 1
                else:
                    break

        # Unblock the rock's original position and block the rock's new position
        blocked.remove((rock_row, rock_col))
        blocked.add((new_rock_row, new_rock_col))
        rocks_after_move.add((new_rock_row, new_rock_col))

    return rocks_after_move


# We are looking at the state of the rocks after each cycle, and trying to detect when it starts cycling
seen_end_states = {}
cycles = 0
cycle_tracker = 0
cycle_length = None

# Go until we've found the same state occurring over 5 times (hard-coded value I chose)
while cycle_tracker <= 5:
    end = False
    for direction in 'NWSE':
        rocks = tilt(list(rocks), direction)
        # Answer for pt. 1
        if direction == 'N' and cycles == 0:
            weight = 0
            for rock in rocks:
                weight += (height - rock[0])
            print("The load on the north support beam is after tilting to the north is:", weight)
    cycles += 1

    # Check if we've seen this state before, and if we have, have we seen it over 5 times yet?
    rock_tuple = tuple(rocks)
    if rock_tuple not in seen_end_states:
        seen_end_states[rock_tuple] = [cycles]
    else:
        seen_end_states[rock_tuple].append(cycles)
        cycle_tracker = max(cycle_tracker, len(seen_end_states[rock_tuple]))
        # Calculate the length of the cycle, so we know the pattern in which these states occur
        if cycle_tracker > 5:
            cycle_length = seen_end_states[rock_tuple][-1] - seen_end_states[rock_tuple][-2]
            end = True
            break
    if end:
        break

for state in seen_end_states:
    # The state after 1 billion cycles will be the one with the same remainder as 1 billion when divided by the cycle length
    # We only want to check states in the cycle, so only ones that we saw at least 5 times
    if len(seen_end_states[state]) >= 5 and seen_end_states[state][-1] % cycle_length == 1000000000 % cycle_length:
        weight = 0
        for rock in state:
            weight += (height - rock[0])
        print("The load on the north support beam after 1 billion tilt cycles is:", weight)