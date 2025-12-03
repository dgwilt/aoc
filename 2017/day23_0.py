from collections import defaultdict

data = """set b 57
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1
set d 2
set e 2
set g d
mul g e
sub g b
jnz g 2
set f 0
sub e -1
set g e
sub g b
jnz g -8
sub d -1
set g d
sub g b
jnz g -13
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23"""

def parsearg(arg,regs):
	try:
		return int(arg)
	except ValueError:
		return regs[arg]

def run(data):
	pc = 0
	insts = [inst.split() for inst in data.split("\n")]
	regs = defaultdict(int)
	muls = 0

	while pc < len(insts):
		op, ra, rb = insts[pc]
		b = parsearg(rb,regs)

		pcinc = 1
		if op == "set":
			regs[ra] = b
		elif op == "mul":
			regs[ra] *= b
			muls += 1
		elif op == "sub":
			regs[ra] -= b
		elif op == "jnz":
			if parsearg(ra,regs) != 0:
				pcinc = b
		pc += pcinc

	return muls

print(run(data))
