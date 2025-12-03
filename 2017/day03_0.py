from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
Delta = namedtuple('Delta', ['dx', 'dy'])
data = 325489

def run(stop):
	side = 1
	dirnum = 0

	deltas = (
		Delta(dx = 1, dy = 0),
		Delta(dx = 0, dy = 1),
		Delta(dx = -1,dy = 0),
		Delta(dx = 0, dy = -1)
		)

	n = 1
	last = Point(x = 0, y = 0)

	while True:
		for _ in range(2):
			dir = deltas[dirnum]
			dirnum = 0 if dirnum == 3 else dirnum + 1
			for _ in range(side):
				n += 1
				next = Point(
					x = last.x + dir.dx,
					y = last.y + dir.dy
					)

				if n == stop:
					return sum([abs(i) for i in next])
				last = next

		side += 1

print(run(data))
