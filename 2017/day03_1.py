from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
Delta = namedtuple('Delta', ['dx', 'dy'])

data = 325489

def run(stop):
	side = 1
	dirnum = 0

	deltas = (
		Delta(dx = 1, dy = 0), # Right
		Delta(dx = 0, dy = 1), # Up
		Delta(dx = -1,dy = 0), # Left
		Delta(dx = 0, dy = -1) # Down
		)

	last = Point(x = 0, y = 0)

	griddim = 20
	grid = [[0 for _ in range(griddim)] for _ in range(griddim)]
	mid = Point(x = griddim//2, y = griddim//2)

	grid[mid.y][mid.x] = 1

	while True:
		for _ in range(2):
			dir = deltas[dirnum]
			dirnum = 0 if dirnum == 3 else dirnum + 1
			for _ in range(side):
				next = Point(
					x = last.x + dir.dx,
					y = last.y + dir.dy
					)
				pos = Point(
					x = next.x + mid.x,
					y = next.y + mid.y
					)
				s = sum((grid[y][x] 
					for x in range(pos.x - 1, pos.x + 2) 
					for y in range(pos.y - 1, pos.y + 2)))

				if s > stop:
					return s

				grid[pos.y][pos.x] = s
				last = next

		side += 1

print(run(data))
