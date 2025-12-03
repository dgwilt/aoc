from itertools import product

data = "330121"

tests = ["51589","01245","92510","59414"]

cache = {}
for a,b in product(range(10),repeat=2):
    s = str(a+b)
    l = len(s)
    cache[str(a)+str(b)] = (s,l,a+1,b+1)

def run(data):
    recipies = "37"
    epos0 = 0
    epos1 = 1
    l = len(data) + 1
    lenr = len(recipies)
    while data not in recipies[-l:]:
        new,lnew,move0,move1 = cache[recipies[epos0] + recipies[epos1]]
        recipies += new
        lenr += lnew
        epos0 = (epos0 + move0) % lenr
        epos1 = (epos1 + move1) % lenr

    return lenr - l + recipies[-l:].find(data)

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: print("Error:",e)
    
print(run(data))
