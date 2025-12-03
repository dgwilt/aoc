#!/usr/bin/env python3 
from itertools import permutations

Finished = -1

data = [[],"3,8,1001,8,10,8,105,1,0,0,21,42,55,64,85,98,179,260,341,422,99999,3,9,101,2,9,9,102,5,9,9,1001,9,2,9,1002,9,5,9,4,9,99,3,9,1001,9,5,9,1002,9,4,9,4,9,99,3,9,101,3,9,9,4,9,99,3,9,1002,9,4,9,101,3,9,9,102,5,9,9,101,4,9,9,4,9,99,3,9,1002,9,3,9,1001,9,3,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99"]

tests = [
    [[9,8,7,6,5],"3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"],
    [[9,7,8,5,6],"3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"]
]

def args_with_dest(pc,prog,modes,nargs):
    return args(pc,prog,modes,nargs,dest_last=True)

def args(pc,prog,modes,nargs,dest_last=False):
    ops = [None] * nargs
    for i in range(nargs):
        modes,m = divmod(modes,10)
        imm = prog[pc+i]
        op = imm if m == 1 else prog[imm]
        ops[i] = imm if dest_last and i == nargs-1 else op
    return ops

def add(pc,prog,modes,inputs,outputs):
    op1,op2,op3 = args_with_dest(pc,prog,modes,3)
    prog[op3] = op1 + op2
    return pc+3

def mul(pc,prog,modes,inputs,outputs):
    op1,op2,op3 = args_with_dest(pc,prog,modes,3)
    prog[op3] = op1 * op2
    return pc+3

def inp(pc,prog,modes,inputs,outputs):
    op1 = prog[pc]
    prog[op1] = inputs.pop(0)
    return pc+1

def out(pc,prog,modes,inputs,outputs):
    op1 = args(pc,prog,modes,1)
    outputs.append(*op1)
    return pc+1

def jit(pc,prog,modes,inputs,outputs):
    op1,op2 = args(pc,prog,modes,2)
    return op2 if op1 != 0 else pc+2

def jif(pc,prog,modes,inputs,outputs):
    op1,op2 = args(pc,prog,modes,2)
    return op2 if op1 == 0 else pc+2

def lt(pc,prog,modes,inputs,outputs):
    op1,op2,op3 = args_with_dest(pc,prog,modes,3)
    prog[op3] = 1 if op1 < op2 else 0
    return pc+3

def eq(pc,prog,modes,inputs,outputs):
    op1,op2,op3 = args_with_dest(pc,prog,modes,3)
    prog[op3] = 1 if op1 == op2 else 0
    return pc+3

def intcode(prog,pc,inputs,outputs):
    execute = {
        1 : add,
        2 : mul,
        3 : inp,
        4 : out,
        5 : jit,
        6 : jif,
        7 : lt,
        8 : eq
    }
    while True:
        modes,opcode = divmod(prog[pc],100)
        if opcode == 99: return Finished
        elif opcode == 3 and len(inputs) == 0: return pc
        pc = execute[opcode](pc+1,prog,modes,inputs,outputs)

def runphase(code,phase):
    amps = len(phase)
    pcs = [0] * amps
    progs = [[int(i) for i in code.split(",")] for _ in range(amps)]
    inputs = [[phase[i]] for i in range(amps)]
    inputs[0].append(0)
    while pcs[-1] != Finished:
        for i in range(amps): pcs[i] = intcode(progs[i],pcs[i],inputs[i],inputs[(i+1)%amps])
    return inputs[0][0]

def run(data,testing=False):
    if testing: return runphase(data[1],data[0])
    else: return max(runphase(data[1],phase) for phase in permutations(range(5,10),5))
    
for test in [t for t in tests if t]:
    try: print(run(test,testing=True))
    except Exception as e: 
        print(f"Error: {e}")
        
print(run(data))
