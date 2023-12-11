import os

# Parse input file
input = open("input_day_11.txt")
lines = input.readlines()
input.close()

# Calculate the height and width, and create a list for tracking the locations of all the galaxies
height = len(lines)
width = len(lines[0]) - 1
galaxies = []

# Find all of the galaxies, and track with rows and columns don't have any galaxies in them
columns_without_galaxies = set(range(0, width))
rows_without_galaxies = set(range(0, height))
for row in range(height):
    if '#' in lines[row]:
        rows_without_galaxies.remove(row)
        for column in range(width):
            if lines[row][column] == '#':
                columns_without_galaxies.discard(column)
                galaxies.append((row, column))


# Function for calculating the manhattan (shortest) distance between two galaxies in the map
def manhattan_distance(galaxy1, galaxy2, columns_without_galaxies, rows_without_galaxies):
    raw = abs((galaxy1[0] - galaxy2[0])) + abs((galaxy1[1] - galaxy2[1]))

    # Count how many empty rows / columns the path crosses
    spanned_rows = set(range(min(galaxy1[0], galaxy2[0]), max(galaxy1[0], galaxy2[0])))
    spanned_columns = set(range(min(galaxy1[1], galaxy2[1]), max(galaxy1[1], galaxy2[1])))
    empty_lines_crossed = len(spanned_rows.intersection(rows_without_galaxies)) + len(
        spanned_columns.intersection(columns_without_galaxies))

    # For pt. 1, each empty line adds one to the distance. For pt. 2, each empty line adds 999,999 more lines (to make it one million in total)
    return raw + empty_lines_crossed, raw + (empty_lines_crossed * 999999)


# Go through every pair of galaxies and find the paths. Don't double-calculate (A -> B and then do B -> A)
distances = 0
distances2 = 0
for x in range(len(galaxies)):
    for y in range(x + 1, len(galaxies)):
        distance1, distance2 = manhattan_distance(galaxies[x], galaxies[y], columns_without_galaxies,
                                                  rows_without_galaxies)
        distances += distance1
        distances2 += distance2

print("The sum of the shortest paths between all pairs of galaxies, where empty lines count as 2 units is:", distances)
print("The sum of the shortest paths between all pairs of galaxies, where empty lines count as 1,000,000 units is:",
      distances2)