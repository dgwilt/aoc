data = """################################
###########################..###
##########################...###
#########################..#####
####...##################.######
#####..################...#.####
#..G...G#########.####G.....####
#.......########.....G.......###
#.....G....###G....#....E.....##
####...##......##.............##
####G...#.G...###.G...........##
####G.......................####
####.........G#####.........####
####...GG#...#######.......#####
###.........#########G....######
###.G.......#########G...#######
###.G.......#########......#####
####.....G..#########....E..####
#####.......#########..E....####
######...##G.#######........####
######.#.#.G..#####.....##..####
########....E...........##..####
########....E#######........####
########......######E....##..E.#
########......#####.....#......#
########.....######............#
##################...#.E...E...#
##################.............#
###################.......E#####
####################....#...####
####################.###########
################################"""

tests = ["""######
#.G..#
#...E#
#E...#
######""","""#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""","""#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
""","""#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""","""#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""","""#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######""","""#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""]

G = 'G'
E = 'E'
W = '#'
S = "."
enemy = {G:E, E:G}
hp0 = 200

def adjacent(x,y):
    return (x-1,y),(x+1,y),(x,y-1),(x,y+1)

def read_order(xdim,positions):
    return sorted(positions, key=lambda p:p[1]*xdim+p[0])

def first_read_order(xdim,positions):
    return read_order(xdim,positions)[0]

def closest_enemies(world,mypos,myrace):
    enemies = set()
    search = set([mypos])
    visited = set([mypos])
    while not enemies and search:
        nextsearch = set()
        for pos in search:
            xs,ys = pos
            for x,y in adjacent(xs,ys):
                if (x,y) in visited:
                    continue
                other = world[y][x]
                if other == enemy[myrace]:
                    enemies.add(pos)
                elif other == S:
                    nextsearch.add((x,y))
            visited.add(pos)
           
        search = nextsearch
    return list(enemies)

def moves_to_enemy(world,xt,yt,xp,yp):
    allpaths = [row[::] for row in world]                    
    search = set([(xt,yt)])
    dist = 0
    allpaths[yt][xt] = str(dist)
    while search:
        nextsearch = set()
        dist += 1
        for pos in search:
            xs,ys = pos
            for x,y in adjacent(xs,ys):
                if allpaths[y][x] is S:
                    allpaths[y][x] = str(dist)
                    nextsearch.add((x,y))
        search = nextsearch

    moves = []
    # Having flood-filled, now find smallest number adjacent to player
    for x,y in adjacent(xp,yp):
        cell = allpaths[y][x]
        if cell.isdigit():
            moves.append({'pos':(x,y), 'dist':int(cell)})

    return moves

def make_move(moves,world,players,xp,yp,xdim,myrace):
    mypos = (xp,yp)
    shortest_dist = min(moves,key=lambda m:m['dist'])['dist']
    closest = [m['pos'] for m in moves if m['dist'] == shortest_dist]
    world[yp][xp] = S
    xp,yp = first_read_order(xdim,closest)
    players[(xp,yp)] = players.pop(mypos)
    world[yp][xp] = myrace
    return xp,yp

def do_attack(foes,players,xdim,world,recently_deceased,armies,ap):
    lowesthp = min(players[f]['hp'] for f in foes)
    weakest = [f for f in foes if players[f]['hp'] == lowesthp]
    attack = first_read_order(xdim,weakest)
    players[attack]['hp'] -= ap
    if players[attack]['hp'] <= 0:
        xa, ya = attack
        world[ya][xa] = S
        recently_deceased.append(attack) # To make sure you don't process a ghost!
        dead_race = players.pop(attack)['race']
        armies[dead_race] -= 1
        return armies[dead_race] == 0
    else:
        return False

def make_world(world,players,armies):
    for y,row in enumerate(world):
        for x, race in enumerate(row):
            if race in [G,E]:
                players[(x,y)] = {'race':race, 'hp':hp0}
                armies[race] += 1

def run(data):
    world = [list(row) for row in data.splitlines()]
    xdim = len(world[0])

    ap = 3 # Attack power

    players = {}
    armies = {G:0, E:0}

    make_world(world,players,armies)

    rounds = 0
    while True:
        lastplayer = len(players)-1
        recently_deceased = []
        for pnum,mypos in enumerate(read_order(xdim,players.keys())):
            # To deal with players that are killed during the round, who were there at the start
            if mypos in recently_deceased: continue

            # A round is finished when the last player takes their turn
            if pnum == lastplayer: rounds += 1

            myrace = players[mypos]['race']
            xp,yp = mypos

            if not any(world[y][x] == enemy[myrace] for x,y in adjacent(xp,yp)):
                # Move only if no adjacent targets
                enemies = closest_enemies(world,mypos,myrace)
                if enemies:
                    xt,yt = first_read_order(xdim,enemies)
                    # Flood fill from the target to find shortest path
                    moves = moves_to_enemy(world,xt,yt,xp,yp)
                    xp,yp = make_move(moves,world,players,xp,yp,xdim,myrace)

            foes = [(x,y) for x,y in adjacent(xp,yp) if world[y][x] == enemy[myrace]]
            if foes:
                finished = do_attack(foes,players,xdim,world,recently_deceased,armies,ap)
                if finished:
                    return rounds * sum(p['hp'] for p in players.values())

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: print("Error:",e)
    
print(run(data))
