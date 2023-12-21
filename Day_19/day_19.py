
input = open("input_day_19.txt")
lines = input.readlines()
input.close()

workflows = {}
parts = []
workflow_reading = True

# Read through the input to create a workflow map {'in': (['x', '>', 100, 'R'], 'A')}
# We are also creating a list of parts for pt. 1, which are also a map of qualities {'x': 100, 'm': 200, 'a': 300, 's': 400}
for line in lines:

    # We found the separator space, switch to reading parts instead of workflows
    if line.isspace():
        workflow_reading = False
        continue

    # Reading workflow lines, populating the workflows map
    if workflow_reading:
        line = line.strip().split("{")
        label = line[0]
        line = line[1].split(",")
        output = line[-1][:-1]
        steps = []
        for step in line[:-1]:
            quality = step[0]
            comparer = step[1]
            step = step.split(':')
            value = int(step[0][2:])
            output2 = step[1]
            steps.append((quality, comparer, value, output2))
        workflows[label] = (steps, output)

    # Reading the part lines, populating the parts list
    else:
        line = line.strip().replace('{', '').replace('}', '')
        line = line.split(",")
        qualities = {}
        for quality in line:
            quality = quality.split('=')
            qualities[quality[0]] = int(quality[1])
        parts.append(qualities)


# Function for pt. 1 to determine if a part is accepted or refused
def go_through_workflow(label, part):
    # REJECTED, return 0
    if label == 'R':
        return 0

    # ACCEPTED, return the sum of the part's values
    elif label == 'A':
        return sum(part.values())

    workflow, output = workflows[label]

    # Go through each of the steps in the workflow
    for step in workflow:
        quality, comparator, value, result = step
        use_result = False

        # If our part matches one of the rules, jump to the label declared by the rule
        if comparator == '<' and part[quality] < value:
            use_result = True
        elif comparator == '>' and part[quality] > value:
            use_result = True
        if use_result:
            return go_through_workflow(result, part)

    # If we got here, we passed all the rules and can jump to the label declared at the end of the current workflow
    return go_through_workflow(output, part)


# Sum up the values of all the accepted parts
sum_accepted = 0
for part in parts:
    sum_accepted += go_through_workflow('in', part)
print("The sum of all the accepted part values is:", sum_accepted)


# Function for pt. 2 to break down ranges of part values and filter out only the accepted ranges
def break_down_workflows(label, current_ranges):
    # REJECTED, none in this set of ranges will work
    if label == 'R':
        return 0

    # ACCEPTED, calculate how many unique combinations are in this set of ranges
    # Thankfully, there shouldn't be any overlap between accepted ranges, since we are creating all disjoint sets of ranges
    elif label == 'A':
        total = 1
        for quality in current_ranges:
            total *= current_ranges[quality][1] - current_ranges[quality][0] + 1
        return total

    total = 0
    workflow, output = workflows[label]

    # Go through each step in the current workflow
    for step in workflow:
        quality, comparator, value, result = step

        # If the rule will split our ranges, we need to handle the split
        # Create a new set of ranges for the combinations that would match the rule and recurse
        # Then, with the remaining ranges that don't match the rule, we continue onwards
        if comparator == '<' and current_ranges[quality][0] < value <= current_ranges[quality][1]:
            ranges_copy = current_ranges.copy()
            ranges_copy[quality] = (current_ranges[quality][0], value - 1)
            current_ranges[quality] = (value, current_ranges[quality][1])
            total += break_down_workflows(result, ranges_copy)

        elif comparator == '>' and current_ranges[quality][0] <= value < current_ranges[quality][1]:
            ranges_copy = current_ranges.copy()
            ranges_copy[quality] = (value + 1, current_ranges[quality][1])
            current_ranges[quality] = (current_ranges[quality][0], value)
            total += break_down_workflows(result, ranges_copy)

    return total + break_down_workflows(output, current_ranges)


accepted_combinations = break_down_workflows('in', {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)})
print("The total number of combinations of 'xmas' values that would be accepted is:", accepted_combinations)
