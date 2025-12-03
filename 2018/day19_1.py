from re import search

data = """#ip 4
addi 4 16 4
seti 1 2 5
seti 1 1 1
mulr 5 1 2
eqrr 2 3 2
addr 2 4 4
addi 4 1 4
addr 5 0 0
addi 1 1 1
gtrr 1 3 2
addr 4 2 4
seti 2 4 4
addi 5 1 5
gtrr 5 3 2
addr 2 4 4
seti 1 8 4
mulr 4 4 4
addi 3 2 3
mulr 3 3 3
mulr 4 3 3
muli 3 11 3
addi 2 4 2
mulr 2 4 2
addi 2 6 2
addr 3 2 3
addr 4 0 4
seti 0 8 4
setr 4 1 2
mulr 2 4 2
addr 4 2 2
mulr 4 2 2
muli 2 14 2
mulr 2 4 2
addr 3 2 3
seti 0 0 0
seti 0 0 4"""

tests = ["""#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""]

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
        address = regs[ip]
        instruction = code[address]
        execute(regs,*instruction)
        nextip = regs[ip] + 1
        if nextip >= len(code):
            break
        regs[ip] = nextip

    return regs[0]

for test in [t for t in tests if t]:
    break
    try: print(run(test))
    except Exception as e: print("Error:",e)

print(run(data))
