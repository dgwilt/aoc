from collections import namedtuple, defaultdict

data = """set i 31
set a 1
mul p 17
jgz p p
mul a 2
add i -1
jgz i -2
add a -1
set i 127
set p 952
mul p 8505
mod p a
mul p 129749
add p 12345
mod p a
set b p
mod b 10000
snd b
add i -1
jgz i -9
jgz a 3
rcv b
jgz b -1
set f 0
set i 126
rcv a
rcv b
set p a
mul p -1
add p b
jgz p 4
snd a
set a b
jgz 1 3
snd b
set f 1
add i -1
jgz i -11
snd a
jgz f -16
jgz a -19"""

test = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

def parsearg(arg,regs):
	try:
		return int(arg)
	except ValueError:
		return regs[arg]

def run(data):
	pc = 0
	insts = [inst.split() for inst in data.split("\n")]
	regs = defaultdict(int)
	lastplayed = None
	while True:

		op, a, *rest = insts[pc]
		if len(rest) > 0:
			b = parsearg(rest[0],regs)

		pcinc = 1
		if op == "set":
			regs[a] = b
		elif op == "add":
			regs[a] += b
		elif op == "mul":
			regs[a] *= b
		elif op == "mod":
			regs[a] %= b
		elif op == "snd":
			lastplayed = parsearg(a,regs)
		elif op == "rcv":
			if parsearg(a,regs) != 0:
				break
		elif op == "jgz":
			if parsearg(a,regs) > 0:
				pcinc = b
		pc += pcinc

	return lastplayed

print(run(test))
print(run(data))
