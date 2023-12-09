
# Generate sequences of differences until we find a sequence that is all zeroes and return it
def get_to_zeroes(line):
    lines = [line]
    while lines[-1] != len(lines[-1]) * [0]:
        next_line = []
        for x in range(len(lines[-1]) - 1):
            next_line.append(lines[-1][x + 1] - lines[-1][x])
        lines.append(next_line)
    return lines

# Generate the all-zero sequence and then iterate back up to extrapolate both forward and back by one value
def extrapolate_history_values(line):
    lines = get_to_zeroes(line)
    lines.reverse()
    lines[0].append(0)
    for x in range(1, len(lines)):
        lines[x] = [lines[x][0] - lines[x - 1][0]] + lines[x] + [lines[x][-1] + lines[x - 1][-1]]
    return lines[-1][0], lines[-1][-1]

# Parse input file
input = open("input_day_9.txt")

next_history_sum = 0
previous_history_sum = 0

for line in input:
    line = [int(val) for val in line.strip().split()]
    previous, next = extrapolate_history_values(line)
    next_history_sum += next
    previous_history_sum += previous
input.close()

print("The sum of the next extrapolated history values is:", next_history_sum)
print("The sum of the previous extrapolated history values is:", previous_history_sum)