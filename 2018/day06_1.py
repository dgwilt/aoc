from collections import defaultdict, namedtuple, Counter

data = """84, 212
168, 116
195, 339
110, 86
303, 244
228, 338
151, 295
115, 49
161, 98
60, 197
40, 55
55, 322
148, 82
86, 349
145, 295
243, 281
91, 343
280, 50
149, 129
174, 119
170, 44
296, 148
152, 160
115, 251
266, 281
269, 285
109, 242
136, 241
236, 249
338, 245
71, 101
254, 327
208, 231
289, 184
282, 158
352, 51
326, 230
88, 240
292, 342
352, 189
231, 141
280, 350
296, 185
226, 252
172, 235
137, 161
207, 90
101, 133
156, 234
241, 185"""

tests = ["""1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
"""]

def mdist(fr,to):
    return abs(fr[0] - to[0]) + abs(fr[1] - to[1])

def run(data):
    coords = [[int(i) for i in l.split(",")] for l in data.splitlines()]
    minx = min([c[0] for c in coords])
    miny = min([c[1] for c in coords])
    maxx = max([c[0] for c in coords])
    maxy = max([c[1] for c in coords])
    
    grid = defaultdict()
    for x in range(minx,maxx+1):
        for y in range(miny,maxy+1):
            fr = (x,y)
            mind = None
            for i,c in enumerate(coords):
                d = mdist(fr,c)
                if mind is None or d < mind:
                    mind = d
                    minc = i
                elif d == mind:
                    # Equidistant
                    minc = -1
            grid[fr] = minc

    infinite = []
    for x in [minx,maxx]:
        for y in range(miny,maxy+1):
            infinite.append(grid[(x,y)])
    for y in [miny,maxy]:
        for x in range(minx,maxx+1):
            infinite.append(grid[(x,y)])

    c = Counter(grid.values())
    for i in infinite:
        c[i] = 0
    c[-1] = 0 # Equidistant
    return max(c.values())

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: print("Error:",e)
    
print(run(data))
