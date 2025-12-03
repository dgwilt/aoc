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

regs = [0]*4
regs[2] = 1

def reg_to_x(reg):
	return ord(reg) - ord('a')

inst = data.split("\n")
pc = 0

while pc < len(inst):
	i = inst[pc]
	opc = i.split(" ")
	if opc[0] == "cpy":
		n = opc[1]
		if n.isdigit():
			n = int(n)
		else:
			n = regs[reg_to_x(n)]
		r = reg_to_x(opc[2])
		regs[r] = n
		pc += 1
	elif opc[0] == "jnz":
		r = opc[1]
		if r.isdigit():
			val = int(r)
		else:
			val = regs[reg_to_x(r)]
		if val != 0:
			pc += int(opc[2])
		else:
			pc += 1
	elif opc[0] == "dec": 
		r = reg_to_x(opc[1])
		regs[r] -= 1
		pc += 1
	elif opc[0] == "inc": 
		r = reg_to_x(opc[1])
		regs[r] += 1
		pc += 1

print(regs[0])
