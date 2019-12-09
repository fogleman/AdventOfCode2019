import fileinput

from collections import defaultdict

def run(program, program_input):
    sizes = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2]
    mem = defaultdict(int, enumerate(map(int, program.split(','))))
    ip = rb = 0
    while True:
        op = mem[ip] % 100
        if op == 99:
            return
        args = [mem[ip+i] for i in range(1, sizes[op])]
        modes = [(mem[ip] // 10 ** i) % 10 for i in range(2, 5)]
        reads = [(mem[x], x, mem[x+rb])[m] for x, m in zip(args, modes)]
        writes = [(x, None, x+rb)[m] for x, m in zip(args, modes)]
        ip += sizes[op]
        if op == 1:
            mem[writes[2]] = reads[0] + reads[1]
        elif op == 2:
            mem[writes[2]] = reads[0] * reads[1]
        elif op == 3:
            mem[writes[0]] = program_input.pop(0)
        elif op == 4:
            yield reads[0]
        elif op == 5:
            if reads[0]:
                ip = reads[1]
        elif op == 6:
            if not reads[0]:
                ip = reads[1]
        elif op == 7:
            mem[writes[2]] = int(reads[0] < reads[1])
        elif op == 8:
            mem[writes[2]] = int(reads[0] == reads[1])
        elif op == 9:
            rb += reads[0]

program = list(fileinput.input())[0]
print(list(run(program, [1])))
print(list(run(program, [2])))
