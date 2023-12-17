import os

# Parse input file
input = open("input_day_15.txt")
lines = input.readlines()
input.close()
hash_map = {}


# Function for calculating the HASH value of a string
def HASH(string):
    current_value = 0
    for letter in string:
        ascii = ord(letter)
        current_value += ascii
        current_value *= 17
        current_value %= 256
    return current_value


value_sums = 0
for string in lines[0].split(","):

    # Pt. 1 - Calculate each string's HASH value
    current_value = HASH(string)
    value_sums += current_value

    # Pt. 2 - If there's an equal sign, we're either adding or replacing a lens
    if "=" in string:

        # Which lens, what focus length, which box?
        label, focus = string.split("=")
        box = HASH(label)
        if box not in hash_map:
            hash_map[box] = []
        found = False

        # Look to see if this lens exists in the box already
        for lens in hash_map[box]:

            # If it does, update the focus length, don't move anything around
            if lens[0] == label:
                lens[1] = focus
                found = True
                break

        # If it doesn't, add it to the end of the box
        if not found:
            hash_map[box].append([label, focus])

    # Pt. 2 - If there's a minus sign, we're removing a lens if it exists
    elif '-' in string:

        # Which label from which box?
        label = string[0:-1]
        box = HASH(label)
        if box not in hash_map:
            hash_map[box] = []

        # Look for the lens in the box, remove it if it's present
        for lens in hash_map[box]:
            if lens[0] == label:
                hash_map[box].remove(lens)
                break

print("The sum of running the HASH algorithm on all the strings is:", value_sums)

# Pt. 2 - Calculate the focus power for each lens
focus_power_sum = 0
for box in hash_map:
    focus_power = 0
    for index, lens in enumerate(hash_map[box]):
        # "One plus the box number" * "The slot number of the lens" * "The focal length of the lens"
        focus_power += ((1 + box) * (index + 1) * int(lens[1]))
    focus_power_sum += focus_power
print("The total focusing power of the final lens configuration is:", focus_power_sum)