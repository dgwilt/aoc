#!/usr/local/bin/python3

no_output = -1

# Some suitable re-writing of the assembunny code for optimization and a new 'djg' instruction

data='''add d a 2541
cpy d a
djg a a c
sub b 2 c
out b
jnz a -3
jnz 1 -5'''

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
				self.run = lambda pc, regs : (pc + 1,regs,no_output)
			else:
				n = opc[1]
				rd = reg_to_x(opc[2])
				if isint(n):
					n = int(n)
					self.run = lambda pc, regs : (pc + 1,[n if r == rd else v for r,v in enumerate(regs)],no_output)
				else:
					rs = reg_to_x(n)
					self.run = lambda pc, regs : (pc + 1,[regs[rs] if r == rd else v for r,v in enumerate(regs)],no_output)

		elif opc[0] == "jnz":
			r = opc[1]
			if isint(opc[2]):
				d = int(opc[2])
				if isint(r):
					r = int(r)
					if r == 0:
						self.run = lambda pc, regs : (pc + 1,regs,no_output)
					else:
						self.run = lambda pc, regs : (pc + d,regs,no_output)
				else:
					rs = reg_to_x(r)
					self.run = lambda pc, regs : (pc + (1 if regs[rs] == 0 else d),regs,no_output)
			else:
				rd = reg_to_x(opc[2])
				if isint(r):
					r = int(r)
					if r == 0:
						self.run = lambda pc, regs : (pc + 1,regs,no_output)
					else:
						self.run = lambda pc, regs : (pc + regs[rd],regs,no_output)
				else:
					rs = reg_to_x(r)
					self.run = lambda pc, regs : (pc + (1 if regs[rs] == 0 else regs[rd]),regs,no_output)

		elif opc[0] == "dec": 
			rd = reg_to_x(opc[1])
			self.run = lambda pc, regs : (pc + 1,[v-1 if r == rd else v for r,v in enumerate(regs)],no_output)

		elif opc[0] == "inc": 
			rd = reg_to_x(opc[1])
			self.run = lambda pc, regs : (pc + 1,[v+1 if r == rd else v for r,v in enumerate(regs)],no_output)

		elif opc[0] == "out": 
			rd = reg_to_x(opc[1])
			self.run = lambda pc, regs : (pc + 1,regs,regs[rd])

		elif opc[0] == "djg": 
			ra = reg_to_x(opc[1])
			rb = reg_to_x(opc[2])
			rc = reg_to_x(opc[3])
			self.run = lambda pc, regs : (pc + 1,[regs[rb]//2 if r == ra else 2-(regs[rb]%2) if r == rc else v for r,v in enumerate(regs)],no_output)

		elif opc[0] == "add": 
			rd = reg_to_x(opc[1])
			ra = reg_to_x(opc[2])
			if isint(opc[3]):
				b = int(opc[3])
				self.run = lambda pc, regs : (pc + 1,[regs[ra]+b if r == rd else v for r,v in enumerate(regs)],no_output)
			else:
				rb = reg_to_x(opc[3])
				self.run = lambda pc, regs : (pc + 1,[regs[ra]+regs[rb] if r == rd else v for r,v in enumerate(regs)],no_output)

		elif opc[0] == "sub": 
			rd = reg_to_x(opc[1])
			if isint(opc[2]):
				a = int(opc[2])
				rb = reg_to_x(opc[3])
				self.run = lambda pc, regs : (pc + 1,[a-regs[rb] if r == rd else v for r,v in enumerate(regs)],no_output)
			else:
				ra = reg_to_x(opc[2])
				if isint(opc[3]):
					b = int(opc[3])
					self.run = lambda pc, regs : (pc + 1,[regs[ra]-b if r == rd else v for r,v in enumerate(regs)],no_output)
				else:
					rb = reg_to_x(opc[3])
					self.run = lambda pc, regs : (pc + 1,[regs[ra]-regs[rb] if r == rd else v for r,v in enumerate(regs)],no_output)

def check_output(program,regs):
	pc = 0
	noof_prints = 0
	lastout = None
	sequence_check_length = 9
	while noof_prints < sequence_check_length:
		pc,regs,out = program[pc].run(pc,regs)

		if out >= 0:			
			if lastout is not None:
				if out == lastout:
					return False
			lastout = out
			noof_prints += 1
	return True

def run():
	program = [Instruction(a) for a in data.splitlines()]
	a = 0
	while True:
		if check_output(program,[a,0,0,0]):
			return a
		a += 1

print(run())
