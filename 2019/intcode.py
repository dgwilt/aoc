#!/usr/bin/env python3 
from collections import defaultdict

class Intcode:

    Finished = -1
    Waiting = -2
    Other = -3

    def __init__(self):
        self.pc = 0
        self.base = 0
        self.inputs = []
        self.outputs = []
        self.prog = defaultdict(int)
        self.__status = Intcode.Other

    @property
    def status(self):
        return self.__status

    def program(self,data):
        for addr,i in enumerate(data.split(",")): self.prog[addr] = int(i)
        return self

    def provide_ascii(self,text):
        return self.provide_input(*[ord(c) for c in text])

    def provide_input(self,*args):
        for i in args:
            self.inputs.append(i)
        return self

    def poke(self,addr,data):
        self.prog[addr] = data
        return self
        
    def peek_outputs(self):
        return self.outputs

    def pop_outputs(self):
        o = self.outputs[:]
        self.outputs = []
        return o

    def args(self,modes,nargs,dest_last=False):
        ops = [None] * nargs
        for i in range(nargs):
            modes,m = divmod(modes,10)
            imm = self.prog[self.pc+i]
            if m == 1: op = imm
            elif m == 0: op = self.prog[imm]
            elif m == 2: op = self.prog[self.base+imm]
            if dest_last and i == nargs-1:
                if m == 2: ops[i] = self.base+imm
                else: ops[i] = imm
            else: ops[i] = op
        if nargs == 1: return ops[0]
        else: return ops

    def args_with_dest(self,modes,nargs):
        return self.args(modes,nargs,dest_last=True)

    def add(self,modes):
        nargs = 3
        op1,op2,op3 = self.args_with_dest(modes,nargs)
        self.prog[op3] = op1 + op2
        self.pc += nargs

    def mul(self,modes):
        nargs = 3
        op1,op2,op3 = self.args_with_dest(modes,nargs)
        self.prog[op3] = op1 * op2
        self.pc += nargs

    def inp(self,modes):
        nargs = 1
        op1 = self.args_with_dest(modes,nargs)
        self.prog[op1] = self.inputs.pop(0)
        self.pc += nargs

    def out(self,modes):
        nargs = 1
        op1 = self.args(modes,nargs)
        self.outputs.append(op1)
        self.pc += nargs

    def jit(self,modes):
        nargs = 2
        op1,op2 = self.args(modes,nargs)
        self.pc = op2 if op1 != 0 else self.pc+nargs

    def jif(self,modes):
        nargs = 2
        op1,op2 = self.args(modes,nargs)
        self.pc = op2 if op1 == 0 else self.pc+nargs

    def lt(self,modes):
        nargs = 3
        op1,op2,op3 = self.args_with_dest(modes,nargs)
        self.prog[op3] = 1 if op1 < op2 else 0
        self.pc += nargs

    def eq(self,modes):
        nargs = 3
        op1,op2,op3 = self.args_with_dest(modes,nargs)
        self.prog[op3] = 1 if op1 == op2 else 0
        self.pc += nargs

    def bas(self,modes):
        nargs = 1
        op1 = self.args(modes,nargs)
        self.base += op1
        self.pc += nargs

    def execute(self):
        decode = {
            1 : self.add,
            2 : self.mul,
            3 : self.inp,
            4 : self.out,
            5 : self.jit,
            6 : self.jif,
            7 : self.lt,
            8 : self.eq,
            9 : self.bas
        }
        while True:
            modes,opcode = divmod(self.prog[self.pc],100)
            if opcode == 99:
                self.__status = Intcode.Finished
                return self
            elif opcode == 3 and len(self.inputs) == 0: 
                self.__status = Intcode.Waiting
                return self
            self.pc += 1
            decode[opcode](modes)
