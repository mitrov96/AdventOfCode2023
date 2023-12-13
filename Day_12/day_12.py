
# Parse input file
input = open("input_day_12.txt")
lines = input.readlines()
input.close()


def calculate_arrangements(springs, groups, current_position, num_springs_in_current_group, groups_matched, memo):
    # Introducing "memoization," a method for caching the results of function calls.
    # The key will be a tuple of the arguments (that change) and the value is the previous result
    arguments_tuple = (current_position, num_springs_in_current_group, groups_matched)
    result = None

    # If we've seen these arguments before, return the cached result
    if arguments_tuple in memo:
        return memo[arguments_tuple]

    # If we've reached the end of the string, check if we've matched all of the required groups
    elif current_position == len(springs):

        # We might have been tracking a group up to the end of the string, so count it if it matches the groups
        if groups_matched < len(groups) and num_springs_in_current_group == groups[groups_matched]:
            groups_matched += 1

        if groups_matched == len(groups):
            result = 1
        else:
            result = 0

    # If we've matched all of our groups, but we haven't reached the end of the string, we should fail if we find any more springs
    elif groups_matched == len(groups):
        if springs[current_position] == '#' or num_springs_in_current_group > 0:
            result = 0
        else:
            result = calculate_arrangements(springs, groups, current_position + 1, 0, groups_matched, memo)

    # If we have encountered a spring, add it to the currently-tracked group and continue
    elif springs[current_position] == '#':
        result = calculate_arrangements(springs, groups, current_position + 1, num_springs_in_current_group + 1,
                                        groups_matched, memo)


    # If we have encountered a dot, then...
    elif springs[current_position] == '.':

        # If we weren't tracking any springs, continue on
        if num_springs_in_current_group == 0:
            result = calculate_arrangements(springs, groups, current_position + 1, 0, groups_matched, memo)

        # If we were tracking a group of springs and it matches the next group, then we've got a new match!
        elif num_springs_in_current_group == groups[groups_matched]:
            result = calculate_arrangements(springs, groups, current_position + 1, 0, groups_matched + 1, memo)

        # If we were tracking a group of springs and it _doesn't_ match the next group, then this path is wrong and we can stop
        else:
            result = 0

    # If we have encountered an unknown spot, then...
    elif springs[current_position] == '?':

        # Pretend it was a spring, and add it to the currently-tracked group (or start a new group...)
        result = calculate_arrangements(springs, groups, current_position + 1, num_springs_in_current_group + 1,
                                        groups_matched, memo)

        # Pretend it was a dot, then we have to check if we were tracking any spring groups. See the above if-block for the logic
        if num_springs_in_current_group == 0:
            result += calculate_arrangements(springs, groups, current_position + 1, 0, groups_matched, memo)
        elif num_springs_in_current_group == groups[groups_matched]:
            result += calculate_arrangements(springs, groups, current_position + 1, 0, groups_matched + 1, memo)
        else:
            result += 0

    # Add the result to the memo and return it
    memo[arguments_tuple] = result
    return result


total_ways = 0
total_ways2 = 0
for line in lines:
    springs, groups = line.split()
    groups = [int(val) for val in groups.split(',')]
    total_ways += calculate_arrangements(springs, groups, 0, 0, 0, {})
    total_ways2 += calculate_arrangements(((springs + '?') * 5)[:-1], groups * 5, 0, 0, 0, {})
print("The number of possible arrangements for the folded-up list is:", total_ways)
print("The number of possible arrangements for the unfolded list is:", total_ways2)