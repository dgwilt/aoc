#!/usr/bin/env python3 

from itertools import product
from math import atan2,hypot,degrees
from collections import defaultdict

data = [(22,25),""".#.####..#.#...#...##..#.#.##.
..#####.##..#..##....#..#...#.
......#.......##.##.#....##..#
..#..##..#.###.....#.#..###.#.
..#..#..##..#.#.##..###.......
...##....#.##.#.#..##.##.#...#
.##...#.#.##..#.#........#.#..
.##...##.##..#.#.##.#.#.#.##.#
#..##....#...###.#..##.#...##.
.###.###..##......#..#...###.#
.#..#.####.#..#....#.##..#.#.#
..#...#..#.#######....###.....
####..#.#.#...##...##....#..##
##..#.##.#.#..##.###.#.##.##..
..#.........#.#.#.#.......#..#
...##.#.....#.#.##........#..#
##..###.....#.............#.##
.#...#....#..####.#.#......##.
..#..##..###...#.....#...##..#
...####..#.#.##..#....#.#.....
####.#####.#.#....#.#....##.#.
#.#..#......#.........##..#.#.
#....##.....#........#..##.##.
.###.##...##..#.##.#.#...#.#.#
##.###....##....#.#.....#.###.
..#...#......#........####..#.
#....#.###.##.#...#.#.#.#.....
.........##....#...#.....#..##
###....#.........#..#..#.#.#..
##...#...###.#..#.###....#.##."""]

tests = [[(11,13),""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""]]

def run(data):
    station = data[0]
    grid = [l for l in data[1].splitlines()]
    ydim = len(grid)
    xdim = len(grid[0])
    asteroids = set([(x,y) for x,y in product(range(xdim),range(ydim)) if grid[y][x] is "#"])
    asteroids.remove(station)
    angledist = defaultdict(list)
    for a in asteroids:
        xd,yd = list(a[i]-station[i] for i in range(2))
        angle = 90 - degrees(atan2(-yd,xd))
        if angle < 0: angle += 360
        angledist[angle].append((hypot(xd,yd),a))

    for d in angledist.values(): 
        d.sort(key=lambda x:x[0])
    
    angles = sorted(angledist.keys())
    hitcount = 0
    aptr = 0
    while hitcount < 200:
        a = angles[aptr]
        _, vap = angledist[a].pop(0)
        if len(angledist[a]) == 0: angles.remove(a)
        else: aptr += 1
        aptr %= len(angles)
        hitcount += 1
    
    vx,vy = vap
    return 100*vx + vy

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: 
        print(f"Error: {e}")

print(run(data))