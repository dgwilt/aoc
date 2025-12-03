#!/usr/bin/env python3 
from itertools import product
from collections import defaultdict
from sys import argv
from aoc import AocDay
import networkx as nx
from math import lcm
import turtle

class AocDay24(AocDay):

    VISUALIZE = True

    def build_world(self,data):
        world = {}
        for y,line in enumerate(data.splitlines()[1:-1]):
            for x,cell in enumerate(line[1:-1]):
                pos = (x,y)
                match cell:
                    case "<": world[pos] = [(-1,0)]
                    case ">": world[pos] = [(1,0)]
                    case "^": world[pos] = [(0,-1)]
                    case "v": world[pos] = [(0,1)]
        return world, x+1, y+1

    def time_step(self,world,xdim,ydim,allpos):
        nextworld = defaultdict(list)
        for pos,dirs in world.items():
            for dir in dirs:
                nextpos = ((pos[0]+dir[0]) % xdim,(pos[1]+dir[1]) % ydim)
                nextworld[nextpos].append(dir)
        thisgaps = allpos - set(world.keys())
        nextgaps = allpos - set(nextworld.keys())
        return nextworld,thisgaps,nextgaps

    def run_silver(self,data):
        world,xdim,ydim = self.build_world(data)
        goal = (xdim-1,ydim)
        start = (0,-1)

        allpos = set(product(range(xdim),range(ydim))) | {start,goal}
        move_or_stay = lambda x,y: ((x-1,y),(x+1,y),(x,y-1),(x,y+1),(x,y))

        G = nx.DiGraph()
        loop = lcm(xdim,ydim)

        for t in range(loop + 1): # To loop back to time=0 state
            nextworld,thisgaps,nextgaps = self.time_step(world,xdim,ydim,allpos)
            for pos in thisgaps:
                for nextpos in [p for p in move_or_stay(*pos) if p in nextgaps]:
                    # Goal is at time -1 to remain fixed
                    G.add_edge((pos,t), (nextpos, -1 if nextpos == goal else (t+1)%loop))
            world = nextworld
                        
        path = nx.shortest_path(G,(start,0),(goal,-1))

        if AocDay24.VISUALIZE:
            SF = 4
            pen = turtle.Turtle()
            turtle.setworldcoordinates(-100,-100,500,500)
            pen.hideturtle()
            pen.pu()
            (x,y),_ = path[0]
            pen.setposition(SF*x,SF*y)
            pen.pd()
            for ((x,y),_) in path[1:]:
                pen.setposition(SF*x,SF*y)
            turtle.done()

        return len(path) - 1

    def run_gold(self,data):
        world,xdim,ydim = self.build_world(data)
        goal = (xdim-1,ydim)
        start = (0,-1)

        xmax, ymax = xdim-1,ydim-1

        allpos = set(product(range(xdim),range(ydim)))
        adjacent4 = lambda x,y: ((x-1,y),(x+1,y),(x,y-1),(x,y+1))
        firstgaps = allpos - set(world.keys())

        G = nx.DiGraph()
        #for t in range(lcm((xmax+1),(ymax+1))):
        for t in range(xdim * ydim):
            nextworld,thisgaps,nextgaps = self.time_step(world,xdim,ydim,allpos)

            for pos in thisgaps:
                if pos in nextgaps:
                    for trip in range(3):
                        G.add_edge((pos,t,trip),(pos,t+1,trip))
                for nextpos in adjacent4(*pos):
                    if nextpos in nextgaps:
                        for trip in range(3):
                            G.add_edge((pos,t,trip),(nextpos,t+1,trip))

            G.add_edge((start,t,0),(start,t+1,0)) # Can always wait before setting off
            G.add_edge((start,t,2),(start,t+1,2)) # Can wait when turning around to go back to the end
            G.add_edge((goal,t,1),(goal,t+1,1)) # Can wait before setting off back to the start

            if (0,0) in thisgaps:
                G.add_edge(((0,0),t,1),(start,t+1,2)) # Finish the return joutney to the start

            if (xmax,ymax) in thisgaps:
                G.add_edge(((xmax,ymax),t,0),(goal,t+1,1))
                G.add_edge(((xmax,ymax),t,2),(goal,-1,-1))

            if (0,0) in nextgaps:
                G.add_edge((start,t,0),((0,0),t+1,0))
                G.add_edge((start,t,2),((0,0),t+1,2))

            if (xmax,ymax) in nextgaps:
                G.add_edge((goal,t,1),((xmax,ymax),t+1,1))

            world = nextworld
        
        thisgaps = allpos - set(world.keys())
        nextgaps = firstgaps
        for pos in thisgaps:
            if pos in nextgaps:
                for trip in range(3):
                    G.add_edge((pos,t,trip),(pos,0,trip))
            for nextpos in adjacent4(*pos):
                if nextpos in nextgaps:
                    for trip in range(3):
                        G.add_edge((pos,t,trip),(nextpos,0,trip))

        path = nx.shortest_path(G,(start,0,0),(goal,-1,-1))

        if AocDay24.VISUALIZE:
            SF = 4
            pen = turtle.Turtle()
            turtle.setworldcoordinates(-100,-100,500,500)
            pen.hideturtle()
            pen.pu()
            (x,y),_,_ = path[0]
            pen.setposition(SF*x,SF*y)
            pen.pd()
            for ((x,y),_,_) in path[1:]:
                pen.setposition(SF*x,SF*y)
            turtle.done()

        return len(path) - 1

