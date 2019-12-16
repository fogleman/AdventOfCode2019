import fileinput

def run(program, program_input):
    instruction_sizes = [0, 4, 4, 2, 2, 3, 3, 4, 4]
    program = list(map(int, program.split(',')))
    program_output = []
    ip = 0
    while True:
        op = program[ip]
        modes = [(op // 10 ** i) % 10 for i in range(2, 5)]
        op = op % 100
        if op == 99:
            return program_output
        size = instruction_sizes[op]
        args = [program[ip + i] for i in range(1, size)]
        params = [x if modes[i] else program[x]
            for i, x in enumerate(args)]
        ip += size
        if op == 1:
            program[args[2]] = params[0] + params[1]
        elif op == 2:
            program[args[2]] = params[0] * params[1]
        elif op == 3:
            program[args[0]] = program_input.pop(0)
        elif op == 4:
            program_output.append(params[0])
        elif op == 5:
            if params[0]:
                ip = params[1]
        elif op == 6:
            if not params[0]:
                ip = params[1]
        elif op == 7:
            program[args[2]] = int(params[0] < params[1])
        elif op == 8:
            program[args[2]] = int(params[0] == params[1])

program = list(fileinput.input())[0]
print(run(program, [1]))
print(run(program, [5]))
