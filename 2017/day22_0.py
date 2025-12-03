data = (10000,"""...##.#.#.####...###.....
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

test = [(70,"""..#
#..
..."""),(10000,"""..#
#..
...""")]

def run(data):
	bursts, start = data
	grid = [row for row in start.split("\n")]

	ydim = len(grid)
	xdim = len(grid[0])

	deltas = {"N" : (0, 1), "S" : (0,-1), "W" : (-1,0), "E" : (1, 0)}
	rturns = {"N":"E", "E":"S", "S":"W", "W":"N"}
	lturns = {"N":"W", "W":"S", "S":"E", "E":"N"}
	infected = set()

	for y in range(ydim):
		for x in range(xdim):
			if grid[y][x] == "#":
				infected.add((x-xdim//2,-(y-ydim//2)))

	pos = (0,0)
	dir = "N"

	cause_infection = 0

	for _ in range(bursts):
		if pos in infected:
			dir = rturns[dir]
			infected.remove(pos)
		else:
			dir = lturns[dir]
			infected.add(pos)
			cause_infection += 1

		delta = deltas[dir]
		pos = (pos[0] + delta[0], pos[1] + delta[1])

	return cause_infection

for t in test:
	print(run(t))
print(run(data))
