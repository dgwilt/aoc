from itertools import product, permutations
from re import search
import networkx as nx

data = """depth: 4080
target: 14,785"""

tests = ["""depth: 510
target: 10,10"""]

TORCH = "TORCH"
CLIMB = "CLIMB"
NONE = "NONE"
R = "."
W = "="
N = "|"
rocktypes = [R,W,N]
allequip = [TORCH,CLIMB,NONE]
equipment = {
    R:{CLIMB,TORCH},
    W:{CLIMB,NONE},
    N:{TORCH,NONE}
    }

def index_to_erosion(index,depth):
    return (index + depth) % 20183

def run(data):
    depth,xt,yt = [int(i) for i in search(r'depth: (\d+)\ntarget: (\d+),(\d+)',data).group(1,2,3)]
    xdim = xt+500
    ydim = yt+500
    index = [[None]*xdim for _ in range(ydim)]
    index[0][0] = 0
    for y in range(ydim):
        index[y][0] = y*48271
    for x in range(xdim):
        index[0][x] = x*16807
    for x,y in product(range(1,xdim),range(1,ydim)):
        if (x,y) == (xt,yt):
            index[y][x] = 0
        else:
            index[y][x] = index_to_erosion(index[y][x-1],depth) * index_to_erosion(index[y-1][x],depth)

    erosion = [[None]*xdim for _ in range(ydim)]
    for x,y in product(range(xdim),range(ydim)):
        erosion[y][x] = rocktypes[index_to_erosion(index[y][x],depth)%3]

    g = nx.Graph()
    for x,y in product(range(xdim),range(ydim)):
        for e1,e2 in permutations(allequip,2):
            g.add_edge((x,y,e1),(x,y,e2), weight=7)
        me = erosion[y][x]
        e1 = equipment[me]
        for xn,yn in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            try:
                n = erosion[yn][xn]
            except IndexError:
                continue
            e2 = equipment[n]
            for e in e1.intersection(e2):
                g.add_edge((x,y,e),(xn,yn,e), weight=1)

    return nx.dijkstra_path_length(g, source=(0,0,TORCH), target=(xt,yt,TORCH), weight="weight")

for test in [t for t in tests if t]:
    break
    try: print(run(test))
    except Exception as e: print("Error:",e)
    
print(run(data))
