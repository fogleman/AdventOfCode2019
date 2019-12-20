import fileinput
import intcode

program = list(map(int, list(fileinput.input())[0].split(',')))

def test(x, y):
    return list(intcode.run(program, [x, y]))[0]

def part1():
    return sum(test(x, y) for y in range(50) for x in range(50))

def part2():
    px = py = 0
    while True:
        y = py + 1
        for x in range(px - 3, px + 4):
            if test(x, y):
                if test(x + 99, y - 99):
                    return x * 10000 + y - 99
                break
        px, py = x, y

print(part1())
print(part2())
