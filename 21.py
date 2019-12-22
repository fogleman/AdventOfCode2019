import fileinput
import intcode

def run(script):
    return list(intcode.run(program, script))[-1]

program = list(fileinput.input())[0]

script = '''
OR C J
AND A J
AND B J
NOT J J
AND D J
WALK
'''.lstrip()

print(run(script))

script = '''
NOT H J
OR C J
AND A J
AND B J
NOT J J
AND D J
RUN
'''.lstrip()

print(run(script))
