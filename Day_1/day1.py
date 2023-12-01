import re


def readFile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines


def part1(lines):
    sum = 0
    pattern = r'[^0-9]'
    for line in lines:
        line = line.replace("\n", "")
        numbers = re.sub(pattern, "", line)
        num = int(numbers[0] + numbers[-1])
        sum += num
    return sum


digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def part2(lines):
    sum = 0
    for line in lines:
        first = ""
        last = ""
        for index, char in enumerate(line):
            if char.isdigit():
                if first == "":
                    first = char
                last = char
                continue
            for digit in digits:
                if line[index:index + len(digit)] == digit:
                    if first == "":
                        first = digits.index(digit) + 1
                    last = digits.index(digit) + 1
        num = int(f"{first}{last}")
        sum += num
    return sum


def main():
    lines = readFile("input_day_1.txt")
    print("Part 1: " + str(part1(lines)))
    print("Part 2: " + str(part2(lines)))


main()
