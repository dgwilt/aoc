#!/usr/bin/env python3 

from re import search
from itertools import combinations, product
from math import gcd
from functools import reduce

data = """<x=8, y=0, z=8>
<x=0, y=-5, z=-10>
<x=16, y=10, z=-5>
<x=19, y=-10, z=-7>"""

tests = ["""<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""","""<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""]

def cmp(a, b):
    return (a > b) - (a < b) 

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def run(data):
    dims = 3
    pos = [[int(i) for i in search(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>',line).group(1,2,3)] for line in data.splitlines()]
    nmoons = len(pos)
    vel = [[0 for _ in range(dims)] for _ in range(nmoons)]
    seen = [{} for _ in range(dims)]
    orbits = [0 for _ in range(dims)]

    steps = 0
    while True:
        for d in [x for x in range(dims) if orbits[x] is 0]:
            state = tuple((pos[m][d],vel[m][d]) for m in range(nmoons))
            orbits[d] = steps - seen[d].get(state,steps)
            seen[d][state] = steps

        if all(o is not 0 for o in orbits): break

        steps += 1
        for axis in range(dims):
            for m1,m2 in combinations(range(nmoons),2):
                delta = cmp(pos[m1][axis], pos[m2][axis])
                vel[m1][axis] -= delta
                vel[m2][axis] += delta
        for m,d in product(range(nmoons),range(dims)): pos[m][d] += vel[m][d]

    return reduce(lcm,orbits)

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: 
        print(f"Error: {e}")

print(run(data))