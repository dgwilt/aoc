from math import lcm

def parser(data):
    instructions,network = data.split("\n\n")
    maps = {}
    for line in network.splitlines():
        fr,lr = line.split(____)
        l,r = lr[1:-1].split(____)
        maps[fr] = {____}
    return instructions,maps

def run_silver(data):
    instructions,maps = parser(data)
    l = len(instructions)
    node = ___
    steps = 0
    while node != ____:
        dir = instructions[____]
        steps += 1
        node = maps[____][____]
    return steps

def run_gold(data):
    instructions,maps = parser(data)
    l = len(instructions)
    gnodes = [n for n in maps if n.endswith('A')]
    gsteps = [0] * len(gnodes)
    
    while 0 in gsteps:
        dir = instructions[____]
        steps += 1
        for i in [i for i,s in enumerate(gsteps) if s == 0]:
            pass
    
    return lcm(*gsteps)

