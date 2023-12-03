schematic = []

input_file = open("input_day_3.txt", "r")

for line in input_file:
    schematic.append(list(line.strip()))

input_file.close()

def is_part(row_index, column_index):
    for check_row in [row_index - 1, row_index, row_index + 1]:
        for check_column in [column_index - 1, column_index, column_index + 1]:
            check_row_index = min(max(0, check_row), len(schematic) - 1)
            check_column_index = min(max(0, check_column), len(schematic[check_row_index])- 1)
            character = schematic[check_row_index][check_column_index]
            if not character.isnumeric() and character != ".":
                return True

    return False


number_started = False
number_is_part = False
start_index = -1

numbers = []

for row_index, row in enumerate(schematic):
    for column_index, character in enumerate(row):
        if not character.isnumeric() or column_index == len(row) - 1:
            if number_started:
                number = ""
                for i in range(start_index, column_index):
                    number += schematic[row_index][i]
                if column_index == len(row) - 1 and character.isnumeric():
                    number += schematic[row_index][column_index]
                if number_is_part:
                    numbers.append(int(number))
                start_index = -1
                number_started = False
                number_is_part = False
        else:
            if not number_started:
                number_started = True
                start_index = column_index
            if not number_is_part:
                number_is_part = is_part(row_index, column_index)

print(sum(numbers))

# --------------- Part 2 ---------------
def adjacent_gears_search(row_index, column_index):
    adjacent_gears = []
    for check_row in [row_index - 1, row_index, row_index + 1]:
        for check_column in [column_index - 1, column_index, column_index + 1]:
            check_row_index = min(max(0, check_row), len(schematic) - 1)
            check_column_index = min(max(0, check_column), len(schematic[check_row_index])- 1)
            character = schematic[check_row_index][check_column_index]
            if character == "*":
                if (check_row_index, check_column_index) not in adjacent_gears:
                    adjacent_gears.append((check_row_index, check_column_index))

    return adjacent_gears



number_started = False
number_is_part = False
adjacent_gears = []
start_index = -1

possible_gears = {}

for row_index, row in enumerate(schematic):
    for column_index, character in enumerate(row):
        possible_gears[(row_index, column_index)] = []

for row_index, row in enumerate(schematic):
    for column_index, character in enumerate(row):
        if not character.isnumeric() or column_index == len(row) - 1:
            if number_started:
                number = ""
                for i in range(start_index, column_index):
                    number += schematic[row_index][i]
                if column_index == len(row) - 1 and character.isnumeric():
                    number += schematic[row_index][column_index]

                if number_is_part:
                    for adjacent_gear in adjacent_gears:
                         possible_gears[adjacent_gear].append(int(number))

                start_index = -1
                adjacent_gears = []
                number_started = False
                number_is_part = False
        else:
            if not number_started:
                number_started = True
                start_index = column_index
            if not number_is_part:
                number_is_part = is_part(row_index, column_index)
            adjacent_gears_to_character = adjacent_gears_search(row_index, column_index)
            for adjacent_gear in adjacent_gears_to_character:
                if adjacent_gear not in adjacent_gears:
                    adjacent_gears.append(adjacent_gear)

s = 0

for number_list in possible_gears.values():
    if len(number_list) == 2:
        s += number_list[0] * number_list[1]

print(s)