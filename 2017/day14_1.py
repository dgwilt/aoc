from day10_1 import run as knothash
from day12_1 import run as getgroups

data = "jzgqcdpd"
test = "flqrgnkx"

def getpos(x,y):
	return str(x + (128 * y))

def run(data):
	dim = 128
	grid = []
	for i in range(dim):
		row = "{:0128b}".format(int(knothash("{}-{}".format(data,i),256),16))
		grid.append([int(i) for i in row])

	toprocess = []
	for y in range(dim):
		for x in range(dim):
			if grid[y][x] == 1:
				fr = getpos(x,y)
				to =  [getpos(x,yy) for yy in [y-1,y+1] if 0 <= yy < dim and grid[yy][x] == 1]
				to += [getpos(xx,y) for xx in [x-1,x+1] if 0 <= xx < dim and grid[y][xx] == 1]
				toprocess.append("{} <-> {}".format(fr,", ".join(to) if len(to) > 0 else fr))

	return getgroups("\n".join(toprocess))

print(run(test))
print(run(data))
