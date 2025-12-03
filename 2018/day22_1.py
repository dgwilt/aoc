from itertools import product
from re import search

data = """depth: 4080
target: 14,785"""

tests = ["""depth: 510
target: 10,10"""]

def run(data):
    depth,xt,yt = [int(i) for i in search(r'depth: (\d+)\ntarget: (\d+),(\d+)',data).group(1,2,3)]
    xdim = xt+1
    ydim = yt+1
    erosion = [[None]*xdim for _ in range(ydim)]
    erosion[0][0] = depth % 20183
    for y in range(ydim):
        erosion[y][0] = ((y*48271) + depth) % 20183
    for x in range(xdim):
        erosion[0][x] = ((x*16807) + depth) % 20183
    for x,y in product(range(1,xdim),range(1,ydim)):
        erosion[y][x] = ((erosion[y][x-1] * erosion[y-1][x]) + depth) % 20183
    erosion[yt][xt] = depth % 20183
    risk = 0
    for x,y in product(range(0,xdim),range(0,ydim)):
        risk += erosion[y][x] % 3
    return risk

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: print("Error:",e)
    
print(run(data))
