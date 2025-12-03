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

    box = 3
    psums = [[sum(sum(grid[y][x0:x0+box]) for y in range(y0,y0+box)) for x0 in range(dim-box)] for y0 in range(dim-box)]
    maxys = [max(row) for row in psums]
    maxp = max(maxys)
    ymax = maxys.index(maxp)
    xmax = psums[ymax].index(maxp)
    return xmax+1, ymax+1

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: print("Error:",e)
    
print(run(data))
