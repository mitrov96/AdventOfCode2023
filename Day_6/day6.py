import math

# Parse input file
input = open("input_day_6.txt")

times, distances = input.readlines()
input.close()

# Add the "combined" race to the list of times/distances so we can calculate everything together
times = times.split()[1:]
distances = distances.split()[1:]
times.append(''.join(times))
distances.append(''.join(distances))
times = [int(val) for val in times]
distances = [int(val) for val in distances]

# So I "solved" the problem using brute force, but went back and found a mathematic approach. Use this boolean to toggle which method is used.
do_old_method = False

# Function for calculating how far the boat travels
def calculate_distance_traveled(time_charging, total_time):
    return time_charging * (total_time - time_charging)

margin_of_error = 1
ways_to_win = 0

if do_old_method:
    for x in range(len(times)):
        ways_to_win = 0
        for y in range(times[x]):
            distance_traveled = calculate_distance_traveled(y, times[x])
            if distance_traveled > distances[x]:
                ways_to_win += 1
        if x < len(times) - 1:
            margin_of_error *= ways_to_win
    print("The margin of error for all of the split races is:", margin_of_error)
    print("The number of ways to win the large race is:", ways_to_win)

else:
    for x in range(len(times)):
        # calculate_distance_traveled is a parabolic function
        # We want to find where calculate_distance_traveled == record_distance
        # Translating calculate_distance_traveled to the standard parabolic form: ax^2 + bx + c = 0
        #       -(time_charging)^2 + (total_time)(time_charging) = record_distance
        #       -(time_charging)^2 + (total_time)(time_charging) - record_distance = 0
        a = -1
        b = times[x] # total_time
        c = -distances[x] # record_distance

        # Good old quadratic formula: x = (-b +- sqrt(b**2 - 4ac)) / 2a to find the two values of x (time_charging)
        solutions = [(-b + math.sqrt(b ** 2 - (4 * a * c))) / (2 * a), (-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a)]

        # Sort the solutions, just in case
        solutions.sort()

        # Now these solutions are for "matching" the record_distance. We need to _beat_ the distance. So use ceil/floor to do so
        # Note that if the solution occurs right on a whole number, we need to jump to the next whole number to _beat_ the distance
        solutions = [math.ceil(solutions[0] if not solutions[0].is_integer() else solutions[0] + 1), math.floor(solutions[1] if not solutions[1].is_integer() else solutions[1] - 1)]

        # Calculate the number of ways to win given our solutions
        ways_to_win = solutions[1] - solutions[0] + 1

        if x < len(times) - 1:
            margin_of_error *= ways_to_win

    print("The margin of error for all of the split races is:", margin_of_error)
    print("The number of ways to win the large race is:", ways_to_win)