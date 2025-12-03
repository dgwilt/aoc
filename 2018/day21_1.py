from re import search
from enum import Enum, auto

data = """#ip 2
seti 123 0 3
bani 3 456 3
eqri 3 72 3
addr 3 2 2
seti 0 0 2
seti 0 6 3
bori 3 65536 4
seti 7041048 8 3
bani 4 255 5
addr 3 5 3
bani 3 16777215 3
muli 3 65899 3
bani 3 16777215 3
gtir 256 4 5
addr 5 2 2
addi 2 1 2
seti 27 6 2
seti 0 1 5
addi 5 1 1
muli 1 256 1
gtrr 1 4 1
addr 1 2 2
addi 2 1 2
seti 25 1 2
addi 5 1 5
seti 17 8 2
setr 5 2 4
seti 7 9 2
eqrr 3 0 5
addr 5 2 2
seti 5 3 2"""

def execute(regs,o,a,b,c):
    if o   == "addr": regs[c] = regs[a] + regs[b]
    elif o == "addi": regs[c] = regs[a] + b
    elif o == "mulr": regs[c] = regs[a] * regs[b]
    elif o == "muli": regs[c] = regs[a] * b
    elif o == "banr": regs[c] = regs[a] & regs[b]
    elif o == "bani": regs[c] = regs[a] & b
    elif o == "borr": regs[c] = regs[a] | regs[b]
    elif o == "bori": regs[c] = regs[a] | b
    elif o == "setr": regs[c] = regs[a]
    elif o == "seti": regs[c] = a
    elif o == "gtir": regs[c] = 1 if a > regs[b] else 0
    elif o == "gtri": regs[c] = 1 if regs[a] > b else 0
    elif o == "gtrr": regs[c] = 1 if regs[a] > regs[b] else 0
    elif o == "eqir": regs[c] = 1 if a == regs[b] else 0
    elif o == "eqri": regs[c] = 1 if regs[a] == b else 0
    elif o == "eqrr": regs[c] = 1 if regs[a] == regs[b] else 0

def run(data):
    ip = int(search(r'#ip\s+(\d+)',data).group(1))
    code = []
    for line in data.splitlines()[1:]:
        o,a,b,c = search(r'(\w+) (\d+) (\d+) (\d+)',line).group(1,2,3,4)
        a,b,c = [int(i) for i in [a,b,c]]
        code.append((o,a,b,c))

    regs = [0]*6
    while True:
        print(regs)
        address = regs[ip]
        if address == 28:
            return regs[3]
        instruction = code[address]
        execute(regs,*instruction)
        nextip = regs[ip] + 1
        if nextip >= len(code):
            break
        regs[ip] = nextip
    
print(run(data))
