from itertools import permutations, product

data = 1308

tests = [42]

def get_power(x,y,serial):
    rackID = x + 10
    power = rackID * y
    power += serial
    power *= rackID
    power = (power // 100) % 10
    power -= 5
    return power

def run(data):
    dim = 300
    grid = [[get_power(x+1,y+1,data) for x in range(dim)] for y in range(dim)]

    maxp = None
    psums = dict()
    for box in range(1,300):
        if box == 1:
            psums[box] = grid
        elif box%2 == 0:
            hbox = box // 2
            psums[box] = [[sum(psums[hbox][y+yoff][x+xoff] for xoff,yoff in product([0,hbox],repeat=2)) for x in range(dim-box)] for y in range(dim-box)]
        else:
            psums[box] = [[psums[box-1][y][x] + psums[box-1][y+1][x+1] - psums[box-2][y+1][x+1] + grid[y][x+box-1] + grid[y+box-1][x] for x in range(dim-box)] for y in range(dim-box)]
        maxys = [max(row) for row in psums[box]]
        thismaxp = max(maxys)
        if thismaxp < 0:
            # When the values get negative, drop out
            break
        if maxp is None or thismaxp > maxp:
            maxp = thismaxp
            ymax = maxys.index(maxp)
            xmax = psums[box][ymax].index(maxp)
            maxdim = box
      
    return xmax+1,ymax+1,maxdim

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: print("Error:",e)
    
print(run(data))
