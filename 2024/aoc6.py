data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

OBSTACLE = "#"
GUARD = "^"
N,S,W,E = (0,-1),(0,1),(-1,0),(1,0)
turns = {N:E,
         E:S,
         S:W,
         W:N}

grid = data.splitlines()
width = len(grid[0])
height = len(grid)
plan = {}
for x in range(width):
    for y in range(height):
        cell = grid[y][x]
        pos = (x,y)
        plan[pos] = cell
        if cell == GUARD:
            guard = pos

dir = N
visited = set()
while guard in plan:
    visited.add(guard)
    while plan.get(nxt := (guard[0]+dir[0], guard[1]+dir[1]),"") == OBSTACLE:
        dir = turns[dir]
    guard = nxt

print(len(visited))
