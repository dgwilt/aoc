#!/usr/bin/env python3 

from re import search
from itertools import combinations, product

data = [1000,"""<x=8, y=0, z=8>
<x=0, y=-5, z=-10>
<x=16, y=10, z=-5>
<x=19, y=-10, z=-7>"""]

tests = [[10,"""<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""],[100,"""<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""]]

def cmp(a, b):
    return (a > b) - (a < b) 

def run(data):
    steps, positions = data
    dims = 3
    pos = [[int(i) for i in search(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>',line).group(1,2,3)] for line in positions.splitlines()]
    nmoons = len(pos)
    vel = [[0 for _ in range(dims)] for _ in range(nmoons)]
    for _ in range(steps):
        for axis in range(dims):
            for m1,m2 in combinations(range(nmoons),2):
                delta = cmp(pos[m1][axis], pos[m2][axis])
                vel[m1][axis] -= delta
                vel[m2][axis] += delta
        for m,d in product(range(nmoons),range(dims)): pos[m][d] += vel[m][d]
        
    pe = tuple(sum(abs(p) for p in moon) for moon in pos)
    ke = tuple(sum(abs(v) for v in moon) for moon in vel)
    return sum(pe[i] * ke[i] for i in range(nmoons))

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: 
        print(f"Error: {e}")

print(run(data))