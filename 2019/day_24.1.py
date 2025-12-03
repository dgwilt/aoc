#!/usr/bin/env python3 

from itertools import product

S = (0,1)
N = (0,-1)
W = (-1,0)
E = (1,0)
bug = 1
space = 0
deltas = (S,N,W,E)
spawn = (1,2)

data = """##.##
#.##.
#...#
##.#.
####."""

def serialize(grid):
    return tuple(tuple(row) for row in grid)

def adjacent_to(x,y,xdim,ydim):
    pos = (x,y)
    adjacent = []
    for ax,ay in [[pos[i] + delta[i] for i in range(2)] for delta in deltas]:
        if 0 <= ax < xdim and 0 <= ay < ydim: adjacent.append((ax,ay))
    return adjacent

def empty(xdim,ydim):
    return [[space for _ in range(xdim)] for _ in range(ydim)]

def run(data):
    grid = [[space if cell == "." else bug for cell in line] for line in data.splitlines()]
    seen = set()
    xdim,ydim = len(grid[0]),len(grid)
    while (s := serialize(grid)) not in seen:
        seen.add(s)
        nextgrid = empty(xdim,ydim)
        for x,y in product(range(xdim),range(ydim)):

            adjacent_bugs = sum(grid[ay][ax] for ax,ay in adjacent_to(x,y,xdim,ydim))
            cell = grid[y][x]

            if (cell is bug and adjacent_bugs == 1) or (cell is space and adjacent_bugs in spawn):
                nextgrid[y][x] = bug

        grid = nextgrid

    return sum(grid[y][x] * 2**(x + xdim*y) for x,y in product(range(xdim),range(ydim)))

print(run(data))