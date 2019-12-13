from collections import defaultdict

def run(program, program_input=None):
    ip = rb = 0
    if isinstance(program, str):
        program = map(int, program.split(','))
    mem = defaultdict(int, enumerate(program))
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

def disassemble(program):
    sizes = dict(enumerate([1, 4, 4, 2, 2, 3, 3, 4, 4, 2]))
    names = {
        1: 'ADD', 2: 'MUL', 3: 'IN', 4: 'OUT',
        5: 'JNZ', 6: 'JZ', 7: 'LT', 8: 'EQ',
        9: 'RB', 99: 'HALT',
    }
    if isinstance(program, str):
        program = list(map(int, program.split(',')))
    i = 0
    while i < len(program):
        op = program[i] % 100
        size = sizes.get(op, 1)
        name = names.get(op, '?')
        args = [program[i + j] for j in range(1, size)]
        modes = [(program[i] // 10 ** j) % 10 for j in range(2, 5)]
        tokens = [name]
        for arg, mode in zip(args, modes):
            if mode == 0:
                tokens.append('%d' % arg)
            elif mode == 1:
                tokens.append('#%d' % arg)
            elif mode == 2:
                tokens.append('[%d]' % arg)
        print('%04d' % i, '%6d' % program[i], ' '.join(tokens))
        i += size

if __name__ == '__main__':
    import fileinput
    disassemble(list(fileinput.input())[0])
