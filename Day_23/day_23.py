from copy import deepcopy

# Parse input file
input = open("input_day_23.txt")
lines = input.readlines()
input.close()

starting_position = None
ending_position = None
height = len(lines)
width = len(lines[0].strip())
graph1 = {}
slopes = {
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
    'v': (1, 0)
}


# They've gotten me to bust out a class this time...
class Node:

    def __init__(self, position):
        self.initial_position = position
        self.positions = set([position])
        self.neighbors = set()
        self.forced_neighbor = None
        self.value = 1

    # To make the final graphs manageable, we will combine long lines of points with no branching paths into single nodes
    # When we do this, we combine all of the positions merged into a set, and update the neighbors to point to the new combo-node.
    def combine_node(self, other_node):
        self.positions = self.positions.union(other_node.positions)
        for neighbor in other_node.neighbors:
            graph2[neighbor].neighbors.remove(other_node.initial_position)
            graph2[neighbor].neighbors.add(self.initial_position)
        self.neighbors = self.neighbors.union(other_node.neighbors).difference(self.positions)
        self.value += other_node.value


# Parse through the input and create node objects for each walkable tile. No neighbors yet.
for row in range(len(lines)):
    for column in range(len(lines[row].strip())):
        if lines[row][column] in '.v^<>':
            node = Node((row, column))
            graph1[(row, column)] = node
            if row == 0:
                starting_position = (row, column)
            elif row == height - 1:
                ending_position = (row, column)

# Now we add neighbors to the nodes. Including a "forced" neighbor for the sloped tiles that we would be pushed to
for node in graph1.values():
    for direction in slopes.values():
        neighbor = (node.initial_position[0] + direction[0], node.initial_position[1] + direction[1])
        if neighbor in graph1:
            node.neighbors.add(neighbor)
            spot = lines[node.initial_position[0]][node.initial_position[1]]
            if spot in slopes.keys():
                node.forced_neighbor = (
                node.initial_position[0] + slopes[spot][0], node.initial_position[1] + slopes[spot][1])

# Copy the graph, we need different graphs for part1 vs. part2
graph2 = deepcopy(graph1)

# For pt. 2, we merge the straight-line paths with no branches, and remove them from the graph to shrink it down.
while True:
    merged = False
    for node in graph2.values():
        if len(node.neighbors) > 2:
            continue
        for neighbor in node.neighbors:
            if len(graph2[neighbor].neighbors) == 2:
                node.combine_node(graph2[neighbor])
                del graph2[graph2[neighbor].initial_position]
                merged = True
                break
        if merged:
            break
    if not merged:
        break


# Main search function
def find_longest_path(starting_node, graph, part2):
    max_length = 0
    stack = [(starting_node, set([starting_node.initial_position]))]

    while len(stack) > 0:

        current_node, visited = stack.pop()

        # If we've found the end, check if this is the new longest path found
        if ending_position in current_node.positions:
            max_length = max(max_length, sum([graph[node].value for node in visited]))
            continue

        # Examine our neighbors. If we're on a slippery tile in pt. 1, that's the only neighbor we can go to.
        for neighbor in current_node.neighbors:
            if neighbor not in visited:
                if part2 or current_node.forced_neighbor is None or neighbor == current_node.forced_neighbor:
                    new_visited = visited.copy()
                    new_visited.add(neighbor)
                    stack.append((graph[neighbor], new_visited))

    return max_length


# Grab the correct Node class objects that we're starting on in each graph
for node in graph1:
    if starting_position == graph1[node].initial_position:
        starting_node1 = graph1[node]
        starting_node1.value -= 1
for node in graph2:
    if starting_position in graph2[node].positions:
        starting_node2 = graph2[node]
        starting_node2.value -= 1

# Warning: Pt. 2 does take a minute or two to complete.
print("The longest path down the mountain with the slippery tiles is:",
      find_longest_path(starting_node1, graph1, False))
print("The longest path down the mountain without the slippery tiles is:",
      find_longest_path(starting_node2, graph2, True))