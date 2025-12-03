data = (".#####.##.#.##...#.#.###..#.#..#..#.....#..####.#.##.#######..#...##.#..#.#######...#.#.#..##..#.#.#","""#..#. => .
##... => #
#.... => .
#...# => #
...#. => .
.#..# => #
#.#.# => .
..... => .
##.## => #
##.#. => #
###.. => #
#.##. => .
#.#.. => #
##..# => #
..#.# => #
..#.. => .
.##.. => .
...## => #
....# => .
#.### => #
#..## => #
..### => #
####. => #
.#.#. => #
.#### => .
###.# => #
##### => #
.#.## => .
.##.# => .
.###. => .
..##. => .
.#... => #""")

tests = [("#..#.#..##......###...###","""...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""")]

def run(data):
    pots,ruledata = data
    rules = []
    for r in ruledata.splitlines():
        fr,to = [x.strip() for x in r.split("=>")]
        if to == "#":
            rules.append(fr)

    startpot = pots.find("#")
    pots = pots.strip(".")

    seen = {}
    gen = 0
    numgens = 50000000000
    while gen < numgens:
        
        pots = "..." + pots + "..."
        startpot -= 3

        potlist = set()
        for fr in rules:
            start = 0
            while True:
                pos = pots.find(fr,start)
                if pos < 0:
                    break
                start = pos + 1
                potlist.add(pos + 2)

        pots = "".join(["#" if i in potlist else "." for i in range(min(potlist),max(potlist)+1)])
        startpot += min(potlist)
        gen += 1
        if pots in seen:
            oldstart, oldgen = seen[pots]
            deltagens = gen - oldgen
            deltastart = startpot - oldstart
            todo = numgens - gen
            fastforward = todo // deltagens
            startpot += fastforward * deltastart
            gen += fastforward * deltagens
        else:
            seen[pots] = (startpot,gen)

    return sum(startpot+i for i,p in enumerate(pots) if p == "#")

for test in [t for t in tests if t]:
    break
    try: print(run(test))
    except Exception as e: print("Error:",e)
    
print(run(data))
