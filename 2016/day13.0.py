#!/usr/local/bin/python3

data = 1364

# Dim needs to be bigger than target to allow for back-paths
xdim = 35
ydim = 45

building = [[None]*xdim for _ in range(ydim)]

for y in range(ydim):
	for x in range(xdim):
		binary = "{:b}".format(x*x + 3*x + 2*x*y + y + y*y + data)
		building[y][x] = True if binary.count("1") % 2 == 0 else False

path = [[None]*xdim for _ in range(ydim)]

path[1][1] = 0
while True:
	finished = True
	for y in range(ydim-1):
		for x in range(xdim-1):
			if building[y][x] and path[y][x] is None:
				possibles = []
				if building[y-1][x] and path[y-1][x] is not None:
					possibles.append(path[y-1][x] + 1)

				if building[y][x-1] and path[y][x-1] is not None:
					possibles.append(path[y][x-1] + 1)

				if building[y][x+1] and path[y][x+1] is not None:
					possibles.append(path[y][x+1] + 1)

				if building[y+1][x] and path[y+1][x] is not None:
					possibles.append(path[y+1][x] + 1)

				if len(possibles) > 0:
					path[y][x] = min(possibles)
					finished = False
	if finished:
		break

'''
for y in range(ydim):
	for x in range(xdim):
		if not building[y][x]:
			print("##",end="")
		else:
			if path[y][x] is None:
				print("  ",end="")
			else:
				print("{:2d}".format(path[y][x]),end="")
	print()
'''

print(path[39][31])

# Part 2
answer = 0
for y in range(ydim):
	for x in range(xdim):
		if path[y][x] is not None and path[y][x] <= 50:
			answer += 1
print(answer)
