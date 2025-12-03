#!/usr/bin/env python3 

from itertools import product

S = (0,1)
N = (0,-1)
W = (-1,0)
E = (1,0)
bug = 1
space = 0
deltas = (S,N,W,E)
middle = (2,2)
left = (1,2)
top = (2,1)
right = (3,2)
bottom = (2,3)
inner_edges = (left,right,top,bottom)
spawn = (1,2)

data = [200,"""##.##
#.##.
#...#
##.#.
####."""]

tests = [[10,"""....#
#..#.
#..##
..#..
#...."""]]

def at(grid,pos):
    x,y = pos
    return grid[y][x]

def empty(xdim,ydim):
    return [[space for _ in range(xdim)] for _ in range(ydim)]

def adjacent_to(x,y,z,xdim,ydim,zmin,zmax):
    pos = (x,y)
    adjacent_cells = []
    for ax,ay in [[pos[i] + delta[i] for i in range(2)] for delta in deltas]:
        if (ax,ay) == middle:
            az = z + 1
            if pos == left:
                for aay in range(ydim): 
                    adjacent_cells.append((0,aay,az))
            elif pos == top:
                for aax in range(xdim):
                    adjacent_cells.append((aax,0,az))
            elif pos == right:
                for aay in range(ydim):
                    adjacent_cells.append((-1,aay,az))
            elif pos == bottom:
                for aax in range(xdim):
                    adjacent_cells.append((aax,-1,az))
        elif ax == -1:
            adjacent_cells.append((*left,z-1))
        elif ax == xdim:
            adjacent_cells.append((*right,z-1))
        elif ay == -1:
            adjacent_cells.append((*top,z-1))
        elif ay == ydim:
            adjacent_cells.append((*bottom,z-1))
        else:
            adjacent_cells.append((ax,ay,z))

    return [a for a in adjacent_cells if zmin <= a[2] <= zmax]

def run(data):
    time,world = data
    grid = [[space if cell == "." else bug for cell in line] for line in world.splitlines()]
    xdim,ydim = len(grid[0]),len(grid)
    zmin = 0
    zmax = 0
    grids = {0:grid}

    # z increases in the middle
    for _ in range(time):
        outer_edges = (
            (row[0] for row in grids[zmin]),
            (row[-1] for row in grids[zmin]),
            (grids[zmin][0]),
            (grids[zmin][-1]))

        if any(sum(edge) in spawn for edge in outer_edges):
            zmin -= 1
            grids[zmin] = empty(xdim,ydim)

        if any(at(grids[zmax],cell) == 1 for cell in inner_edges): 
            zmax += 1
            grids[zmax] = empty(xdim,ydim)

        nextgrids = {}
        for z in range(zmin,zmax+1):
            nextgrid = empty(xdim,ydim)
            for x,y in product(range(xdim),range(ydim)):
                if (x,y) == middle: continue

                adjacent_bugs = sum(grids[az][ay][ax] for ax,ay,az in adjacent_to(x,y,z,xdim,ydim,zmin,zmax))
                cell = grids[z][y][x]

                if (cell is bug and adjacent_bugs == 1) or (cell is space and adjacent_bugs in spawn):
                    nextgrid[y][x] = bug
            
            nextgrids[z] = nextgrid
        grids = nextgrids

    return sum(sum(sum(row) for row in grid) for grid in grids.values())

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: 
        print(f"Error: {e}")

print(run(data))
