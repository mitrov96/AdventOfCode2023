input = open("input_day_16.txt")
lines = input.readlines()
input.close()

height = len(lines)
width = len(lines[0].strip())

# Reflections for a backslash character '\'
backslash_translation = {
    'R': 'D',
    'D': 'R',
    'U': 'L',
    'L': 'U'
}

# Reflections for a forward slash character '/'
slash_translation = {
    'R': 'U',
    'D': 'L',
    'U': 'R',
    'L': 'D'
}


# Helper function. Given a position and a direction, return the next position
def get_next_in_direction(position, direction):
    if direction == 'R':
        return (position[0], position[1] + 1)
    elif direction == 'L':
        return (position[0], position[1] - 1)
    elif direction == 'U':
        return (position[0] - 1, position[1])
    elif direction == 'D':
        return (position[0] + 1, position[1])


# Main function. Takes in a starting set of beams, containing a tuple of the position and the direction: {((x, y), dir)}
def shoot_beam(beams):
    memo = set()
    energized = set()

    # Keep going while we have beams bouncing around
    while len(beams) > 0:

        # Grab a random beam
        beam_position, beam_direction = beams.pop()

        # If we've seen this state before, we can prevent loops by stopping here
        if (beam_position, beam_direction) in memo:
            continue

        # Track this stata for the memo. Mark this tile as energized
        memo.add((beam_position, beam_direction))
        energized.add(beam_position)

        # If we are on a dot, we just keep going in the same direction
        if lines[beam_position[0]][beam_position[1]] == '.':
            next_direction = beam_direction

        # If we hit a backslash or forward slash, we get reflected
        elif lines[beam_position[0]][beam_position[1]] == '\\':
            next_direction = backslash_translation[beam_direction]

        elif lines[beam_position[0]][beam_position[1]] == '/':
            next_direction = slash_translation[beam_direction]

        # If we hit a splitter, depending on our direction, we either keep going straight or we split in two directions
        elif lines[beam_position[0]][beam_position[1]] == '-':
            if beam_direction in 'LR':
                next_direction = beam_direction
            else:
                next_direction = 'LR'

        elif lines[beam_position[0]][beam_position[1]] == '|':
            if beam_direction in 'UD':
                next_direction = beam_direction
            else:
                next_direction = 'UD'

        # Since the splitters might produce two different directions, we want to track both...
        for direction in next_direction:

            next_position = get_next_in_direction(beam_position, direction)

            # If the beam has gone off the board, stop tracking it
            if next_position[0] >= 0 and next_position[1] >= 0 and next_position[0] < height and next_position[
                1] < width:
                beams.add((next_position, direction))
    return len(energized)


# Shoot beams along each of the four edges, find the one with the highest energy level
most_energized = 0
for x in range(width):
    energized = shoot_beam(set([((0, x), 'D')]))
    most_energized = max(most_energized, energized)
    energized = shoot_beam(set([((height - 1, x), 'U')]))
    most_energized = max(most_energized, energized)
for x in range(height):
    energized = shoot_beam(set([((x, 0), 'R')]))
    # Part 1 Solution
    if x == 0:
        print("By shooting the laser at the top-left of the board going right, the total number of tiles energized is:",
              energized)
    most_energized = max(most_energized, energized)
    energized = shoot_beam(set([((x, width - 1), 'L')]))
    most_energized = max(most_energized, energized)
print("The optimal laser configuration results in the total number of energized tiles being:", most_energized)