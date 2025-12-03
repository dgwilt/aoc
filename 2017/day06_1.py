data = "4	1	15	12	0	9	9	5	5	8	7	3	14	5	12	3"
test = "0 2 7 0"

def run(data):
	blocks = [int(i) for i in data.split()]
	l = len(blocks)

	rounds = 0
	seen = {str(blocks) : rounds}
	while True:
		rounds += 1
		index = blocks.index(max(blocks))

		to_distribute = blocks[index]
		blocks[index] = 0
		while to_distribute > 0:
			index = (index + 1) % l
			blocks[index] += 1
			to_distribute -= 1
			
		config = str(blocks)
		if config in seen:
			return rounds - seen[config]
		seen[config] = rounds

print(run(test))
print(run(data))
