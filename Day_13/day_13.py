
# Parse input file
input = open("input_day_13.txt")
lines = input.readlines()
input.close()


# Helper function, if given a list of numbers, returns pair of consecutive numbers
# For example, given [1, 4, 5, 6, 10] it will return [[4,5],[5,6]]
def find_consecutive_number_pairs(values):
    pairs = []
    for x in range(len(values) - 1):
        if values[x] + 1 == values[x + 1]:
            pairs.append([values[x], values[x + 1]])
    return pairs


# Primary function to find the reflection value of a given pattern
def search_for_reflection(pattern, old_value=0):
    # First we'll search for a reflection row, and track how many times we see each row
    seen_rows = {}
    for index, row in enumerate(pattern):
        if row in seen_rows:
            seen_rows[row].append(index)
        else:
            seen_rows[row] = [index]

    # If we have two identical rows that are next to each other, that might be a point of reflection, so let's find those pairs of rows
    potential_row_reflections = []
    for row in seen_rows:
        pairs = find_consecutive_number_pairs(seen_rows[row])
        for pair in pairs:
            potential_row_reflections.append(pair)

    # For each potential point of reflection, we iterate in both directions until we either find a mismatched row (fail) or the end of the pattern (success)
    for row in potential_row_reflections:
        low, high = row
        reflection = True
        while low >= 0 and high < len(pattern):
            if pattern[low] != pattern[high]:
                reflection = False
                break
            low -= 1
            high += 1
        if reflection:
            value = (row[0] + 1) * 100
            # Edge case for pt. 2: Fixing the smudge might reveal a new line of reflection without breaking the old one. We want to make sure we find the new one.
            if value != old_value:
                return value

    # Same logic for rows, but altered to handle columns instead. Too lazy to try and consolodate functionality for both cases into one.
    seen_columns = {}
    columns_by_index = {}
    for column_index in range(len(pattern[0])):
        column = ''.join([pattern[row][column_index] for row in range(len(pattern))])
        columns_by_index[column_index] = column
        if column in seen_columns:
            seen_columns[column].append(column_index)
        else:
            seen_columns[column] = [column_index]

    potential_column_reflections = []
    for column in seen_columns:
        pairs = find_consecutive_number_pairs(seen_columns[column])
        for pair in pairs:
            potential_column_reflections.append(pair)

    for column in potential_column_reflections:
        low, high = column
        reflection = True
        while low >= 0 and high < len(pattern[0]):
            if columns_by_index[low] != columns_by_index[high]:
                reflection = False
                break
            low -= 1
            high += 1
        if reflection:
            value = column[0] + 1
            if value != old_value:
                return value

    # If there's no line of reflection, return 0
    return 0


# Helper function for finding the smudge. Replaces each character with its opposite until a new line of reflection is found
def search_for_smudges(current_pattern, old_reflection_value):
    for row in range(len(current_pattern)):
        for column in range(len(current_pattern[row])):
            smudged_row = current_pattern[row][:column] + ('.' if current_pattern[row][column] == '#' else '#') + \
                          current_pattern[row][column + 1:]
            result = search_for_reflection(current_pattern[:row] + [smudged_row] + current_pattern[row + 1:],
                                           old_reflection_value)
            if result != 0 and result != old_reflection_value:
                return result


# Add a blank entry to the lines to make processing the patterns easier
lines.append(' ')

current_pattern = []
reflection_sum = 0
smudged_reflection_sum = 0

for line in lines:
    if not line.isspace():
        current_pattern.append(line.strip())
    elif current_pattern != []:
        reflection_value = search_for_reflection(current_pattern)
        reflection_sum += reflection_value
        smudged_reflection_sum += search_for_smudges(current_pattern, reflection_value)
        current_pattern = []

print("The sum of the reflection values is:", reflection_sum)
print("The sum of the un-smudged reflection values is:", smudged_reflection_sum)