import fileinput

from collections import defaultdict

def run(program, program_input):
    ip = rb = 0
    mem = defaultdict(int, enumerate(map(int, program.split(','))))
    while True:
        op = mem[ip] % 100
        if op == 99:
            return
        size = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2][op]
        args = [mem[ip+i] for i in range(1, size)]
        modes = [(mem[ip] // 10 ** i) % 10 for i in range(2, 5)]
        reads = [(mem[x], x, mem[x+rb])[m] for x, m in zip(args, modes)]
        writes = [(x, None, x+rb)[m] for x, m in zip(args, modes)]
        ip += size
        if op == 1:
            mem[writes[2]] = reads[0] + reads[1]
        if op == 2:
            mem[writes[2]] = reads[0] * reads[1]
        if op == 3:
            mem[writes[0]] = program_input.pop(0)
        if op == 4:
            yield reads[0]
        if op == 5 and reads[0]:
            ip = reads[1]
        if op == 6 and not reads[0]:
            ip = reads[1]
        if op == 7:
            mem[writes[2]] = int(reads[0] < reads[1])
        if op == 8:
            mem[writes[2]] = int(reads[0] == reads[1])
        if op == 9:
            rb += reads[0]

program = list(fileinput.input())[0]
print(list(run(program, [1])))
print(list(run(program, [2])))
