import os

# Parse input file
input = open("input_day_5.txt")

seeds = []
maps = []

# Iterate over the input and parse out the list of seeds and a list of the maps
for line in input:
    if "seeds:" in line:
        seeds = [int(val) for val in line.strip().split()[1:]]
    elif ":" in line:
        maps.append([])
    elif line.isspace():
        if len(maps) > 0:
            maps[-1].sort(key=lambda x: x[1])
    else:
        values = [int(val) for val in line.strip().split()]
        maps[-1].append(values)
input.close()

# Sort the maps in ascending order based on the source values
maps = [sorted(map, key=lambda x: x[1]) for map in maps]


# Helper function: Given a seed, iterates over the maps and finds the final location value
def readMaps(seed, maps):
    value = seed
    for map in maps:
        for r in range(len(map)):
            # If we find an intersection, apply the conversion
            if map[r][1] <= value and map[r][1] + map[r][2] - 1 >= value:
                value += (map[r][0] - map[r][1])
                break
            # Otherwise with no intersection, the value maps to itself
            elif map[r][1] > value:
                break
    return value


# Find the lowest location value for each seed (pt. 1)
min_location = float('inf')
for seed in seeds:
    min_location = min(min_location, readMaps(seed, maps))
print("The lowest location for the given seeds is:", min_location)

# Convert the seed list into a list of ranges
ranges = []
for s in range(0, len(seeds), 2):
    ranges.append([seeds[s], seeds[s] + seeds[s + 1] - 1])


# Helper function to slice the ranges given a map of translations.
def slice_ranges(input_range, map):
    input_start, input_end = input_range
    current = input_start
    result = []

    # Adjust any ranges in the map that overlap with the end of the input_range to stay contained in the input_range
    # e.g. if input_range = [10,15] and the map has an entry for [5,12] then adjust it to [10,12]
    adjusted_ranges = []
    for r in map:
        destination_range_start, source_range_start, span = r
        source_range_end = source_range_start + span - 1

        # Throw away any ranges that don't intersect with our input_range
        if source_range_start > input_end or source_range_end < input_start:
            continue

        # Calculate the translation value of this mapping (before we mess with the source_range_start, potentially)
        difference = destination_range_start - source_range_start

        # Adjust the start and end of the range if they are outside the input_range
        source_range_start = max(input_start, source_range_start)
        source_range_end = min(input_end, source_range_end)

        adjusted_ranges.append([source_range_start, source_range_end, difference])

    # Sort the adjusted ranges in ascending order
    sorted_ranges = sorted(adjusted_ranges)
    for r in sorted_ranges:
        source_start, source_end, translation = r

        # Check if there is a gap between the current position and the start of the range, don't apply the translation
        if current < source_start:
            result.append([current, source_start - 1])

        # If there's a valid intersection, apply the translation
        result.append([source_start + translation, source_end + translation])

        # Update our current position
        current = source_end + 1

    # If there's any remaining values between the current position and the end of the range, don't apply the translation
    if current <= input_end:
        result.append([current, input_end])

    return result


# Iterate over each map and slice the ranges each time
for map in maps:
    new_ranges = []
    for r in ranges:
        new_ranges += slice_ranges(r, map)
    ranges = new_ranges

print("The lowest location for the given seed ranges is:", min(ranges)[0])