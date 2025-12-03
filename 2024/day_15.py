#!/usr/bin/env python3 
from itertools import product
from sys import argv
from aoc import AocDay

class AocDay15(AocDay):

    silver_modifier = lambda room : room.splitlines()
    gold_modifier = lambda room : room.replace("O","[]").replace("#","##").replace(".","..").replace("@","@.").splitlines()

    def parser(self,data,modifier):
        DELTAS = {"^":(0,-1),"v":(0,1),">":(1,0),"<":(-1,0)}
        room, moves = data.split("\n\n")
        moves = [DELTAS[m] for m in moves.replace("\n","")]
        room = modifier(room)
        xdim,ydim = len(room[0]),len(room)
        walls,boxes,pairs = set(),set(),{}
        for p in product(range(xdim),range(ydim)):
            x,y = p
            if (cell := room[y][x])== "@":robot = p
            elif cell == "#": walls.add(p)
            elif cell == "O": boxes.add(p)
            elif cell == "[":
                boxes.add(p)
                boxes.add(p2:=(x+1,y))
                pairs[p] = p2
                pairs[p2] = p
        return robot,walls,boxes,moves,pairs

    def silver_mover(nxt,dx,dy,boxes,_,walls,robot):
        look, dst = nxt,1
        while (look := (look[0]+dx,look[1]+dy)) not in walls:
            if look not in boxes:
                # Cheat by moving one box from the back to the front
                boxes.remove(nxt)
                boxes.add((nxt[0] + (dst*dx),
                            nxt[1] + (dst*dy)))
                return nxt
            dst += 1
        return robot

    def gold_mover(nxt,dx,dy,boxes,pairs,walls,robot):
        moved = set()
        for m in (moves := AocDay15.get_moves(nxt,dx,dy,boxes,pairs,walls,[])):
            if m in moved: continue
            moved.update(AocDay15.move_box(m,dx,dy,boxes,pairs))
        return nxt if moves else robot
        
    def get_next(p1,dx,dy,pairs):
        p2 = pairs[p1]
        x1,y1 = p1
        x2,y2 = p2

        x1 += dx
        x2 += dx
        y1 += dy
        y2 += dy

        n1 = (x1,y1)
        n2 = (x2,y2)

        return p1,p2,n1,n2
    
    def get_moves(p1,dx,dy,boxes,pairs,walls,moves):        
        p1,p2,n1,n2 = AocDay15.get_next(p1,dx,dy,pairs)

        tmpboxes = boxes - set([p1,p2])

        if n1 in walls or n2 in walls:
            return []
        
        if n1 not in tmpboxes and n2 not in tmpboxes:
            return [p1] + moves
        
        # At least one of the two new parts overlaps an existing box
        if (don2 := (n1 == p2)) or (n2 == p1):
            return (m + [p1] + moves) if (m := AocDay15.get_moves(n2 if don2 else n1,dx,dy,tmpboxes,pairs,walls,moves)) else []
        else:
            if n1 in tmpboxes and n2 in tmpboxes and pairs[n1] != n2:
                return (m1 + m2 + [p1] + moves) if ((m1 := AocDay15.get_moves(n1,dx,dy,tmpboxes,pairs,walls,moves)) and 
                                                    (m2 := AocDay15.get_moves(n2,dx,dy,tmpboxes,pairs,walls,moves))) else []
            elif (don1 := (n1 in tmpboxes)) or (n2 in tmpboxes):
                return (m + [p1] + moves) if (m := AocDay15.get_moves(n1 if don1 else n2,dx,dy,tmpboxes,pairs,walls,moves)) else []

    def move_box(p1,dx,dy,boxes,pairs):
        p1,p2,n1,n2 = AocDay15.get_next(p1,dx,dy,pairs)

        # Remove
        boxes.remove(p1)
        boxes.remove(p2)
        del pairs[p1]
        del pairs[p2]

        # Add
        boxes.add(n1)
        boxes.add(n2)
        pairs[n1] = n2
        pairs[n2] = n1

        # Returns any sub-boxes that were moved
        return set([p1,p2])

    def run_robot(self,data,modifier,mover):
        robot,walls,boxes,moves,pairs = self.parser(data,modifier)

        for dx,dy in moves:
            if (nxt := (robot[0]+dx,robot[1]+dy)) in boxes:
                robot = mover(nxt,dx,dy,boxes,pairs,walls,robot)
            elif nxt not in walls:
                robot = nxt

        seen = set()
        gps = 0
        for b in boxes:
            if b in seen: continue
            other = pairs.get(b,b)
            left = min(b,other)
            gps += left[0] + 100*left[1]
            seen.add(other)
        return gps

    def run_silver(self,data):
        return self.run_robot(data,AocDay15.silver_modifier,AocDay15.silver_mover)

    def run_gold(self,data):
        return self.run_robot(data,AocDay15.gold_modifier,AocDay15.gold_mover)

