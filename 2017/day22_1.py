from collections import defaultdict

data = (10000000,"""...##.#.#.####...###.....
..#..##.#...#.##.##.#..#.
.#.#.#.###....#...###....
.#....#..####.....##.#..#
##.#.#.#.#..#..#.....###.
#...##....##.##.#.##.##..
.....###..###.###...#####
######.####..#.#......##.
#..###.####..####........
#..######.##....####...##
...#.##.#...#.#.#.#..##.#
####.###..#####.....####.
#.#.#....#.####...####...
##...#..##.##....#...#...
......##..##..#..#..####.
.##..##.##..####..##....#
.#..#..##.#..##..#...#...
#.#.##.....##..##.#####..
##.#.......#....#..###.#.
##...#...#....###..#.#.#.
#....##...#.#.#.##..#..##
#..#....#####.....#.##.#.
.#...#..#..###....###..#.
..##.###.#.#.....###.....
#.#.#.#.#.##.##...##.##.#""")

test = (100,"""..#
#..
...""")

def run(data):

	bursts, start = data
	grid = [row for row in start.split("\n")]

	ydim = len(grid)
	xdim = len(grid[0])

	deltas = {"N" : (0, 1), "S" : (0,-1), "W" : (-1,0), "E" : (1, 0)}
	rturns = {"N":"E", "E":"S", "S":"W", "W":"N"}
	lturns = {"N":"W", "W":"S", "S":"E", "E":"N"}
	bturns = {"N":"S", "W":"E", "S":"N", "E":"W"}
	nstates = {"C":"W", "W":"I", "I":"F", "F":"C"}

	nodes = defaultdict(lambda:"C")

	for y in range(ydim):
		for x in range(xdim):
			if grid[y][x] == "#":
				nodes[(x-xdim//2,-(y-ydim//2))] = "I"

	pos = (0,0) # Tuples are hashable
	dir = "N"

	cause_infection = 0

	for _ in range(bursts):
		state = nodes[pos] # Defaultdict returns 'C' if not seen before
		if state == "F":
			dir = bturns[dir]
		elif state == "I":
			dir = rturns[dir]
		elif state == "C":
			dir = lturns[dir]

		nstate = nstates[state]
		if nstate == "I":
			cause_infection += 1
		nodes[pos] = nstate

		delta = deltas[dir]
		pos = (pos[0] + delta[0], pos[1] + delta[1])

	return cause_infection

print(run(test))
print(run(data))
