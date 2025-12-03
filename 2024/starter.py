from itertools import product

data = """"""

W,S,E,N = (-1, 0), (0, 1), (1, 0), (0, -1)
grid = data.splitlines()
xdim,ydim = len(grid[0]),len(grid)
plot = {(x,y):grid[y][x] for x,y in product(range(xdim),range(ydim))}
visited = set()
regions = []
for start in plot:
    if start in visited: continue
    plant = plot[start]
    todo = [start]
    region = set()
    while todo:
        pos = todo.pop()
        if pos in region: continue
        region.add(pos)
        for dir in (W,S,E,N):
            nxt = (pos[0]+dir[0],pos[1]+dir[1])
            if plot.get(nxt,"") == plant:
                todo.append(nxt)
    visited.update(region)
    regions.append(region)

cost = 0
for region in regions:
    perimeter = 0
    for pos in region:
        for dir in (W,S,E,N):
            nxt = (pos[0]+dir[0],pos[1]+dir[1])
            if nxt not in region:
                perimeter += 1
    cost += len(region) * perimeter

print(cost)
