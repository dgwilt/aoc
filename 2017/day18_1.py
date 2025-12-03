from collections import defaultdict

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

test = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

def parsearg(arg,regs):
	try:
		return int(arg)
	except ValueError:
		return regs[arg]

def run(data):
	insts = [inst.split() for inst in data.split("\n")]
	numpids = 2

	pcs = [0] * numpids
	allregs = [defaultdict(int) for _ in range(numpids)]
	queues = [[] for _ in range(numpids)]
	waiting = [False] * numpids

	# Initialize registers
	for pid in range(numpids):
		allregs[pid]['p'] = pid

	pid_1_snd = 0

	while True:
		for pid in range(numpids):
			# Check for halt condition
			if all(waiting):
				return pid_1_snd

			regs = allregs[pid]
			op, a, *rest = insts[pcs[pid]]
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
				queues[pid].append(parsearg(a,regs))
				if pid == 1:
					pid_1_snd += 1
			elif op == "rcv":
				rcv_index = 1 - pid
				if len(queues[rcv_index]) > 0:
					regs[a] = queues[rcv_index].pop(0)
				else:
					waiting[pid] = True
					pcinc = 0 # Don't move on because waiting
			elif op == "jgz":
				if parsearg(a,regs) > 0:
					pcinc = b

			pcs[pid] += pcinc

print(run(test))
print(run(data))
