from collections import defaultdict
from re import search
from blist import *

data = """446 players; last marble is worth 7152200 points"""

tests = ["9 players; last marble is worth 25 points",
"10 players; last marble is worth 1618 points",
"13 players; last marble is worth 7999 points",
"17 players; last marble is worth 1104 points",
"21 players; last marble is worth 6111 points",
"30 players; last marble is worth 5807 points"]

def run(data):
    players, maxmarble = [int(i) for i in search(r'(\d+) players; last marble is worth (\d+) points',data).group(1,2)]
    circle = blist([0])
    scores = defaultdict(int)
    toplace = 1
    current = 0
    elf = 1
    pos = 0
    nummarbles = 1
    while toplace <= maxmarble:
        if toplace % 23 == 0:
            takepos = (pos - 7) % nummarbles
            scores[elf] += toplace + circle.pop(takepos)
            current = circle[takepos]
            pos = takepos
            nummarbles -= 1
        else:
            placepos = (pos + 2) % nummarbles
            if placepos == 0:
                circle.append(toplace)                
                pos = nummarbles
            else:
                circle.insert(placepos,toplace)
                pos = placepos
            current = toplace
            nummarbles += 1

        toplace += 1
        elf = (elf + 1) % players
    return max(scores.values())

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: print("Error:",e)
    
print(run(data))