if __name__ == "__main__":

    silver_tests = ["""#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""",""""""]

    gold_tests = ["""""",""""""]

    data = """#.####################################################################################################
#>>^<^v>v<>^>>v<<.<<<^<vv^<^>v><^<v>><^>.<><^^>v<^>v>^^>v><v.^<.^>>>^>v^^^<vv^<><vvv>v>^vv<<>v^^<v><>#
#>^>^><^v<>.v><><<<>><v><>vv^.><v^<^v^>v<<<v..<v.v^v.v<<v<>>^^<v^v.<^.^v><^v^.^^<v>..v<^>^<<^>.v.>v.>#
#.>^>v<v^><v<v^><>^v>><>v<>^><>v^<^v<>v<>^<v<><^^v.v.>^^.v<<^v<>>.v>>v<^^.v<v^<^>>..>><<v.^>.<<<^v.^>#
#<>^^^..v^^v^<<><<<^<>.>.vvv.v>^^.><.^>>>v^^>^^vv>v<^v>>^^<v>v^<<^>..^v^<>>>>>.>>><v^^^vv<>v^v<>^^.<>#
#>v^vvv><>>v^v.v><v<<^.>.>>^<.^<^<>><^<><^>v.>v<>v><<>>><^v<.>v<^v<v^..<vv><><.^^^^<^.<v<<^^>>v^>^<><#
#>^>^>^<<>^><<v^^^^^^^v^<<>>v^^>v>v<.><><^v^<v>>>>^<..>v<.^v><^<^v>v^^vvv^v^<v>>.^<<<.^^vv>vvv>^..<v>#
#><vv.vv^v.>^>>v<<<v^>>^^>><v<<.^>>v>v^.<v<vv<<<.vv^<>^.<v>vv<.>^^v><><^<v<^><.^vv^^<><<.vv^<v<<v.v^>#
#<^<v>.>^v^<v^^><vv.>>.<^>.^..><v^<<v^<^<<.<v<^v^v<^<.<<v<^v>^<<^v<>^<^v>vv^>vv>^<v.>^><v..>><v^<^^^>#
#>^><v><<<>><^v^>v<><>v^><.v>>.>^v<.^><vvv<.>v<v>^>>v><^^^v^.v>^.^^>^v>>v^v<^v>.^.<^>^^v<.<<v^..<<.v>#
#>vv>^.<<>><^>.<^><v<^<>>v><v>^.>v^<><.v.>^>>^><<v>^v..<^^^<vv^..^^<<<.v<<v<vv^v^<^><><v>.<<><^<v<^<<#
#>^>v<^v^.<<v<<^^>^<>vvv<v^>^<v<.^v^>><>vv<>v<.^^>^<>>><>v<<>.>^<<>vvv^v.v<><<>^.v.>^><^^>>^>>><>v.^<#
#>^<.^.<>v<.<^v>v<^^<>^>vvv..v.^><<^<.><...<.^>^>^vv<>v^^><<v>v^^<^^><<^>>vvv^<^^v>>vv<v<><v^<^v<^v^>#
#.>>^.v<>v>><<..vv>^.>>^>^^.v>v.<^><>v<v^^><<v<.>>^<v<<><>.^<<.>>^<v<>v^>><v>^>..v<^<^.vv<>^^>>>v^>v<#
#<>^^^<v><^v^vvv>^v^v><<>>^<vv^><<v.>>v>.v>^>>v<^vv.<><<>><<v<>>^.<<>v.v^^vv<.>^<^v.<^<vvv^v.vv><vv.>#
#>vv.vv^><v>v>.<v^><v<vv^v<.v<<>^<^>^><v^>v>^<v><>v>>v>>>>v^.<v<vv>^v<^.^.^>>><>^<^<^.<v<.><v.^<^.><.#
#>^vvv<>^v^^>^<^v<^>v<<^<vv.vvv<<<v<v^..^.<<v<<<>>^>v^v^>^><v.^<v<<v>^^v<v.>>>v^<v^<v>^<^^.>v<^<>^.v<#
#<>^<<<<v<>^v>v^<vv<^v>v^^<>.^>^^<.>>v>v<<^<<<>v<v^v><>>.<<.^<>><<<v>v^>v^^<v^^.><vv>^^<v.v>^<v<.vv><#
#<>vvv<^^.v^^.v.<^<^>.^^v>^v>>.vv.>.v<<^<^^>vvv^<<<vv^<vv<>>v^^<^.<^.>v.^>v><^^>>^>^<>.>.^<<<.v.<>^>>#
#><>v<>>>><.^v>v><v>^<<><>^vv.^.<.>>vvvv><>^^><>v>v.^^<^<^v>v<^<.<^<>^^^^vvv>.>>><^vv<^^^>.^<<v^>>><>#
#<<><^>>^>^^>><.v^^^.v^^^>.^v<vvv.^^<^^>^<>>><<>>><<.v<^>><<v<v^>vv^<>vv.<<>v<v^><<vv^^^>vvvv<<v<><<<#
#<^<><>><<>^^>v<<^v<v>^^^>^^vvvv<^^vv<>><.<^^.vv^>>.<>^.v<><^^vv>^^>>^<^^v>.v<>>^v.v^>.^v<.<v.<>>>>v<#
#<^<<^^^vv><^<>^^>^v<v^v^.<v.>v>><<^^>v^>v>><v<<><>^^.vv^><.^>vv^v<<>^><^>^>^v^<><>^.^<.^.^>>^<.>^><<#
#>^.<<v>^.<<<^>v>>>^<.^>>>.^^<<^.v^<<>v^<<<^<><>^vvvv^>vv^^>.>>^>><>^^^^>v<^^>^^<^vv.v.^<<^<<^>v><.>>#
#>vv^.^vv>^<>^v.^^<v>v>><^^^v<<>>^>>^^>^<^<<<^.v><^>v<<v^<^^^>vv><<v<.<v><^vv>^>^v^<^v>^<^vv<<^v<.^^>#
#<v>vv<^>v^^<<^^<<<v>v><<<.v^>^<><vvv^>.^.v>v<^^vvvv>>^v^^v^^^<>>>>v>>^>v^.<>.>.^vvv^<^<.<^>^<.v<><.>#
#.<.<^v<v><^>.^.v<>>^<>.<<^.vv^>v^v<..>^.^^vv^><.<>^<><^vv>^<.<>v..<^^<v^^v<<<v<><<>>vv<>^^<>^vvvvv><#
#<.^v^>vvv<.v<.vv><^vv^>>.^>><><<v>v<^<<vv.<>v<vv^v>^>^^<v>^>^<<>^<<^>.v^^^><>.^^v>^...^<^>>>.>v^^vv<#
#.<^v>^>^^<^v.v>.^<><<<>>vv>.^v<>.<<>>v^v<v>>^.^<^^<.v^<><vvv>><^.>.vv<.vv^>^><<.<.>><^>vv^^>>v^>^>.<#
#.>^<>><v<.>vv<>>^<v.>^.<v^v.v<><>^<v^<v.<<^v<>v<<v>v^>^>v.>>v^.><^^.>v<v.v^.>^^<>^<.^<v^^><<>^vvv>><#
#.^.^vv^..^>.v.<<v>^^^>^<^v<^>>v<>v>.<><>>.<v^<^>.<v.^^v^<v><>^>v.<^<<><>v.<<<^>.<<.^>^>^<^.>^v>>>.>>#
#.^v>><>v<<.<^>^^<<>^>v>vv<>>^>>^.v^>.>^<v^v>>v^^><.v.<v>.>vv<<^v<v<v^v>v<v<.^<.^<<v>^^v.^v.<^>.v>^>>#
#>^v>^<<>>vv>^<.<v^v<^>>^v>^v^<<><<^^^^v>^^^^^^^vv<^..<vvv><^.<..^>^^<^>v^>>>>vv>v<<<<>.>.>^.^<^.v<v>#
#.^v.^>><.><<v^>^^.>><^v<..>..><.><><<v>>>v<>^.>v<vv^^<<.^.^^v<v..^<v^>.<vvv>^>v>^<^><>>>>v<>^>>vv^.>#
#<v<vv^vvv><v^<^>>.v^v^>><.>><>>v^^<v>>>>.v^.^.<vv.>>>^v>^<>v^.^>v<vv.>>vvv^v^<vv<>v<^<^.<<^..v^.^v<<#
#<.<v>^>v<^<.<><>.v<<^v<^<>^.vv<v<<v>v<^<^v>v<v^^vv<><..v<<<<.^^v<>>^<v>.^>>v<^>v>^><vvv<^>>.^v>^<.><#
####################################################################################################.#"""

    answer = AocDay24(data,silver_tests,gold_tests,argv)

    print(answer)
