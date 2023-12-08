import math

# Parse input file
input = open("input_day_8.txt")

paths = {}
lines = input.readlines()
input.close()

# Grab the instructions from the first line and save them for later
instructions = lines[0].strip()
starting_nodes = []

# Create a dictionary such that paths[source][L or R] = destination
for line in lines[2:]:

    line = line.split()
    source = line[0]
    left = line[2].replace('(', '').replace(',', '')
    right = line[3].replace(')', '')
    paths[source] = {"L": left, "R": right}

    # Track all of the starting nodes for pt. 2
    if source[2] == 'A':
        starting_nodes.append(source)

# I found that the puzzle input was designed kindly
# Rule 1: The paths from each starting node to an ending node are cyclical
# Rule 2: There are no lead-up steps before entering the cycle (i.e. AAA -> BBB -> CCC -> DDD -> ZZZ -> DDD -> ZZZ -> DDD -> ZZZ ... )
# Rule 3: There is only a single ending node in each cycle (i.e. AAA -> ZZZ -> BBB -> QQZ -> AAA ... )
# Following Rule 1, let's calculate the size of the cycles for all of the starting points
cycle_sizes = []
for node in starting_nodes:
    steps = 0
    current_node = node
    while current_node[2] != 'Z':
        current_node = paths[current_node][instructions[steps % len(instructions)]]
        steps += 1
    # Pt. 1 only cares about AAA. And given Rule 3, we know that it will end on ZZZ instead of another --Z node.
    if node == 'AAA':
        print("The amount of steps from AAA to ZZZ is:", steps)
    cycle_sizes.append(steps)

# Given Rule 2 and the cycle sizes, we just need to calculate the least-common-multiple of the cycle sizes to find where they all will overlap for the first time
# If Rule 2 didn't exist, we would need to calculate an offset for each node's cycle, which would be a pain...
least_common_multiple = 1
for cycle in cycle_sizes:
    least_common_multiple = (least_common_multiple * cycle) // math.gcd(least_common_multiple, cycle)
print("The number of steps until all ghosts would reach an exit node is:", least_common_multiple)