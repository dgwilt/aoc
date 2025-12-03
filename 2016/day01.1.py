data = '''R4, R4, L1, R3, L5, R2, R5, R1, L4, R3, L5, R2, L3, L4, L3, R1, R5, R1, L3, L1, R3, L1, R2, R2, L2, R5, L3, L4, R4, R4, R2, L4, L1, R5, L1, L4, R4, L1, R1, L2, R5, L2, L3, R2, R1, L194, R2, L4, R49, R1, R3, L5, L4, L1, R4, R2, R1, L5, R3, L5, L4, R4, R4, L2, L3, R78, L5, R4, R191, R4, R3, R1, L2, R1, R3, L1, R3, R4, R2, L2, R1, R4, L5, R2, L2, L4, L2, R1, R2, L3, R5, R2, L3, L3, R3, L1, L1, R5, L4, L4, L2, R5, R1, R4, L3, L5, L4, R5, L4, R5, R4, L3, L2, L5, R4, R3, L3, R1, L5, R5, R1, L3, R2, L5, R5, L3, R1, R4, L5, R4, R2, R3, L4, L5, R3, R4, L5, L5, R4, L4, L4, R1, R5, R3, L1, L4, L3, L4, R1, L5, L1, R2, R2, R4, R4, L5, R4, R1, L1, L1, L3, L5, L2, R4, L3, L5, L4, L1, R3'''

instructions = data.split(", ")
rdirs = {'N':'E','E':'S','S':'W','W':'N'}
ldirs = {'N':'W','W':'S','S':'E','E':'N'}

def have_visited(x,y,visits):
	if (x,y) in visits:
		return True
	else:
		visits.add((x,y))
		return False

def walk(instructions):
	x = 0
	y = 0
	d = 'N'
	visits = set()
	for i in instructions:
		turn = i[0]
		dist = int(i[1:])
		if turn == 'L':
			d = ldirs[d]
		elif turn == 'R':
			d = rdirs[d]

		dist += 1
		if d == 'N':
			for _ in range(1,dist):
				y += 1
				if have_visited(x,y,visits):
					return(abs(x)+abs(y))
		elif d == 'S':
			for _ in range(1,dist):
				y -= 1
				if have_visited(x,y,visits):
					return(abs(x)+abs(y))
		elif d == 'W':
			for _ in range(1,dist):
				x -= 1
				if have_visited(x,y,visits):
					return(abs(x)+abs(y))
		elif d == 'E':
			for _ in range(1,dist):
				x += 1
				if have_visited(x,y,visits):
					return(abs(x)+abs(y))

print(walk(instructions))
