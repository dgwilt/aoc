#!/usr/local/bin/python3

'''
The trick (hinted at in the puzzle) is to re-write the first part of the 
assembly code and introduce a multiply instruction.  Cannot replace the 
pseudo-multiply loop after the tgl, however, as it gets modified by the tgl.  
Also need to adjust the backwards branch from -16 instructions to -9 instructions.
'''

data = '''cpy a b
dec b
cpy a d
cpy 0 a
mul a b d
dec b
mul c b 2
tgl c
cpy -7 c
jnz 1 c
cpy 87 c
jnz 74 d
inc a
inc d
jnz d -2
inc c
jnz c -5'''

def isint(s):
	try:
	    a = int(s)
	    return True
	except ValueError:
		return False

def reg_to_x(reg):
	return ord(reg) - ord('a')

class Instruction:
	def __init__(self,asm):
		opc = asm.split(" ")
		if opc[0] == "cpy":
			if isint(opc[2]):
				# Nop
				self.run = lambda pc, regs : (pc + 1,regs,-1)
			else:
				n = opc[1]
				rd = reg_to_x(opc[2])
				if isint(n):
					n = int(n)
					self.run = lambda pc, regs : (pc + 1,[n if r == rd else v for r,v in enumerate(regs)],-1)
				else:
					rs = reg_to_x(n)
					self.run = lambda pc, regs : (pc + 1,[regs[rs] if r == rd else v for r,v in enumerate(regs)],-1)

		elif opc[0] == "jnz":
			r = opc[1]
			if isint(opc[2]):
				d = int(opc[2])
				if isint(r):
					r = int(r)
					if r == 0:
						self.run = lambda pc, regs : (pc + 1,regs,-1)
					else:
						self.run = lambda pc, regs : (pc + d,regs,-1)
				else:
					rs = reg_to_x(r)
					self.run = lambda pc, regs : (pc + (1 if regs[rs] == 0 else d),regs,-1)
			else:
				rd = reg_to_x(opc[2])
				if isint(r):
					r = int(r)
					if r == 0:
						self.run = lambda pc, regs : (pc + 1,regs,-1)
					else:
						self.run = lambda pc, regs : (pc + regs[rd],regs,-1)
				else:
					rs = reg_to_x(r)
					self.run = lambda pc, regs : (pc + (1 if regs[rs] == 0 else regs[rd]),regs,-1)

		elif opc[0] == "dec": 
			rd = reg_to_x(opc[1])
			self.run = lambda pc, regs : (pc + 1,[v-1 if r == rd else v for r,v in enumerate(regs)],-1)

		elif opc[0] == "inc": 
			rd = reg_to_x(opc[1])
			self.run = lambda pc, regs : (pc + 1,[v+1 if r == rd else v for r,v in enumerate(regs)],-1)

		elif opc[0] == "tgl": 
			rd = reg_to_x(opc[1])
			self.run = lambda pc, regs : (pc + 1,regs,pc+regs[rd])

		elif opc[0] == "mul": 
			rd = reg_to_x(opc[1])
			ra = reg_to_x(opc[2])
			if isint(opc[3]):
				b = int(opc[3])
				self.run = lambda pc, regs : (pc + 1,[regs[ra]*b if r == rd else v for r,v in enumerate(regs)],-1)
			else:
				rb = reg_to_x(opc[3])
				self.run = lambda pc, regs : (pc + 1,[regs[ra]*regs[rb] if r == rd else v for r,v in enumerate(regs)],-1)

def toggle(asm):
	asm = asm.replace("inc","DEC")
	asm = asm.replace("dec","INC")
	asm = asm.replace("tgl","INC")
	asm = asm.replace("jnz","CPY")
	asm = asm.replace("cpy","JNZ")
	return asm.lower()

def run(asm,regs):
	program = [Instruction(a) for a in asm]
	pc = 0
	maxpc = len(program)
	while pc < maxpc:
		pc,regs,tpc = program[pc].run(pc,regs)
		if 0 <= tpc < maxpc:
			asm[tpc] = toggle(asm[tpc])
			program[tpc] = Instruction(asm[tpc])
	return regs[0]

asm = data.splitlines()
print(run(asm,[7,0,0,0]))

asm = data.splitlines()
print(run(asm,[12,0,0,0]))
