#!/usr/local/bin/python3

data = '''cpy 1 a
cpy 1 b
cpy 26 d
jnz c 2
jnz 1 5
cpy 7 c
inc d
dec c
jnz c -2
cpy a c
inc a
dec b
jnz b -2
cpy c b
dec d
jnz d -6
cpy 14 c
cpy 14 d
inc a
dec d
jnz d -2
dec c
jnz c -5'''

def reg_to_x(reg):
	return ord(reg) - ord('a')

class Instruction:
	def __init__(self,asm):
		opc = asm.split(" ")
		if opc[0] == "cpy":
			n = opc[1]
			rd = reg_to_x(opc[2])
			if n.isdigit():
				n = int(n)
				self.run = lambda pc, regs : (pc + 1,[n if r == rd else v for r,v in enumerate(regs)])
			else:
				rs = reg_to_x(n)
				self.run = lambda pc, regs : (pc + 1,[regs[rs] if r == rd else v for r,v in enumerate(regs)])

		elif opc[0] == "jnz":
			r = opc[1]
			d = int(opc[2])
			if r.isdigit():
				r = int(r)
				if r == 0:
					self.run = lambda pc, regs : (pc + 1,regs)
				else:
					self.run = lambda pc, regs : (pc + d,regs)
			else:
				rs = reg_to_x(r)
				self.run = lambda pc, regs : (pc + (1 if regs[rs] == 0 else d),regs)

		elif opc[0] == "dec": 
			rd = reg_to_x(opc[1])
			self.run = lambda pc, regs : (pc + 1,[v-1 if r == rd else v for r,v in enumerate(regs)])

		elif opc[0] == "inc": 
			rd = reg_to_x(opc[1])
			self.run = lambda pc, regs : (pc + 1,[v+1 if r == rd else v for r,v in enumerate(regs)])

def run(program,regs):
	pc = 0
	maxpc = len(program)
	while pc < maxpc:
		pc,regs = program[pc].run(pc,regs)
	return regs[0]

program = [Instruction(asm) for asm in data.splitlines()]

print(run(program,[0,0,0,0]))
print(run(program,[0,0,1,0]))
