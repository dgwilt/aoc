from collections import defaultdict, namedtuple, Counter

data = ("""84, 212
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
241, 185""",10000)

tests = [("""1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""",32)]

def mdist(fr,to):
    return abs(fr[0]-to[0]) + abs(fr[1]-to[1])

def run(alldata):
    data,checkdist = alldata
    coords = [[int(i) for i in l.split(",")] for l in data.splitlines()]        
    minx = min([c[0] for c in coords])
    miny = min([c[1] for c in coords])
    maxx = max([c[0] for c in coords])
    maxy = max([c[1] for c in coords])

    region = 0
    for x in range(minx,maxx+1):
        for y in range(miny,maxy+1):
            fr = (x,y)
            sumd = sum([mdist(fr,c) for c in coords])
            if sumd < checkdist:
                region += 1

    return region

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: print("Error:",e)
    
print(run(data))
