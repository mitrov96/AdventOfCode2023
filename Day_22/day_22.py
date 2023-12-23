# I take no credit for this solution's second part. I would not have figured this problem out on my own.

# Parse input file
input = open("input_day_22.txt")
lines = input.readlines()
input.close()

# Parse the input and save the bricks as tuples of positions (x1, y1, z1, x2, y2, z2)
bricks = []
for line in lines:
    bricks.append(tuple([int(value) for value in line.strip().replace('~', ',').split(',')]))

# Sort the bricks in ascending order, and prepare to make maps of the supporting-relationships
bricks.sort(key = lambda x: min(x[2], x[5]))
supported_bricks = {}
supporting_bricks = {}

# Given a brick, let it fall as far as it can
def move_brick_down(index, brick, group):

    x1, y1, z1, x2, y2, z2 = brick
    z_min = min(z1, z2)
    distance = z_min - 1 # By default, we can fall all the way to z = 1

    # Initialize the two maps as empty.
    supported_bricks[index] = set() # Value is a list of all the bricks that are being supported by Brick Key
    supporting_bricks[index] = set() # Value is a list of all the bricks that are supporting Brick Key

    # If the brick isn't on the ground already...
    if distance > 0:

        # We want to know which bricks this brick is going to land on, if any
        closest_obstacle_z = 0
        closest_brick_indexes = set()

        # Go through all the lower bricks to check for collisions
        for other_index, other_brick in enumerate(group[:index]):

            ox1, oy1, oz1, ox2, oy2, oz2 = other_brick

            # If the falling brick intersects with a lower brick in the x-y plane, then it will hit the lower brick on the way down
            if min(x1, x2) <= max(ox1, ox2) and max(x1, x2) >= min(ox1, ox2) and min(y1, y2) <= max(oy1, oy2) and max(y1, y2) >= min(oy1, oy2):
                oz_max = max(oz1, oz2)

                # If this is true, then this is now the highest (first) brick we will collide with
                if oz_max > closest_obstacle_z:
                    closest_obstacle_z = oz_max
                    closest_brick_indexes = set([other_index])

                # If this is true, then the brick will land on more than one brick (unless we find a higher brick to land on)
                elif oz_max == closest_obstacle_z:
                    closest_brick_indexes.add(other_index)

        # Update our distance and supporting/supported bricks maps (shouldn't make any changes if we hit no bricks on the way down.)
        distance = z_min - closest_obstacle_z - 1
        supporting_bricks[index] = closest_brick_indexes
        for supporting_brick in closest_brick_indexes:
            supported_bricks[supporting_brick].add(index)

    # If the brick is going to fall at all, update its position in the bricks list
    if distance > 0:
        new_brick = (x1, y1, z1 - distance, x2, y2, z2 - distance)
        group[index] = new_brick

# Make the bricks fall!
for x in range(len(bricks)):
    move_brick_down(x, bricks[x], bricks)

# Time to look for bricks that can be safely disintegrated
disintegration_candidates = 0
for x in range(len(bricks)):
    can_disintegrate = True

    # Go through every brick that the candidate brick is supporting...
    for y in supported_bricks[x]:

        # ... and if this brick is the only one supporting it, then it can't be disintegrated
        if len(supporting_bricks[y]) == 1:
            can_disintegrate = False
            break

    if can_disintegrate:
        disintegration_candidates += 1

print("The number of bricks that can be safely disintegrated is:", disintegration_candidates)

# Time to calculate how many bricks we can make fall
falling_bricks = 0
for x in range(len(bricks)):

    # Start with the disintegrated brick "falling" (we'll subtract this out later)
    bricks_to_fall = set([x])
    fallen_bricks = set()

    # Keep iterating while we have bricks that should be falling
    while len(bricks_to_fall) > 0:

        # Take a brick and mark it as "fallen"
        next_brick = bricks_to_fall.pop()
        fallen_bricks.add(next_brick)

        # Check every brick that the now-fallen brick was supporting
        for supported_brick in supported_bricks[next_brick]:

            # And check if all of its supporting bricks have now fallen. If so, it's time for this brick to fall as well.
            if len(supporting_bricks[supported_brick].difference(fallen_bricks)) == 0:
                bricks_to_fall.add(supported_brick)

    # Count up how many bricks that fell (minus the one we disintegrated)
    falling_bricks += len(fallen_bricks) - 1

print("The number of bricks that can be made to fall by disintegrating each brick is:", falling_bricks)