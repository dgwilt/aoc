#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay

class AocDay17(AocDay):
    RA = 4
    RB = 5
    RC = 6

    combo = lambda op,regs: regs.get(op,op)

    def adv(op,regs,pc,_):
        regs[AocDay17.RA] = regs[AocDay17.RA] >> AocDay17.combo(op,regs)
        return pc + 2

    def bxl(op,regs,pc,_):
        regs[AocDay17.RB] = regs[AocDay17.RB] ^ op
        return pc + 2

    def bst(op,regs,pc,_):
        regs[AocDay17.RB] = AocDay17.combo(op,regs) & 7
        return pc + 2

    def jnz(op,regs,pc,_):
        return pc + 2 if regs[AocDay17.RA] == 0 else op

    def bxc(op,regs,pc,_):
        regs[AocDay17.RB] = regs[AocDay17.RB] ^ regs[AocDay17.RC]
        return pc + 2

    def out(op,regs,pc,out):
        out.append(AocDay17.combo(op,regs) & 7)
        return pc + 2

    def bdv(op,regs,pc,_):
        regs[AocDay17.RB] = regs[AocDay17.RA] >> AocDay17.combo(op,regs)
        return pc + 2

    def cdv(op,regs,pc,_):
        regs[AocDay17.RC] = regs[AocDay17.RA] >> AocDay17.combo(op,regs)
        return pc + 2

    def run_prog(regs,prog):
        pc, out = 0, []
        decode = {0:AocDay17.adv,
                  1:AocDay17.bxl,
                  2:AocDay17.bst,
                  3:AocDay17.jnz,
                  4:AocDay17.bxc,
                  5:AocDay17.out,
                  6:AocDay17.bdv,
                  7:AocDay17.cdv}
        while pc < len(prog):
            # Fetch
            opcode,operand = prog[pc:pc+2]
            # Decode
            inst = decode[opcode]
            # Execute
            pc = inst(operand,regs,pc,out)
        return out

    def parser(self,data):
        regs,prog = data.split("\n\n")
        regs = {r:int(line.split(": ")[1]) for r,line in enumerate(regs.splitlines(),start=AocDay17.RA)}
        prog = [int(i) for i in prog.split(": ")[1].split(",")]
        return prog,regs

    def run_silver(self,data):
        prog,regs = self.parser(data)
        out = AocDay17.run_prog(regs,prog)
        return ",".join(str(i) for i in out)
    
    """
My Program is:
--------------
RB = RA & 7
RB = RB ^ 5  <--+-- Assume these numbers are different for other people
RC = RA >> RB   |
RB = RB ^ 6  <--+
RB = RB ^ RC
PRINT RB & 7
RA = RA >> 3
LOOP TO START IF A != 0

out = ((RA & 7) ^ 5 ^ 6 ^ (RA >> ((RA & 7) ^ 5))) & 7
    """
    # Doing the heavy lifting here!
    output = lambda ra: ((rb := ((ra & 7) ^ 5)) ^ 6 ^ (ra >> rb)) & 7

    def run_gold(self,data):
        prog,regs = self.parser(data)
        ras = [0]
        for op in reversed(prog):
            ras = [nxt_ra for ra in ras for lsb in range(8) if op == AocDay17.output(nxt_ra := (ra*8 + lsb))]
        regs[AocDay17.RA] = (ra := min(ras))
        assert(prog == AocDay17.run_prog(regs,prog))
        return ra
    
if __name__ == "__main__":

    silver_tests = ["""Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""",""""""]

    gold_tests = ["""Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0""",""""""]

    data = """Register A: 47792830
Register B: 0
Register C: 0

Program: 2,4,1,5,7,5,1,6,4,3,5,5,0,3,3,0"""

    answer = AocDay17(data,silver_tests,gold_tests,argv)

    print(answer)
