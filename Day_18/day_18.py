import os

# Parse input file
input = open("input_day_18.txt")
lines = input.readlines()
input.close()

vertices = [(0,0)]
vertices2 = [(0,0)]
edge_holes = 0
edge_holes2 = 0

# Direction character to coordinate tuple map
directions = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}

# Number to direction character map (for pt. 2)
num_to_direction = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}

# Go through each instruction. Track each vertex, and the length of each edge
for line in lines:

    direction, distance, color = line.strip().split()
    distance = int(distance)
    vertices.append((vertices[-1][0] + (directions[direction][0] * distance), vertices[-1][1] + (directions[direction][1] * distance)))
    edge_holes += distance

    distance2 = int(color[2:7], 16)
    direction2 = num_to_direction[color[-2]]
    vertices2.append((vertices2[-1][0] + (directions[direction2][0] * distance2), vertices2[-1][1] + (directions[direction2][1] * distance2)))
    edge_holes2 += distance2

# Important formula #1, the Shoelace Formula. This can be used to calculate the area of the entire pit using its vertices.
# Note that this is not our answer, because we need to count the number of points contained by the polygon and its edges, not the area.
def shoelace_formula(vertices):
    v = len(vertices)
    area = 0
    for x in range(v):
        y = (x + 1) % v
        area += vertices[x][0] * vertices[y][1]
        area -= vertices[y][0] * vertices[x][1]
    return abs(area) // 2

# Important formula #2, Pick's Theorem: A = I + (B/2) - 1, where A = Area, I = Internal Points, B = Boundary Points
# The Shoelace Formula gives us A, and we counted up B in the for-loop above. So solve for I: I = A - (B/2) + 1
def picks_theorem(vertices, boundary_points):

    area = shoelace_formula(vertices)
    interior_points = area - (boundary_points // 2) + 1

    # Now that we know I and B, we know how many points are contained. Add 'em up.
    return interior_points + boundary_points

print("The lagoon can hold the following cubic meters of lava:", picks_theorem(vertices, edge_holes))
print("The larger lagoon can hold the following cubic meters of lava:", picks_theorem(vertices2, edge_holes2))