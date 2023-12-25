import networkx as nx

# Parse input file
input = open("input_day_25.txt")
lines = input.readlines()
input.close()

# Parse the input into a map.
edges = set()
for line in lines:
    key, values = line.strip().split(": ")
    values = values.split(" ")
    for value in values:
        edges.add(tuple(sorted([key, value])))


# It's late. I'm exhausted from 25 nights of problems. So I found an algorithm online called the Stoer-Wagner algorithm
# Which takes in a graph and finds the minimum number of cuts needed to separate the graph into two parts.
# So I grabbed a library that implements it, assumed that it would require 3 cuts, and ran it.
# All 50 stars achieved, Merry Christmas!
def find_min_cut(edges):
    G = nx.Graph()
    for (node1, node2) in edges:
        G.add_edge(node1, node2)
    _, partition = nx.stoer_wagner(G)
    return len(partition[0]) * len(partition[1])


print("The product of the two disjointed components counts is:", find_min_cut(edges))