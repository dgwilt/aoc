data = 330121

tests = [9,5,18,2018]

def run(data):
    recipies = "37"
    elfpos = [0,1]
    last = 10
    lenr = len(recipies)
    while lenr < data + last:
        elfnums = [int(recipies[e]) for e in elfpos]
        new = str(sum(elfnums))
        recipies = recipies + new
        lenr += len(new)
        elfpos = [(elfpos[i] + 1 + elfnums[i]) % lenr for i in range(2)]

    return recipies[-last:]

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: print("Error:",e)
    
print(run(data))
