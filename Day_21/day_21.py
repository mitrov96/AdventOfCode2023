# I take no credit for this solution's second part. I would not have figured this problem out on my own.

import os
import numpy as np

# Parse input file
input = open("input_day_21.txt")
lines = input.readlines()
input.close()

# Read the input, mark down the open garden plots and the starting position
plots = set()
marked_tiles = set()
height = len(lines)
width = len(lines[0].strip())

for row in range(len(lines)):
    for column in range(len(lines[row])):
        if lines[row][column] == '.':
            plots.add((row, column))
        elif lines[row][column] == 'S':
            plots.add((row, column))
            marked_tiles.add((row, column))

# Set for each of the four moveable directions
directions = set([(0, 1), (0, -1), (1, 0), (-1, 0)])

# Goal for pt. 2, we will never actually iterate up to this goal (we shouldn't, at least)
goal = 26501365

# Alright, I needed some serious help with this problem.
# Basically, the way the input is structured with blank rows/columns for the Start,
# The growth of the number of walkable points is perfectly quadratic when compared to the size of the board (which is square).
# So we get the offset of the goal from the edge of the board, and then manually find the values for 1 and 2 boards away.
keystone_points = []
for step in range(goal):

    if step == 64:
        print("The number of walkable tiles after 64 steps is:", len(marked_tiles))

    # Keystone points are points that are in the same relative distance as the goal. We need 3 of them to solve for the quadratic
    if step % height == goal % height:
        keystone_points.append((step, len(marked_tiles)))
        if len(keystone_points) == 3:
            break

    # Explore outward, finding new tiles. Use Parallel Universe mod logic to handle open/closed positions in the infinite boards
    new_marked_tiles = set()
    for tile in marked_tiles:
        for direction in directions:
            neighbor = (tile[0] + direction[0], tile[1] + direction[1])
            parallel_neighbor = (neighbor[0] % height, neighbor[1] % width)
            if parallel_neighbor in plots:
                new_marked_tiles.add(neighbor)
    marked_tiles = new_marked_tiles

# Now the part I needed some serious help understanding (I still don't)
# Once we have 3 keystone coordinates, the way the input is structured, we can calculate a quadratic formula, and it will
# fit perfectly. Then we just plug our goal into the formula and get a result.
# Using numpy to solve a system of linear equations: ax^2 + bx + c = y for our three sets of x,y
A = np.array([[keystone_points[0][0] ** 2, keystone_points[0][0], 1],
              [keystone_points[1][0] ** 2, keystone_points[1][0], 1],
              [keystone_points[2][0] ** 2, keystone_points[2][0], 1]])
b = np.array([keystone_points[0][1], keystone_points[1][1], keystone_points[2][1]])

a, b, c = np.linalg.solve(A, b)

# Round the values to mitigate float precision loss.
print(f"The number of walkable tiles after {goal} steps is:", round((a * (goal ** 2)) + (b * goal) + c))