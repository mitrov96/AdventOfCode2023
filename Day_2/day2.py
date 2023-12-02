def part_1(input) -> int:
    max_red,  max_green, max_blue = 12, 13, 14

    S = 0
    for line in input:
        game = line.split(': ')
        _, game_id = game[0].split()
        game_id = int(game_id)
        rounds = game[1].split('; ')
        impossible = False

        for r in rounds:
            if impossible:
                break
            for x in r.split(', '):
                nr, color = x.split(' ')
                nr = int(nr)
                if color == 'red' and nr > max_red:
                    impossible = True
                    break
                if color == 'green' and nr > max_green:
                    impossible = True
                    break
                if color == 'blue' and nr > max_blue:
                    impossible = True
                    break

        if not impossible:
            S += game_id
    return S


def part_2(input) -> int:
    S = 0
    for line in input:
        game = line.split(': ')
        _, game_id = game[0].split()
        rounds = game[1].split('; ')

        max_red = max_green = max_blue = 0

        for r in rounds:
            for x in r.split(', '):
                nr, color = x.split(' ')
                nr = int(nr)
                if color == 'red':
                    max_red = max(max_red, nr)
                if color == 'green':
                    max_green = max(max_green, nr)
                if color == 'blue':
                    max_blue = max(max_blue, nr)

        S += (max_red * max_green * max_blue)
    return S


def read_input_file(filename: str):
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file("input_day_2.txt")

    print(f"Part 1: {part_1(input_str)}")
    print(f"Part 2: {part_2(input_str)}")