#!/usr/bin/env python3 
from itertools import permutations

data = [[],"3,8,1001,8,10,8,105,1,0,0,21,42,55,64,85,98,179,260,341,422,99999,3,9,101,2,9,9,102,5,9,9,1001,9,2,9,1002,9,5,9,4,9,99,3,9,1001,9,5,9,1002,9,4,9,4,9,99,3,9,101,3,9,9,4,9,99,3,9,1002,9,4,9,101,3,9,9,102,5,9,9,101,4,9,9,4,9,99,3,9,1002,9,3,9,1001,9,3,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99"]

tests = [
    [[4,3,2,1,0],"3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"],
    [[0,1,2,3,4],"3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"]
]

def args_with_dest(pc,prog,modes,nargs):
    return args(pc,prog,modes,nargs,dest_last=True)

def args(pc,prog,modes,nargs,dest_last=False):
    ops = []
    for i in range(nargs):
        modes,m = divmod(modes,10)
        imm = prog[pc+i]
        op = imm if m == 1 else prog[imm]
        ops.append(imm if dest_last and i == nargs-1 else op)
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
        if opcode == 99: return pc
        pc = execute[opcode](pc+1,prog,modes,inputs,outputs)

def runphase(code,phase):
    amps = len(phase)
    pc = 0
    inputs = [0]
    for i in range(amps): intcode([int(i) for i in code.split(",")],pc,[phase[i],inputs.pop(0)],inputs)
    return inputs[0]

def run(data,testing=False):
    if testing: return runphase(data[1],data[0])
    else: return max(runphase(data[1],phase) for phase in permutations(range(5),5))
    
for test in [t for t in tests if t]:
    try: print(run(test,testing=True))
    except Exception as e: 
        print(f"Error: {e}")
        
print(run(data))
