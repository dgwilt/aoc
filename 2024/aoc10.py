data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

multipath = False # True for part two

grid = data.splitlines()
xsize = len(grid[0])
ysize = len(grid)
trailheads = []
for y in range(ysize):
    for x in range(xsize):
        if grid[y][x] == '0':
            trailheads.append((x,y))

result = 0
for start in trailheads:
    visited = set()
    score = 0
    todo = [[start,0]]
    while todo:
        next = todo.pop()
        pos = next[0]
        height = next[1]

        if not multipath:
            if pos in visited:
                continue
            visited.add(pos)

        if height == 9:
            score = score + 1
        else:
            xpos = pos[0]
            ypos = pos[1]
            up = height + 1
            for chX,chY in [0,-1],[0,1],[-1,0],[1,0]:
                x = xpos + chX
                y = ypos + chY
                if 0 <= x < xsize and 0 <= y < ysize and int(grid[y][x]) == up:
                    nextpos = (x,y)
                    todo.append([nextpos,up])
    result = result + score
print(result)
