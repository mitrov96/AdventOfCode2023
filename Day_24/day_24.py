import os
from z3 import *

# Parse input file
input = open("input_day_24.txt")
lines = input.readlines()
input.close()

# Parse the input to get the points as a dictionary. {(position): (velocity)}
points = {}
for line in lines:
    point, slope = line.strip().split(' @ ')
    point = point.split(', ')
    slope = slope.split(', ')
    points[tuple([int(p) for p in point])] = tuple([int(s) for s in slope])


# Helper function: given the line formula of y = mx + b, let's find m and b from x,y and velocity (which can be translated to 'm')
def get_line_equation(position, velocity):
    m = velocity[1] / velocity[0]
    b = position[1] - (m * position[0])
    return m, b


# Helper function for determining if a point lies on a ray
def is_on_ray(p, start, direction):
    point_directions = [p[dimension] - start[dimension] for dimension in range(2)]
    return all([(point_directions[dimension] > 0) == (direction[dimension] > 0) for dimension in range(2)])


# Given two rays, calculate their point of intersection (if there is one)
def calculate_intersection(ray1_position, ray1_velocity, ray2_position, ray2_velocity):
    # Get the line equations
    m1, b1 = get_line_equation(ray1_position, ray1_velocity)
    m2, b2 = get_line_equation(ray2_position, ray2_velocity)

    # If the slopes of the two rays are the same, they are parallel and will never intersect
    if m1 == m2:
        return None

    # Calculate the point of intersection using our two line equations
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1

    # These are rays, not lines. Even if they intersect, we want to make sure that the intersection point is forwards, not backwards
    if is_on_ray((x, y), ray1_position, ray1_velocity) and is_on_ray((x, y), ray2_position, ray2_velocity):
        return (x, y)
    return None


test_area = (200000000000000, 400000000000000)
test_intersections = 0
sorted_keys = sorted(points.keys())

# Iterate over every pair of stones and calculate their intersection points
for x in range(len(sorted_keys)):
    for y in range(x + 1, len(sorted_keys)):
        intersection = calculate_intersection(sorted_keys[x], points[sorted_keys[x]], sorted_keys[y],
                                              points[sorted_keys[y]])

        # If they intersect, check if it happens within our desired test area
        if intersection is not None and test_area[0] <= intersection[0] <= test_area[1] and test_area[0] <= \
                intersection[1] <= test_area[1]:
            test_intersections += 1
print("The number of collisions that happen inside the testing area is:", test_intersections)

# Introducing Z3, which is a library for solving systems of linear equations.
# I haven't used it before, but it appears to be quite powerful. I plan on learning more about it over the next year.
# Set the variables we want to find (the starting position and the throw's velocity)
starting_position = (Real(f'sp_x'), Real(f'sp_y'), Real(f'sp_z'))
god_throw_velocity = (Real(f'd_x'), Real(f'd_y'), Real(f'd_z'))

# Instantiate a new equation solver
solver = Solver()

# Go over every stone and add a new constraint on the variables...
for s in range(len(sorted_keys)):

    # Create a variable for the time of collision with this stone
    t = Real(f't_{s}')

    # Grab the position and velocity of this stone, these will be used as constants in the constraints
    position = sorted_keys[s]
    velocity = points[position]

    # Add a constraint for each dimension x,y,z
    for dimension in range(3):
        # Basically, the position of the thrown rock must, at some point in time, match the current stone's position
        solver.add(starting_position[dimension] + (t * god_throw_velocity[dimension]) == position[dimension] + (
                    t * velocity[dimension]))

# Run the calculation, and make sure that a solution exists
if solver.check() == sat:

    # The model contains the variables
    model = solver.model()
    solution = sum([int(str(solver.model().evaluate(starting_position[dimension]))) for dimension in range(3)])
    print(
        f"By throwing a rock from ({', '.join([str(solver.model().evaluate(starting_position[dimension])) for dimension in range(3)])}) with a velocity of ({', '.join([str(solver.model().evaluate(god_throw_velocity[dimension])) for dimension in range(3)])}), we can hit all rocks, giving us a coordinate sum of:",
        solution)

else:
    print("FAILURE")