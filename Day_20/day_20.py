
def parse_file():
    flipflops = {}
    conjunctions = {}
    broadcaster = []

    for line in open("input_day_20.txt").readlines():
        line = line.strip()
        type_ = line[0]
        key, values = line[1:].split(" -> ")
        values = values.split(", ")
        if type_ == "%":
            flipflops[key] = [values, False]
        elif type_ == "&":
            conjunctions[key] = (values, {})
        else:
            broadcaster = values
    return flipflops, conjunctions, broadcaster

def part1():
    nhighs = 0
    nlows = 0
    # reset all inputs of conjunctions
    for y in flipflops:
        for x in flipflops[y][0]:
            if x in conjunctions:
                conjunctions[x][1][y] = False
    for y in conjunctions:
        for x in conjunctions[y][0]:
            if x in conjunctions:
                conjunctions[x][1][y] = False
    for _ in range(1000):
        Q = [("broadcaster", x, False) for x in broadcaster]
        nlows += 1
        #print()
        while Q:
            src, dst, value = Q.pop(0)
            #print(f"{src} {'-high' if value else '-low'}-> {dst}")

            if value:
                nhighs += 1
            else:
                nlows += 1

            if dst in flipflops:
                if not value: # flip flop ignores high pulse
                    flipflops[dst][1] = not flipflops[dst][1] # flip and remember state
                    for x in flipflops[dst][0]:
                        Q.append((dst, x, flipflops[dst][1]))
            elif dst in conjunctions:
                conjunctions[dst][1][src] = value # set state for specific input
                for x in conjunctions[dst][0]:
                    Q.append((dst, x, not all(conjunctions[dst][1].values()))) # if high on all inputs send low, send high otherwise

    print(nhighs*nlows)

flipflops, conjunctions, broadcaster = parse_file()
part1()


# PART 2
import math

def parse_file():
    flipflops = {}
    conjunctions = {}
    broadcaster = []

    for line in open("input_day_20.txt").readlines():
        line = line.strip()
        type_ = line[0]
        key, values = line[1:].split(" -> ")
        values = values.split(", ")
        if type_ == "%":
            flipflops[key] = [values, False]
        elif type_ == "&":
            conjunctions[key] = (values, {})
        else:
            broadcaster = values
    return flipflops, conjunctions, broadcaster

def part2():
    cycles = { 'pv': 0, 'qh': 0, 'xm': 0, 'hz': 0 }

    # reset all inputs of conjunctions
    for y in flipflops:
        for x in flipflops[y][0]:
            if x in conjunctions:
                conjunctions[x][1][y] = False
    for y in conjunctions:
        for x in conjunctions[y][0]:
            if x in conjunctions:
                conjunctions[x][1][y] = False
    for i in range(1,20000):
        Q = [("broadcaster", x, False) for x in broadcaster]
        #print()
        while Q:
            src, dst, value = Q.pop(0)
            #print(f"{src} {'-high' if value else '-low'}-> {dst}")

            if dst in flipflops:
                if not value: # flip flop ignores high pulse
                    flipflops[dst][1] = not flipflops[dst][1] # flip and remember state
                    for x in flipflops[dst][0]:
                        Q.append((dst, x, flipflops[dst][1]))
            elif dst in conjunctions:
                if dst == 'kh':
                    print(math.lcm(*cycles.values()))
                    if value == True:
                        print(f"{src} {i}")
                        cycles[src] = i
                        print(math.lcm(*cycles.values()))
                    if all(x > 0 for x in cycles.values()):
                        print(math.lcm(*cycles.values()))
                        return
                conjunctions[dst][1][src] = value # set state for specific input
                for x in conjunctions[dst][0]:
                    Q.append((dst, x, not all(conjunctions[dst][1].values()))) # if high on all inputs send low, send high otherwise


flipflops, conjunctions, broadcaster = parse_file()
part2()