import fileinput

def run(line, a, b):
    program = list(map(int, line.split(',')))
    program[1] = a
    program[2] = b
    i = 0
    while True:
        op, a, b, c = program[i:i+4]
        if op == 99:
            return program[0]
        if op == 1:
            program[c] = program[a] + program[b]
        if op == 2:
            program[c] = program[a] * program[b]
        i += 4

line = list(fileinput.input())[0]

print(run(line, 12, 2))

for a in range(100):
    for b in range(100):
        c = run(line, a, b)
        if c == 19690720:
            print(100 * a + b)