if __name__ == "__main__":

    silver_tests = ["""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
""","""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""]

    gold_tests = ["""#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^""",""""""]

    data = """##################################################
##.#...OO#O...O.O..#.#O.............O...O.O.O.OO.#
#O#O.....O...O..O#OO..O..OO....OO........#..#....#
#..O.O.O...OOO..O..#.#..O.OOO....O.....OO#.O#.#.O#
#.....#....O.O..#.#.O...OOO..#...O...O....OO.....#
#O.O#.....O....O#.O..OO.O...#O.........O...O.O.OO#
#..O..#OO.........O.#...O....O..OOOOO.O....O..O.##
##O#....OOO......#O#.#.##O..O...O.O.OOO#.........#
#O....O...O...O#OO.........O.........O.O.......O##
#......OOO...OOO.O........OOOO.....O..O.O......O.#
#.O....O#...#O.O.OOO...O...O..O...#OO.........O..#
#....#O..O.O#.............O...O#.O.#.O....#......#
##..O..O.OOO.O...................O#...O.....#...O#
#....O.O........O.O.#O.OO...O....O.....OO....O...#
#O...O.O....OOOO.O..#..O..O.#....OOOO#.....OOO.#.#
#...#O.........O......OO..O.O..#...OO#.##.#...OO##
#...O...OO.#...O....#..O...........#.......O#.O..#
#....OO.......O...##.#...O..O.O..#..O.....O.O.O..#
#..O.O...O....O..O....O.O..O.O.O.......OO.....O.##
#O..O.........O.......O.O.O..O#.OO.O.O.OO......#.#
#OO.O..OOO.....OO.#..#....OO..O.#.#.O..O.O.O.O.#.#
#..O...O.....OO..#..O...#....O..OO.#O.O...O.O..OO#
#.....#OO.O...O...#O..#..OO...O..#OO...........OO#
#..#O...O..#.O...O#.....#O.OOOOOO...#.O.O.O.O..O.#
#O......##.O..O........#@.....O..O#......O..OO...#
#......OOO..O.......#.....OO##...O.#O...#.O..O...#
#...O..O.....OO.O.#O.#..O.....O.O...#....O..O....#
#O....O.O..O..O..O..O..O..#...O.O.....O#.O.#.#OO##
#.O.....OO...OO#........OO....O...O....#........O#
#.#.....OO..O.O.#O#.##.O..#O#................OO.##
#.........O#OO.O.....#..#...O#O....O.O..O..O.....#
#OO....OOO.....O.............#OO#...#....#.O.....#
#.O#.....O#...#.O..O...O...#.OO..O...OOO#..#....O#
#.#.O.O..O......#...OOO.......##.O..OOO#.O.O.....#
#.........#.......#..O.OO.#.OO..O..O.....OOO..O..#
#..#...O#O...............OO.O.O.O..O..OO.....#.#.#
#O#.O.O.#.O..O#...O..O....O....OO#O.O.OOO.#..O...#
#...#.##........OO.O.O..O.....O.O#OO..O.O.O.##O..#
#O#...##.#...OO.OO.#O..O..#OO..O.O......O.O......#
#.OO....#.O...O........OO..O.......O.O#..O.......#
#O..O..O...O...O......OO..O..O.OOO.#...O....#O...#
#.....#...#...OO.O...O.#..#..#OO..........O.O.#O.#
#....O......O#.O.O...#...O..O.O.....O.O..O.....OO#
#..O...#.O..O.O...O......#.#OOO..................#
#.O.....OO.O...OO.......O.#...#...O....O.....O...#
#O##O.#..OOO...#......O..O..#OO.........O..O...OO#
#..O.O...O....O..O....#O.......O......O..OOOO##.O#
#..O.#O..O.OOO..#O.......O.#.#OO.O.O.O.O..O.#..#.#
#.....O.OOO...#.O.O..O...O.OO...OOO..#.O.O.OO.OOO#
##################################################

<v><v><><vv>v<v<^>><><>v^v>v>v<>^v<<>>v>>v>v^><>><v^v><v>v^v>v<^vv>vv><>v^^v>>v>^>>^v<v<^<v^^^<<<<v>>vvv<v<vv^><<>>^>v^^v>v^v>>^vv<^>^v>>^^>>>>v<<>^v>^^><^v>^<<<^<<<v<<v^>>^v<>v>>v<v^^v>v><<^vvv<>>v>>v^^^<vv<>^><^>^<<>>^<>v>v<v<><^>^v>^<^<^^^v>^>v<v^vv^<vvv><v><v><<^<v<v>vv<>>v>>^^v>v<<^<^v<<<^>v<<<^><>v<>v>vvv^^^<v><v^<vv>v^^<v^vv<<^<^v^>v<vvv^^^^<>v>>^>>>>^<>><>v<^^<v<>v^<^v<^v^^^v<><<vv<><vv^>v<><vv^>vv>vv^>vv>v>v>>><v>vv^>v^^v>^vvv^>^v^^<<<^>^>>>^<>^>^v^v^<>v^>^<vv>v<>^^v>>v^<>^><vv^<<<>v>^>>^<<v>vvv>><^><^^<v^>v<^>^<><^><vv<v>v<^><>^^>v^<v<>>vv^><^>v^^<^^vv^>vv^^v>>v<^^v^v>><v<v^^v^v^vv>>^^vv^^v^vv^v<^^>>><><^^<<>v><>v<^^>^<^<v><^vv>v>>>v<<v<<^^>><^>>^^v^<v<>vvvv<vv>^^<>><>>>^^v<><>>^<<<v<<v^^>>>v^>^v><><>^vvv^>>v^^^v>^><v^v^><^^<>v>vvv>vvvv>>>v<^v^^^vv>>v><<v>^<>>^<v^<v>>>v>^v<<^v<^^<^<^vv^v<>v<v<>>v^v<<^^^v>>><v>v^><v<<>>vv<<<v^>^v^^v^>^^^^>v^v<<^^v^>^<>^<<<<v><<><><<<<^vv<^v^<^>>v>>v<^><^>^<^v<^v^>^^v<^^^v^>^><^v>>^<^^^>^^^^v<><<^^<>>>vvvv<<^>v>^>v>^<^v<^^v^<v^><>^^^<^>><<^^><<
>^><<>vvv^<>>>^>vv<v^v<<^<><<><<>>^>^>v>vv<v<vvv<<<vv<v><^^><^>vv^v<v>vvv>^^^<>>v^<v<^v<>>^<vv^<v^^v<vv^<<^<>^v><v><>^^>>>^<^v><^^^><<vv^>^>v<<<<>>><>>^>v^^vvvv<>v^^v><v<>><>v<^^<>>vv^v<^<>>>^^^<^^>vvv<^<<v<><v>><^^<^vv<v>vv><>v<v><^^>vvv<><<>v<<^<<<<^v>>><<v^vvv>><v><v><^^^>vvvv><<>^<^>^^>>^^<<^^v^^<<^vvvv<v>vv><>>^v>^>v^<<>>><v><>><<>vv><v^><<v<>><>v><<<>v>v<>^^^v<^>^<^<^<>>>><>v>vv^<<<^v^<<^<>^<v>^^v^>>v^<<^^<><><<<^>>><><v>vv^>v^>><^>>^v>>vv^<v^v<v<v><<^vv<<vv>^vv<v^v>v>v>>v^<vv^<v<>^>>v><>>vvv><>>>>v^<<^^<<^vv>^v>v<v<^<^^><<v>^^>>^<^<vv>>><^vv^^^>v<^^<>v>^^^>^<<<><>vv>^^<^<^<<<vv^v><^>v^v^<>^><^v<<>^>>^v^<<v>v^><v^^<^<<v^^v>v<><v>vvv^<>^v>>^^^v><>>v<<vv^v<^<>^<>>v<><<v<^>^<^v^^^vv><^vv>>^<>>>v<vv^<v^<^>v>>^<v<><>>>>><>v><v^<v^<v^<>vv^v<v^<v^^<v^<>v^v^>vvv<>^v<><^>>v>^<><<^<>^<v^>><^^v<<<vv^v^<v^>^><^^v><><v>v^<<<><v^>v<>^^<<<><>v<^<<<><^^>^^v<<v>v>><<v^vv^>^>^vv^v>v<<v^<v^<<>^<v^><>v>>v><>^v^<^vv<v^<vvv>vv<^vv>v<<>v^^<^<<>^><^^<^v^<v<v>^v<v<<<>^^><<<v<v>v>v><>^<<v^>v<vvv>^v^vvv<<<
vv^^><^>v<<vv<<vvvvvv>^>v^><^<v^<><^<v>^v>^<>^^^^><<>^^>>>^>^<>v^<^v^^v<v>vv><><<>>^>>>v<vvvvvv<^>>v<<><<>v^^v<v>^>^<v>^v>vvvv^vv<^><^<v^vvv>>>vv^v<>^>^>^>vvv^><v^<v^>^^^v>>v<^>><<^^v^<>v>><^v<v>v<v<<>^^vv^^v<<<<vv><>>^vv^<^vv<>>v^>vv<^<v>><<^>^>>>^v>vvvv^<v<^^<>vvv><^v<>^<<v<>>v<<^^><v<<v^>>><vv>>v^^<<>v>v^^^<<v<^>v^>^v<^<v^^>><<><^<<<><>^^<v<<><>^v^>>^<>>v>>v<<vv^vv>>>^>vv^v^<>v<<v<<^^<^^<<vv>>>^>v<v^^^v>^<^^<^<>vv>v<^v^><<vv^^^v>>>>^^^>^<v^>>>>^><>><<v^><v^^<<^><v^^<>>>>vv><v^^vv^v>^v^><>v^^<><><^<><<<<v>>v<^>^vv^^v^<^>>>>^v^^^<v^v<^vv>vvvv^^vv<^<>><vv^^<^<>^^<^v^^><<>>^v>><^>v^vvvv><<^v>v>>^v^v<<>v^<^^<v^v>^vv^v<^v<>^v<vv>^>vv>>v<v^><^v<<>^^<v><^>><vv><>v<>^>^>vv^v><vv<v>vv^<<>v>v^^><>vvv>v^<<>^v<<>v>v>>><v<^^^^<>^^v<^vv<v<vv>vv>^vvv>>^^<v>v><^vvv<>^v^<^vv^<vvv^v^v^^><<<>^vv>>>>v><v^<^^^<vvv<^^^^<><>v^v>>^^^^v^>^<v<^^^^>^^>^^><^<^><^<<vv^<vv>>vv<v^<v^^><>^>>><^^^<v<vv^<<^vv><><vv<>>>v^>>v<>v>>>^v^>^<<<^<>v^>^v>>^<<v^<><^<>>v^v<^>^><^>v>><^v^^^>v^>^^<^v^^v>vv>v<^^^<^><^vv^v>v<>v<^vv
^^>v<><<^vvvv>^v>>><^^<vv>v>><<>v>vv>^>>^^>>^><<v^<<><vv<<>v><<><>vv<v><<vv<^<^><v><>^v^<>v>^^>v>^<<<^<>v<<>v<><>v<<v><^>v<<^v<<^v>>v<^<<<^<><^>>^<>^^>>^<v^>^vv<>>^v^<><>^v><<<<^^><^^>>^^^>^v><v<><<^>^<<^<^^<v^>^vv>^>^v<>>>><^v>v^^^>>><>^<>>^^<vv^v>^>>><v>v>><^^v<^><vvv><><>v^><>>>^v<>>vvv><>v><<v>>>v<>v><^><<^<v<>v<><<^><<^v>>^^>><^^v^><v>vv<<^><><v>^>><^><^<^>^v><v>^^v<^^<v^<>v<vv><^<>v^>^^<^v>^<^^>v><<^>^>v>^>^><>^<v>>^<v<^>v<^vvv><v^v<^v^>^v^^^>>>vv<^<>^>>>>v^>^>v^vv^^v<^^v^^>>>^^vv>v>^v<^^v<vv^^>>v^^^^>^^>^^<vv^>v^v<><v^vv^vv><^<^><<<<<<v><<>^vv><vv>><<<v<^^<^<v><^><>>v>>v<v<v>^^v<^^<>^^v<>>v<>>><^>^<><<v<><>^^v<<vv><^v^<<<>v^<^<<^vv^^^<<<>v<^^>^^v>>>>v>>^>^>^<^v^vv^^<>v>><<^v<>v>>><<v>vv^><v>>^^<><<>>>>><^^^<<^>vv^v>^<>>^^^v><v^<<>v>^>vv^<v<^<<^v^v<^<<<vv^<v<vv><^^^><<v<vv^v><<<v><vv<vv<>^^^^v^^vv>>vv^v><^vv<^^v^v<v^>v<<v^>v<>^>>>><^>^>>vv>^>v^v<<<<<v<v<^<>^>vv^<^^><^<^<<>><>^>>>^v><^<<>>^><><<>v<<^v^^<^>v><vv^^vv>^^>^v>>^>vv<<>>>>v<<^>>v<^<><^<>^<<^^v^^<<v><<<^v>v<^>^v<<^><^<^v^
^>v><>^>v^>^vv^^v<<<<><^^<^><<^v<v>v<<>>>><>^^^v><>v<^v><<<<^<>v>v>^>^><vv<<^>^<><vv>^^>v<v>vvvv>^^^<>vv^>><v>^<^vv<<v<<^^<vv<^<^v^vv><v^^vv^<^>^>^^^^>><^>v^v^^v^<vv^>>><^^^v<^v>>v^<^^v>v>^v>^<vv<^v^v^vvv>>v^><v^><<<>>v^^><v>v><<<^v><>v^^vv^v>>v><>^^^v<v>^<vv>v>^>^v<>><>>v^<><><^vvvv^>^^<>vv<v<<>><<<>><<<<>^v>>v^^^v>vv<<v<vv^<v>><>vv<v<<<<><v^<>^v^v<^>><^<<>^>v>^>v>^>^>>>v^>v>v^v^^^v<^>>>v>><<<<v^v<^<v^v^vv>vv^vv>v^v^><<^<><<<^^>vv<<^<^<v<vv^v>vv^<^^>>>vv^><<<^<><>^>>v<^^v><<<>v^v<<<^<<v<<^v<^v^^^>^<^^<<vv>^<^>^vvv>^^><^><^v>v^>v<v><<<><>v^vv^v<<<<>v^<^^v>v>v^^>^v>^<<>v<^<><^<vv<^<>>^<>>^<v^^vv<<<v<<^>^><^^vv^<<<^vvv^^^>^v^^v^<><^^>^^<^<><>>><^v^>vv^>>><v^v^>v^<<>v<v^<vv>^<^^^<<>^<v^vv>>^^<v^<>>>>^<>v<v<^^><<>v^^<<<^>>^v^^<>>v><v>^v^v^>>^^>^<<<>><<>^^>>>^^<>><>><<<<^<>^>^v^^vv>><v^^<v^><<v>>><v<<<^><>^<<>>v<^v<v><>><^>>^>^<<<^v>^>v^>vvv>>v^^><>>v^v<>v<<v^^>vv><<<^<v^>vv<>^v^^^>^>^<>^>^<v^<>^vvv<<<>^>><><^^^v^<^^>v^<v^<^^v^>^<^^<>v<<>>v>^>^<<>vv^^^<>^v>v^<^v<<v^><v>>^^<<vv<<>>v<<><v>>^v
<^>^vvv>>^vv<><>v<v><^>>vv^v^v^<^<<<^<vv<>v>><<v<^>><vv<<v>vv<><>v^v>^><^>>^v<^<<<^v><><><<v^<<<^^<vvv<v>vv<^<v<^v<<><<^v^^v<^<><^<<><<^v<<<><<^v<<^<^<v>^>>v>>>^^>>^vv>>^>v<^v^>^<^<v<^<<<v^v^^><v^^><^<>^v^^><v<>v^><^<<vv^v>v<>v<>^<v^vvv^^v<^^>v^><>><^^>vv><>>v<>>vv^>v^^vvv<v<v>>^v<v>>v>v><vvv<>^>><^vv^<<^>^>^vv^vv<>v^<vv^^><>vv^<<^><^v>>^^^>v^v<><>><v>^^vv<><<^<^v^<>v^v>^<><<<>vv>^<^^>v<>>v>v<^<<>^v<>>>^<v>^>^^<v>>^<<^><v>>v^v<vv>>>^<^v^<^>^<v>><vv^^><^>v>^>^^>><><v<^<<v<v<^^v^><^<<^v<>v>^^v^>v><<<<^>^v<v<v^^^>v>>v^vv>v^^>^><<>^<^<>vv<<v<^^^>><^v^v<v^^<^v^<^^v<^v<><^^v^<^<^^>>^>vvv^<<<^v<<<<<^v^^<>^<>v<<v<^>>^>^>vv^v<vv<^v>vv^v^v<>>^>v^v<v^^v>^v^v^^v^^<<><<^>><>^<>v^<<<><<<^vv>v<vv^>v<vvv<<><<^<<vv^^^v<vvv<^<vvvv>v>^>^v<>>><><^<vv<<v<^<v>^v><<><<v>^<^<<vv<^>v>^>>vv^^>>v<>^vvv>>v><^<<v^v^^^>^>v<><>><>v><<<>v^^vv<^>v<>>^vv>v<^^>v>^>v<<^<^<><v^^<^><v<<<>^^vv^>><v<v<>>^>^^^v^<>^v>>>v^v<>^<<^>>><<v>^>vv<>v>v>^vv^vv^v<v<^^<>><>^v^>^>v><^^^>>^vv^>v>v>v<vvv^v^><^>v^^^>vv>^^>><^^^^<^v<v<><v>^>^
>vv^^vv<^vv>^>^v>^^<^^^<>^^<<^<v><vv<>v><vv^v^<>>vv><<^^<<>^>v^<<v^v<>v^v>v>v<^^v<<vv<>^^<><v^<>^>^<^>><>v^^^>^vv>v<<><v<<<v>><^v<^v^^<>>v^<^vv^<^v^v^^v^^^>^v^^><^><^>^><v>^v>^<>v^v>v^^^^>>v<v<><^^v>><<v^<>>>>^v^v>vvv^v><v>vv<^^v>v<^<vv^<<v>>vv^>v<^^<<^<^v>v^v>>>v^v^v<v>v^v^>><v^>vvvv^>v><^^vvv<vv<<<><>^^<^<>><vv^vv<^>>^v<v^<>^^v<v>>>><v<>v><^v^^<<v^>><^<^v^^>vv<<<v><v^>v>v<vv><v<<v^<^>>v^^<<>v><<<v><>>>>vv<<^v<v^v^v<>>vvv^v^v<^>>v^>^<v><><>><>^<<>v^vv><<><>^^vv^v^^v^><v<<^^>>v^v>v^>>^<v>^<>v^vv^^v^v>v<>^v^<^<>v>v<^v^><vvv^><v<><<^v<>><^v^>>^v<<v^^<<<><v<vv^><><^>vv<<v>^>^<v<^v^>^vv^><v<^>>v<^v^vv<vvv<<^^<<<v><<^^v^^<^<>^v^><><<^^><><<<v^>><>v<>>v>><^^v<v>>vvv>vv>>>><>vv><v<<vv><vv<<^v>^^^>vvvvv>^^<<<v>^vv^^><^<^>^vv^><>>v<>v<^>v>>v^^><^v>>v<>vv^^v<v^v<v>^><>^^<>^^<^>^<>><<v<v>>><>v>vv^<^<<>>^>^vvv>v^><^<<<>><v^v<v^<<<>^>><v<^<v>v^<^>^><v>^><v^vv^>>v<^^^v<<<v<v<v>v<<^<vv^vv^v>>^<>>>v^^vv^<<^><^v<>><^<^<<<^<^v<>><^v^<^v^<<<vv<v^<^<^^v<>v<>vvvvvv>>><>><v>^^<>^>><v^vv^v^>vvv>^>v<v><v^>^vv
<<vv><>v>>v>>vvv^>v><<<v>^>^<>^<<^v><^v^v<<v>^<>v>^>vvv<><^^>vvv^v^>><<><<>^<<<><v^^>vvvv>vv>^vv<^>v<>v<^v>v<^^>v<^vvv^^<<<vv<v<<v<v>vv>v><v>><v^v^<<>>>v>^^v^>v^^^>^><<v^vv^v<^v<><v<^<^><vvv>>vv>v^<vv^><><>v>><^v><>vv^^<vv<^v<>>v>^<<^>>>^>vv^<><v<^>v>vv<v><v^<<v<^><^>>><v<^<>>^<v^<<^>^>^v^<<v^v<^^v><>v<<^<v^vv<^>^^^^<>^vvv<<^>>><^><^<v^^^v<>^>^vvv<>^<<>>v<<^^<v^<vv>>^>><^v^<<^^vv><vv<<^v^>><v^^<<v<<vv<<^vv<<vv^v>>^^>v>>v^v^^<v>^><<>^^^>>^v^<v<^^^<v<>v^^v>^>^<<^>>v^v^^^><>>>v^>>^<^><<>^v><<v>^<^>v>><<>>>>v<v>^><^^>>^^>vv>^>^<^v>v^v<<><^v^<^vv>^<<v><<<<v>^v<vv^v>vv<<<><>>><^v^>^><^>>>v<>>^v>>^v^v^>>>v<<^><>v<v<^>>^>^<^><^<v<<^^v^^><vv^>^<><vvv<v<v^^^<v<^><vv^v>>v<<>^<>vv^<<><<<^<>^vv>v^>^v^v^<^<>^><^>>v^^<<<v>>^><<>><<v>><^<<<>^><>vv><^v><<>v^^^^^^>^vvv^^>v>v<^vv^^<<vv>>v^v^>^<<v<v<v>vv><^v<>><^^>>^^<v^<^v>v>>v^v<v>>>v^<>v><^^^<>^>^vv<^v>><^v^><v>>>v<v<<<><<>v^v<<v>^^v^v^<<>^><>v^^><v<vv<^<^^<^v<<>^<^<<^v<><v>^>^<>>v>>v^v<<^^^^<v<>><>>v>><^><v^>>^^>^^<vv^^<<^^>^>^<vvv><<>>vv<<>>><^vvv>><
<<^vv><v><>v><>v^<>>v^v<v<>v^^>vv><>v>>>^v^^>v<^>^^<><^<^<v^^<<>>>^^v><>^<vv^vvv^^vvvv><><^^vv>>^^<^<v<><^^^v>^v^>>^<v^>^^^><<v>><^^>vv<^<^vv^>^>^>^><^v^>^^><v>^<<vv<>v^<^^<vv<<v^^v<^>>^>vvvv<^^<><><vv<>v<^v><v^<<vv>>v<^v><v>^v^^v<^<>>^>v>^<v<<>>>^v>^><<<v<^<vv><v^v^v>^<<><^v<<>^>^vv<<^v><>vvv>vv<v^v>>^<<<v>>v>>>^<^<v>>^>^>^><^<>^>>v><^<v^^<v><>^^<^<^^<^v^^<><^<>>v<^>v<^<v><^v>^>v^>>v>v<<><><<>^<<>vv>v<<^v^^^><v^><><v^><^<<vvv>^<^^vv<><<vv><v>v>^v><v^<<<<>v>v>v<v<v>^>^><vv><<^>vv<>vv^^>>vvv^><><v<^>>^<>v><>vv>>><<>>^>^<<<v^<<^>>>^^^><>>v>>>>>v<>vv<><<^vv>^<^<vv<>>v^vv>>^<^v>v^v^<>>^>>^^<<><^<<>v<<>>>^<<<>v^^>><<vv<>v^v^>><v^^>>^<v^v<vv>>><<v<>vv^v^<v<^vv<<vv>v>^^v><><>v><<>^^<^^^>^v^^>vvv<><><>^><vv^<^v><><<>>v>>>^v^<^v<<<<v>v<><<<>>^<<>^^<<><><>v><<vv^>v^<v<v^vv<v>v>v^^v^v^^v>vv<v>^^>v<>v^<>v>^v^>^>^<v<^^<^v<vv^^>v^^^vv>>>^v>vv>v^^vv^^v^^v^>>^>><^v^>^v<^^>^>>^>^>>>>>vv<>v>^><^^^vvv><v^<^v^<v<>>^vvv<v<>v<<>v^v^<^v<<>>^^v<><^^<vvv>^v<v^^>^v^>><v><^<<>v^<v<>vv>>>><v<>v^v<^<><v^v^vvvv<^<>
^>><>^v^vv<^v^v<^>>vv<<^^^^<><^>>><v<v>^v^^>^<>>vv>vv<><^>>v<<<><^<><^<>^<<><v^<v><v^<^>>>v<^^>^<>^>^<^^>><^>^vvvv^^v^v^>^<>vvvv<>^<v<^v>^^>^<<^><<v^<><vv<^v<v^>^>^<<v^v^v>vv^><<^<v<<v>v<<^>^<>>vv>v<>>>^>v^v>><>>>>v>>^<vv^>^>>vv<vv>v<<^><v>>vvv<<><^^<>^>v^<vv><vv><<^<>^<>vvv><vv^>^vv^vvv^^>^v>>^><vv>v<v^^<^vvv^<<><^>>v^<^<v<<^<vvv<>^><<^><>v<<v^^^v^>v>^vv>v^v^^^>><^>^<<<>^<>v>^^v>v>v<>^vv<<v^><v><><^v^v>^<v>^<^<^v<^vv^>v^^v^>v>^<v<<v<>^<><<v<<<>><v^^^<>^>><>>><v>v<^vv<^v^>>>^^^^v^<><vv>vv>^^v^<v>vv^^^<v>^v>v>^^v<v<v^vv<>><<^^<<^<v^v^^^^>vv^><vv<^>>^><v<vv>^^<^<^^>^^<<<v>>v<vv>v<>>>>v<v>^^^>>vv<^v<><v<<^<>^v>^>v>>^<<^>v<vv><<v<v^>>^v^>>><v>>vv<<<v>>^v<<><vvvv<vv<^<<vv>^<><^<^v<<>v>v^v><vv<^>^>>vvv^^>>v^<vv^<^^<<^>>^>><^>v<<^<>^vv<><^v<^>vv>vvvv^v>^<vv<>vvvv>>>>>v>v>^<>vv<<v>>^v^v<v>>>^vvvv<v><^>vv><>>v>^<^<<^^<>vv>v<^v<^<^><v^vv<>><>^vv<v^<^>^^<v^^>^vvv^>^v^v>v^v><<<<<vv<^^vv^^<>>>>vvv^<^>v^<^>>vv^>v<>^v^<v>vvv>><<>^<v<^>v<v^>^^<v>><vv><v^^v^v<<<<<<<<>>>>>v<^^^v<<^^v^<>v<<<>v>^<>>^^^>><
><<>v<^<<^v>v^^>vvv^>vvv^>^v><^<v<^<^^<v^v<v>>^><>>vv^<>^>><>^v^><<><vvv<^^^vv<vv^<><><<v^<^v>^^v^<<^<>vvvvv<v>v^><^>v<<^<^^<^>^>v^vv<>vv<>><<>vvv<>vv>^^^v<><v<<<>vv<<>>v^^<^<v>^v>v<<vv^^vv<^<<<<>>><^>>vv<<>^v<<v>^<<v^vv><v>^<^<>v<^vvv>>v>vvv><vvv^<^v><>v<v^<v<v^^^><^>>><vv<^v>^v<^>v^v^v><^>^><<>v^<vv>vvvvv^<v<<vvv<^<>>v>^<<v^<<^^>><v>>vvv<<<>^^<^>^^^<<<v^><^>^>>v>v<^v<^>vvv>vvv^v^v>v>v<^^v<^v>^>><<^><<<><<>>^<<<<^<v^vv><<>vv>^v>>vv>^^>>^<>>^<<<<>v>^^^<^<^<<^^>^v^v^^vv^<>><^vv^>>v>^>>>>vv>^><<v<v^><^v<>^<>>v<v^v<^<v<^><<<v><^<<v>^>><^<><vv<^<^>v<^>v^^v^v<<^>^><vvv>>><<v<<><vv^vv<><^v^>>>vvvv<vv<^v^>v^^v<<<^^<<<v>>^<>^v<<>^^>^^v^<vv^<<>><^<^><>><^^<vv>v<<v>vv<><^^v><<<^v^^>vv<^<<^v^v^^>^><vv><>^vvvvv>>>>^v>><^<><<<>^>v^^^><><^v<^vv^^v<^>>>^><^^<>>v<v^^<<<<<>^v^^><^<<<>^<>^v<>>><>v><<<^vvv<^v^<<v^v^^<v<vvv^<^<^^<v<v^<v^vv^<^vv>v><v^vv<v^<^vv>v^><^>vv>vv<^<v<v^<^^>^<><><<^>^^>v^<^>^^v^v^^<<v^v^v>>v<>v>>^v>>^><v<^v<v><<<><<<v>^v><><^<^v<><<><<>v^<<>v<>vvvv<><^^^<<^^>^>>^>><v<>vv^<<^vv^>>^<
<^vv><v^>v>^v><>^<<^>v<>v><^<<><<^v><<v>^>^^<<v^<^><>>v><v>^<><^<v<v^>v<^v>>^^>v><>^>^v^vv>>><<^vv>^<>^<^v^>vv><v>vvvv>^v>>>>v^v^v^v^>><^v^>v<^<v<<^<<vv<^^v>>^>>>^>^^^v<vv>v^<^^>^>^v^^v>v<^<vv^^^>^<^v^v>^vvv<>>vv^v<<v^>^v>>v>^<^^>>>v><<^<<^<^v<v<v>vv^^>>^<^^><<<^^^>^^<>>^<<v<v><^vv>>^v<vvv<>v><><^<v>v<><v<<^v^^>vvv<>^^^><<<<v>^^>>>vv<^v^^>^>^v>>><v^<v<^<<v>^><>^^<<^v^<^>>v<^v^^^>^><><vv<v<v<^^>^v^^<vv<><<^v^><<>>^^^>^^><<<v>v^>^<vv<><<>v><>>v^<^<><><>^^^^>>^v^<v<>^^^<^^>v^^v<vvv<>><v<>v>^<>^vv<^<^^>>vv<<>^^>vvvv><v^v>vv<v>><^v^>^^vv><>v><>v^^><v>^>^^>^<v^^vvv^v>v<^>^<^v<v<vv^>^><>^v<><vv>^<<v<<<>>v>v>v^<v<>^>v<>v^<<^v>^vvvv^v>^vvv<<v>vv>><^v>^<<v<^vv^>vv<v<>^^v<v<<v<^^v^vvv<<vv>v<<<^>vv>v^^v^^^<<><^<v<^^<v^^^>v<^^v<><>^>>><><>^^^v^<>><vv<v><<>v<>>^>^v>^>vv^<<^v^^^<<^vv>>>>^^^^^^<<<<<^vv^v<<<^v<<<<><^^><^<<>>v><<<v^^<>^>>><^^v<^v>>><>v<>>v<^>><^>vv<^><<v>v<<>^^^<<<v^>>>v<v>^<^>>^v<>>^^<^v>v^vv>>^vv>^>>v<<><>^><<>vv<^v><v^<vvvv<^^v<v><^>><^<^<^<<<v<v<>>^vv>^<<^<v^v>>>vv<v<^<v^>v^v>^^^<v<
<^>v^^<v^<v^>^>vv<<^<^vv>v>^><^<<vv><^^vvv^>^><v<^v<<^>>v<vvv<v>^>^v>vv^^>^^><v<>>>vv<<^<^v^^^^>^^vv<<<>><^v<<>^^>v^<<v>>vv<v>vvv^v<v>>>vvv>vv^>^^^^^>^v^<<><v<^v><v<v^v>^><v>>v><<<>v^v<>>v>v>^>^<^v>v^v<v>^><>vv^^^>><v<v<<>><>^v^v^^<vv^<^<<vv<^^>>v>v<>^>^^v<v<vv>^>vvv>v^v^><>>^<v>>v^^^v^>>^^v<<<<v>^^>^<>v^v^><v<>v<><<vv>^^^^<v<v<v>v>^^<<<>^v^>v<<<^v^>>^<>^v<^^v^<^><<v^<v^^^v<v^^^^^>^^^v<>>>>^>>v^><v^<<^^^^<^<>v<<<^^>>v^<><v>>v^<>^>><><><<^>^<^>>^v^vv>^<^<>><v<>^<^^^^>^^>^^><v<>v>>><>^^<v^^^^vv<vv^^>^<>v><><^>^^<><><<^<vv><>><^^>>^<v<v<v^<^<<<^v>>v>v>^v^v^^^<^vv<<v<vv^<^<v>>^<v^v>v^>>v<^>^<<><<^<><v^^v><>^v>vv>>>vv><^<v^<^^^^>v^v<<v>>v<>v<<^<><v<<^^vv><><^>^<vv^<<>>>>vv>^>>^^>vv^>^<<v<<^v^><^<>^^^><>v<<>><<>v><^><^v<>^><>v><^<><^v^^vv>>v>^^<^>^^<<^^<<<>^>^>^<><<^>^vv<<^>^v^v<v<>>v^<<<<^>v><>^><v<v>^>v<>^v>>>v^<><<>>v<<<v<<><^>v<vv<v<^>v<^^v^><<>^<^^v^^>>><>v<<<v<^<vv><v<<^<>vv>v>v>v^<>>^<^^<^>vv^<^>^<>^>^vv<vv<>>^><^v^v^>>vvvvv<^<v<<^<^><v<><v>^^vvv<v<^^<>>v^^v<<vv<^^v^<^v><^<<><^><^>^>v
<^vv^>^^v^<^v>vv<><<v<^>><v<><<<>>>vv^>^>vv<v<<^^>^^v>v^>^^<<v^v>^<v<<^^<v<><<v^v>^>v^v^vv>>vv<v^>v^><^<^>>>^<<vv><vv^^v^<<<^vvv><v>v>><vv^^>^<^v>v^^>>>><v^<v^<>^vvv<v<v><<>^v<^<<>v>^v<vv<>>v<<^^<v^^v<v<<<>>v><>^v><<v^v>>^v<><<<^v^^^<v>^v^<^vvv<><>>><^^^^<^^^v^v<^>vvvv>vv^>>v<>vvv<v<><>v>v<^vv>v^<<^^<><>v<><<>>>^<vvv<>>^<<>>^vvv>^v>>>>v^>^^<^>>v>>^v^v><^^<>vv^>v^<>v<^>v><<^>^^<>^^v><<<<^v>^v^^^^^v^><v^<^><^^>>>^<^v<^v<>v<vvv<v>^>>v<v<^v>>^>>^^>>v^<>v<>^>v^vv>v^^vv^><>v>^><^v<>>^>>^><>v^^>^^><^v><><<<<><vv^^v^>^<<>^^v^>>><vvv^>^v^v^><^<>vv^vv>^<vv<>v^v>^^<>>vvvv^v^^<^><v><>vvv<<><vv^>><<<^^<<^<>>^>^<>>^<<^^>>>>vv>><v^v^<v^>^<^vv<>v^><>>><vvv<v>vv>vv<v<v^^<>v><>vvv<^^^>vv><vv>>v<^>^<>^<<<^<<^^>v>^vv^>v<<^^^><^>^v><^v>vv^^^v>><v^<^><<^<>><^>v<>^<v>v^<<v><^>>^<<^<vv^><<^^vv^v<vvv><vv^^^<^^^^<vv><<v<v><^v<v^<^vv^>^^<><<>^^^v^<^<<^^v<^><^<<<><><<vv>>^>>>v<<^v^<v><^vv<>><>>^^v<<v><<>>^<>>>^<>^vv<<>v<>vvv>v<^^^v<>>v><^v^^<^^>v<><<^<<^>^^vv>v<v^v><>^^^vv^^>>^vvv>>^>>^v^^>v<>><^><vvvv<><v><^v^>>
<v^<^v^^>><^>v><^^<><>v>^>v^<>v<<vvvv>v^^>>^<<vv^vvv>^v^><^>^>>><v^^<>^>>^<v^<^v^^<v^v^>v<>v^<vv^><><v<^<v^v^^><v<^>v^<<<><^v^^>v><>v^<vv<>><^>>^^vv>^^>>vv^<<<^v^vv^>>^<<v>>v>^><vv^^v<^>>v^<^><^<^^^>^^>^v<<>v^<^v>v><<v<<v^>^v^>^^<v<><<^>^v^^vv>vv^^^v>^v>>vv^v^^^>^v^^^^<<<>^^vv^^^><<^vvv^v<vvv><>^<v^v^<v^^<^vvvv<^^<vv<^<>><<v^^>^v^^<^v>^^<v^>^^>>>^<>v^^vv^v^v<v>>><^<>^^><>v<>^<<>>>v<^^<<>>^>>^^^><<><><v^^v<>v^<><>v<>v^<>v^^<^v^^^<>^^v><<^v<v^v>><<>v>v^^v^<<>>^^<>><^^<<<>^v^><^<<^^^^>><^<^^<<v^^><><v><<v^>v^>>^v^>>vvv^^v<^^v^>>v^v><^>^>>^>vv<^><<^^^><>^<v^^v<<<<^^vv^^vv>>^<<<>^>>vv<<v<>>v^v>^^^<^<v^>>^<^>^v^>>^^>>^vv^><^v>>^><<>>^>>v^v<>^^v<<<<^<>v^>><>>v^v^^^^^^vv>vv<^v^><^<>vv>^v<><>vv><v>>^>v^vv^><<><v<vv><<<<v>>^^v<v>>^v>^^><v<v^vv^v^^v<<^<^^v^<<^><<>><vv<^><^>>v^<^^><>^^<>v<^<v<<>>^v^v>>>><vv>v><>>><><^<>^<><v<v>v^>v<>vv<^<<vvv<><v>v<v^v^v>^>vv>^>^^<>v^v>>^><>><<v><<v>>>>v^>>v<v<>v<<<>v><^^^>>^vv^>^v><^^>^^<v^^>^^v><<>v<^<^>^v^<>^><^>><>^>^>>^>^^v>^v<^>^>^><<><>^>>^<v<^>v^<^><v><>^>
v>>v^<v^>v^<>>><vv>v^<<>v<<v>>v><>^<>vv<^^^v<<v^v<^><>>>>>^^v^^<<<><>>^v^v^^v>>>><vv<<>>v^<vv><^^^>v^<v^>><<v>v<<<<>v<>>><<<vv<<>^^>v>^v<v><v>>><^<^><^<>vv>v<>vv<><v>^>^v^^v<<>vv<v>v<<<^v>^><<<>^>v><<><^<>^^^^v^>^><>><v^>>^<v<><>^^<^><>>v<v>vv>^<v^^>^<^^><^^<v>v^<^>>vvv<vvv>v>>><<<><<><>vv^^<v^>^^<>>><>>v>^>^<>>v><v^^vv^vv^<><^<vv>>v<^<<^^<<^>>v>><<v<^v<<<>^>>>^v^<v^<vv>>^v<^vv<v^vv^<v<v<<<v<v<^^<v^<><<^<v<<>>v>^vv^><^v<<v>^v>>v^v^><^<^^>^>vv>>^^<><v>v^^<v^^>>>v^>><>>^<>>>>>v>v<<vv^>v^^^^<v>><><^<^^<v>^^>^>^<<<><v^<>>v><<<>^v^^<v>>^>^><>^v>><vvv>v>^><^^<v<><vv^>v^<<<^v^^^v<>v><^^<vv^^v><^v><^^^>^<>vv^^v<vv>^^<<^^><><><<^>^v>><v^>^>>^^v>>^>>>v^<^<^<v<>v<<<<vv^^><<>^>v^^>^>vvv>>^v>^^^><><^<vv<><<<>v>v>v^<<^^<^vv^<vv^>>^v<<^<>^>>^>^<^^v<v<>>v>>^<^>^<^>^^<^>>>><<<vv>vv^^^<^<v><<^^<v^^<>><<v>^v^v^^^^vv^><<v<^<><>^v<^v<^>v^<><^^^>^v<>><^<^v<^v<^^>^<v^v^^^>v^><v>vv<>^><v>>v>v>^<vvvv<^>v<v<>v^<<<v<>v^^^^><<v^^^<^^<v>v>^>v>^v<^<^><<v^v<<^^v>>>><^<>v^><<v<^^^<v<<^vv>^^<^<>v^vv><<<^<<>v^<>^v><^<<
^<^^><v<vv<<<>vvv<v^>>^^><^vv><<^^<<>>>v^v<><v^><v>>>>>^<v^<>^><>vvv^^^<vv>><^<v^><v^^>vv^<>^^v^^v<v^v<>vv>^v^<<<<v>>v<>>><v>^<<>^>>v><^^^>v><<vv<>v<^<<<vv^^^<^>>^<v<>>^>v<><<<><><<vv<^><><><<vv<>>^<<v^>>v>>^<v<v>>><<><v><<><^<>^v^<>^vvv^v<^<<^v^<<^v<^v^^^^v<^>^^<vv>v^><^^^>v>v^>^<>v>vvv^<>v^v<^>>^^>^>^<>>^^<<^>v<<>>^>^<<<><^vv><>><><<^><v^vv<^>v>>^v>^^vv^^<v>^<<v<^<<<^<><v^>v>vv<^><^v^v>vv^>>>v>^>^>vv^>v<v>>vvv^<^v^^<<>><vvv<<v>>^<><<>^<^>^vv^>^vvvv<><<<<^^>v><^^v>^<>>vv^<^v>><^>>^>><^v<^^^>v><<^<<>^^v>vv><^>v^v<>><vv^v>^^<^><^>^>v<<><^<v>^<v^<v<<^^vv<>v^>^^vv>^<vvv<^v>^v><v^v>^<><<><<v>v<^>>v<>^>><v^<<><<><vv<^<>>^v<v<<>>><v^><<<vv<>>v^>vv^^^^<v^^^^vv<^v<<^vv><<v^<<><>^>vv>>^>^>^<>vv><<^^><v^vv<<^><vv^^<^<>^v>^<v<vv^^><^v>^^^<>^vv<v>v>vv>^^><v^^^<^^v<v<<vvv<>v><>>^>>vv^^v^><<<^^<v<v<v>>><v>^^^>^vvv^v<<^<>vv^<<>>><<^<>><>><v><^<v><^vv<^^<v^^v<vvv<<vvv><vvv^vvvv^^<^<^^^<^<^v><^^^<v>v^<<^^>^vvvv^<<vv<^^v^>v>vv<vv<>v^v^^v<^vvv^>>v^<v<^<><v<><v<^v<vv<v<v><^>>^><^v>^vvvv><v<>^^^vv>v^<><^vv
^><<^<<>v^>>v><vvv^v<^>vvvv<>^>>vv<^>>v<v^<<>^^<^<^^^^^^<<^<v^>v^>^^vv^^>v<^><^^><v^<v><<^v>v>>>^^<v>><^^>><<^^>^^^<v^>vv<><vv>>>vv^v^<>v<><^>>v^<v>v>^><<v^v>>^v^^^<<<>v^><v^<^vv<>>>>^>>>>^v^v>><<^>^>>^><^v^>^<v<v><<^>>^>^v<<v^<>^v^v<^>vv>vv^v^<vv<v>^^^v^^>vv>^^^>>v^<<v<>^^<<v>v^v^<v^v><<<v<vv<^v^^vv<vv^vv<<v>><^>v<v<<v>><v^^^<^<v^<>v^vv^>><^>v>>^><<v<^<^v^<<><>v>^<>>v><<^^vv<<v<>^<v^^v^vv>>^v><<>v>v<^<vv^^>v>^<^^<v^^<<v<^<^^>^<^v>>^<<v<>><v<v>v^^^>vv^>^<>v^>v^<<>^<><^>v<v<<v><^<<vvv>^v<><v^><><>>>^<<^<<>v<v<><<^<v<>v>vv>v<><<^v>>><v<^^v^<v>vv>>^<<v^<^>^><<<v^>>^<v>v<<>^>v>>>v<v^vv>^^v<v<<^<^^>^<>>vvvv^v>^^vv^<^><v><<^^><>>><<>^<v^^vv>><<^v><><v<vv><v<<><><vvv^<^^<^><<^<<^<><><>vv<>>^>^^vvv<v^v<<v<><<>^^^^vv<><>^<><v>^<>>>v^v<>^><<<<^<^>^<>vv<>^<v^v<>>><vv>v^<^<><<^>vv^v>v>^>>>^vv<><^>>>>>^^<>^>^^>^^>>vv>v>vv^^v<><v^<^><^<<>v>^<><^v<<><^v><><>^^<^^v^>^^>v^<><><^>v><^><<^vv<<<>^v^<<^^<^<><^<>^<><v<v<^<^<vvv>>><<<v^v^>vv<^>v><<><<^<^v>vv^<>^^v>v^>^<<>v><^<><<v<v><>>^>>v>v>^>v<>^<<v^vvvv>
^^^<><vv<><<<vv<^v>v>>v><><v>><<<v^^vv<><^v><>vv^<^><<<^v>>vv>v<>v<><>>>^^v>>vv<^^<<<v>^^^>v<<>^v^^<<^>^v^<<<<^^>>vv><>>^<v^^v^<<><>>>v>^<v><vv><<v<>^>^<<^v^<>^>vvvv>>>>^><^vv>>^<<^>v^<^^>vv^^>v<<>^<>>v<<^<vvv<^^^><>v>>>^><^^<^><^^<>^>v<>>><<<v^v^vvvvvv^<<^v>><<^><>>v<^<v^<^<>>><v<>vv^><v><^^>v<^vv><><<^<<vv^v>v^><v>^^v<^<v<v^vv>>^^<<<<vvvvvv^>v<>><v>>>^<<^^<v>>^<<v^><><>vv<v^^^<^><>^v^<v^vv^vv>><<^><><v^>^v>^v<v<>^v^v>v>^^v><<>v<<<<>v>v>^<><<><><>v<v^^>^vv>vv><<><<><v<v>^^^^^vv><vvv<><><>><<<>>^>^v>^^<^v^^^>v^><v><><<^<v>^><>vv>vv<^^v<^><^><^<v^<>^<>v^vv<v^v>^>v^^>^^>><>^>>>vv<^^^<<<>v^><<^v><>v><<vv^^><vv^<^><<>>>^^><v<v><<<vv^v><>v><<^<^<v<v^<^<vv<>>><><v^>vv<<v^<vv><v^<><>^v^><><<<v<^^^>v<<vv<<^>>>^^v><>>>vv>><vvv^vv^><<<^v^^^vv<<<^^^<>><v^<v>v>>^><>^^vv<^^vv<^^^vv^>v^>^^<v<v>>>vv^v<<<v^vvv><v<^><v^>^^<v<^>v<^<^v>v^<^v^<^<>>v>>>>v^v>^^<v><^v^v<v<v<>><v^v<>v<^>v<>^<vv>^^<<vvvv<^v^<<<>v^v<^v<><^>><^^^v<<^^<v^v^>>vv^<vvv>>>v>^^>>>^>>^v^>>><>>>>^v^vv<^>><^<v>v>^v><>^^><>v<<v<>>>^<<>><^
>v^^v<<>>^>^<v<<<^^vv<<><^^^v>^>^>v^<>^^<^v><<v>v^><v^>^>>>vv^vv<<<v^<v>^vv^v><^v<<^vv>>^><v>v><>v^v<<>v<<v^v>v><><v>^v<v<v>v^^v>^^>^><^<^v<^>v<vv><v<^^>v<>>^^^v<^vvv<>^<<><>^<^>^v>>^>v<^^>v><<>v<^^>>><^<^>vv<>^<v^<^^<>^^vv>^v><^<^v^^v^><<<^<v>vv<<^^v^^^<^^^^vv>^v>^v^<<v>v^<v>>v<^v>^v^<^><<vv>>v>^>^^<vv<>^^vvvv>^>vvv>><v>vv<v>^><v<^^>>^^vvv>v<<vvv<^^><>v<v<<<<><v^v<<<^^>v<v>>>^>vv^<><v^<v>v<<<>^^v<>^v^v>v>>^<<>>^v>^<v>^<^>^<><>^v^^>>v^<<v><v^>vvv^>><^^>>v^<>^^^>>>><^>^<<^>^<><^<^v>^>^<<v<v<>^^v^^>v><<<<v>>>v^<<^>v^v<><^<>^^vv^vv<^<^v<^^><<v<><^><^<>v^v<^^<^<<^^>><<>^>^>^><<^^v^<>^^^<^>^<>>><v><^^<^^>v^v>^^>^<^vv^>v^<v>^>v><>v^v<<v^v>>>^v<vv<v>>^^^<^^<v<<vv^>^>^<>>^>v^^v<v>^<<>>>^v^>^<^^<^v>^<vvv<^^v^>^<v<^vv<>><<<^v^v><^v^<v^<<>^>^>^<^^^>><><v<v<<vv>^^><>><^v><v^v<><<^^v>>^v<v>>v<>v>^>vvv>>v>^<^^v>vv^^<^>^<><>>>>v^^^v^<<>>v>v^>^<<v^>^><<^v<>>v>^^<<<>^>vv<^^v<>>^<><<<v^v<v>><>^<>>v<^v^<<<<>>>><v>^>vv<v>>^^>v^v><^v<v^><>^<<>v^<^<^<v<><>v<>^v>v>v>^v^^<<<><v^v><<>>v><>v<>^vv<v<vvv^^<<>^<^v"""

    answer = AocDay15(data,silver_tests,gold_tests,argv)

    print(answer)
