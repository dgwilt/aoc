data = "4	1	15	12	0	9	9	5	5	8	7	3	14	5	12	3"

test = "0 2 7 0"

def run(data):
	blocks = [int(i) for i in data.split()]
	seen = set()
	seen.add(str(blocks))
	rounds = 0
	while True:
		rounds += 1
		index = blocks.index(max(blocks))
		
		# re-distribute the blocks
		to_distribute = blocks[index]
		blocks[index] = 0
		while to_distribute > 0:
			index = (index + 1) % len(blocks)
			blocks[index] += 1
			to_distribute -= 1

		# have we seen it before?
		config = str(blocks)
		if config in seen:
			return rounds
		seen.add(config)

print(run(test))
print(run(data))
