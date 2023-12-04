input_file = open("input_day_4.txt", "r")

s = 0

for line in input_file:
    useful_line = line.strip()[line.index(":") + 1:]
    winning_numbers, my_numbers = map(str, useful_line.split("|"))
    winning_numbers = winning_numbers.strip().split()
    my_numbers = my_numbers.strip().split()

    score = 0
    for winning_number in winning_numbers:
        number_found = False
        for my_number in my_numbers:
            if winning_number == my_number:
                number_found = True
                break

        if number_found:
            if score == 0:
                score = 1
            else:
                score *= 2

    s += score


input_file.close()

print(s)


# --------------- PART 2 ---------------


input_file = open("input_day_4.txt", "r")

cards = []

for line in input_file:
    useful_line = line.strip()[line.index(":") + 1:]
    winning_numbers, my_numbers = map(str, useful_line.split("|"))
    winning_numbers = winning_numbers.strip().split()
    my_numbers = my_numbers.strip().split()

    cards.append({ "winning_numbers" : winning_numbers,
                   "my_numbers" : my_numbers,
                   "copies" : 1 })

input_file.close()

for i in range(len(cards)):
    card = cards[i]
    score = 0

    for winning_number in card["winning_numbers"]:
        number_found = False
        for my_number in card["my_numbers"]:
            if winning_number == my_number:
                number_found = True
                break

        if number_found:
            score += 1

    for j in range(1, score + 1):
        cards[i + j]["copies"] += card["copies"]


s = 0

for card in cards:
    s += card["copies"]

print(s)