import numpy as np
import heapq as hq

a = np.array([list(line.strip()) for line in open("input_day_17.txt").readlines()])

LEN = len(a) # ATTENTION: only works for arrays of same dimensional length
end = (LEN-1, LEN-1)
N, E, S, W = range(4)
to_direction = ['N','E','S','W']

def goto(node, direction):
    dirs = [(-1,0), (0,1), (1,0), (0,-1)]
    d = dirs[direction]
    return (node[0]+d[0], node[1]+d[1])

def in_board(node):
    return True if (0 <= node[0] <= end[0]) and (0 <= node[1] <= end[1]) else False

# just insert all nodes in the priority queue
# and dont care for higher cost nodes
# they will not be taken out there anyways

# dijkstra
# node: direction of travel  N O S W
# and a counter for same directions
# three same -> turn
# previous list to backtrack
def dijkstra():

    PR = [(-1,-1)]
    heap = [(0, (0,0), S, 0, PR)] # 0 is the distance, S is the start vertice (x,y) coordintates, direction and count
    visited = set()
    # idea is that we have a sorted heap queue
    # we add every traversed node unconditionally to the hq
    # this means we have duplicates with shorter paths
    # but because of the sorting we always find the best path
    # and duplicates are detected and thrown away later on
    # in other words we spare the step to modify the temporary node list
    # instead we add new elements - this must be checked later on by
    # comparing if we already found a shorter distance
    while heap:
        #print(heap)
        dist, node, direction, count, prev = hq.heappop(heap)
        if (node, direction, count) not in visited: # forward only, dont step back
            #print(f"visiting {node}")
            if node == end:
                print(dist)
                print(prev)
                return dist
            if in_board(node) and (count <= 3): # nodes not in board are consumed
                visited.add((node, direction, count))
                for direction_next in (range(4)):
                    node_next = goto(node, direction_next)
                    if (in_board(node_next)):
                        # update distance of this node
                        dist_next = dist + int(a[node_next[0]][node_next[1]])
                        count_next = count + 1 if direction_next == direction else 0
                        if (node_next, direction_next, count_next) not in visited and count_next <= 2 and ((direction + 2) % 4) != direction_next:
                            #print(f"goto {node_next}")
                            x = prev.copy()
                            x.append(node)
                            hq.heappush(heap, (dist_next, node_next, direction_next, count_next, x)) # FIXME only add if not visited

print(dijkstra())




# PART 2

import numpy as np
import heapq as hq

a = np.array([list(line.strip()) for line in open("input_day_17.txt").readlines()])
END = (len(a)-1, len(a[0])-1)
N, E, S, W = range(4)

# return next node after going at direction
def goto(node, direction):
    offset = [(-1,0), (0,1), (1,0), (0,-1)][direction]
    return (node[0]+offset[0], node[1]+offset[1])

# returns True if node is inside array, False otherwise
def in_board(node):
    return True if (0 <= node[0] <= END[0]) and (0 <= node[1] <= END[1]) else False

# returns True if we go back where we came from, False otherwise
def backwards(direction1, direction2):
    return ((direction1 + 2) % 4) == direction2

# This implements a modified dijkstra where we just insert all nodes we are
# allowed to visit into the priority queue. We do not care for higher cost
# nodes being also inserted there, because they will only be taken into account
# (heapq being a priority sorted queue) if we have to backtrack (if we are not
# allowed to follow the shortest path because of path-constraints)
# Returns the shortest path costs to END
def dijkstra():
    heap = [(0, (0,0), S, 0), (0, (0,0), E, 0)]
    visited = set()
    while heap:
        cost, node, direction, count = hq.heappop(heap)
        # dont visit a node from same direction and count twice, because it
        # must be the same path
        if (node, direction, count) not in visited:
            visited.add((node, direction, count))
            if node == END and count >= 3:
                return cost
            for direction_ in (range(4)):
                node_ = goto(node, direction_)
                if (in_board(node_)):
                    cost_ = cost + int(a[node_[0]][node_[1]])
                    count_ = count + 1 if direction_ == direction else 0
                    if ((node_, direction_, count_) not in visited and
                        count_ <= 9 and
                        not backwards(direction, direction_) and
                        ((direction_ == direction) or (count >= 3))):
                        hq.heappush(heap, (cost_, node_, direction_, count_))
print(dijkstra())