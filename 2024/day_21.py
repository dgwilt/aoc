#!/usr/bin/env python3 
from itertools import product
from collections import defaultdict
from sys import argv
from aoc import AocDay
import networkx as nx
from heapq import heappush,heappop
from math import inf

deltas = {"^":(0,-1),"v":(0,1),"<":(-1,0),">":(1,0)}

class Panel:

    keypad = {
        (0,0):"7",
        (1,0):"8",
        (2,0):"9",
        (0,1):"4",
        (1,1):"5",
        (2,1):"6",
        (0,2):"1",
        (1,2):"2",
        (2,2):"3",
        (1,3):"0",
        (2,3):"A",
    }
    revkeypad = {v:k for k,v in keypad.items()}
    
    def __init__(self):
        self.key = None
        self.pos = None

    def set(self,key):
        self.key = key
        self.pos = Panel.revkeypad[key]

    def move(self,dir):
        if dir != "A": 
            dx,dy = deltas[dir]
            self.pos = (self.pos[0]+dx,self.pos[1]+dy)
            self.key = Panel.keypad[self.pos] # Allow this to raise an exception
        return None

class Control:
    keypad = {
        (1,0):"^",
        (2,0):"A",
        (0,1):"<",
        (1,1):"v",
        (2,1):">"
    }
    revkeypad = {v:k for k,v in keypad.items()}

    def __init__(self):
        self.key = None
        self.pos = None

    def set(self,key):
        self.key = key
        self.pos = Control.revkeypad[key]

    def move(self,dir):
        if dir == "A":
            return(self.key)
        else:
            dx,dy = deltas[dir]
            self.pos = (self.pos[0]+dx,self.pos[1]+dy)
            self.key = Control.keypad[self.pos] # Allow this to raise an exception
            return None

class AocDay21(AocDay):

    # Used a Reddit cheat credit for part 2. This was the best I found.
    # https://github.com/oshlern/adventofcode/blob/main/advent24/2024/python/18/concise.py
    def fewest_my_presses(N_ROBOT_KEYBOARDS,code):
        keypad = {key: (x, y) for y, row in enumerate([" ^A", "<v>"]) for x, key in enumerate(row)}
        # Fewest of MY presses to hit kf when starting at ki (at layer 0)
        leg_lengths = {(0, key_fr, key_to): 1 for key_fr,key_to in product(keypad,repeat=2)}
        # Fewest of MY presses to hit all ks when starting at A (at layer l)
        fewest_for_layer = lambda l, keys: sum(leg_lengths[(l, key_fr, key_to)] for key_fr, key_to in zip('A' + keys, keys)) # DJG this is the key line
        for layer in range(1, N_ROBOT_KEYBOARDS+1):
            if layer == N_ROBOT_KEYBOARDS:
                keypad = {key: (x, y) for y, row in enumerate(["789", "456", "123", " 0A"]) for x, key in enumerate(row)}
            gap = keypad[' ']
            for (key_fr, (xfr, yfr)),(key_to, (xto, yto)) in product(keypad.items(),repeat=2):
                hor_keys = ('>' if xto > xfr else '<') * abs(xto - xfr)
                ver_keys = ('^' if yto < yfr else 'v') * abs(yto - yfr)
                fewest_hor_first = inf if (xto, yfr) == gap else fewest_for_layer(layer-1, hor_keys + ver_keys + 'A')
                fewest_ver_first = inf if (xfr, yto) == gap else fewest_for_layer(layer-1, ver_keys + hor_keys + 'A')
                leg_lengths[(layer, key_fr, key_to)] = min(fewest_hor_first, fewest_ver_first)
        return fewest_for_layer(N_ROBOT_KEYBOARDS, code)

    def routes(keypad):
        deltas = {(0,-1):"^",(0,1):"v",(-1,0):"<",(1,0):">"}
        paths = defaultdict(dict)
        for frpos,topos in product(keypad,repeat=2):
            frkey = keypad[frpos]
            tokey = keypad[topos]
            todo = []
            heappush(todo,(0,frpos,""))
            while todo:
                cost,pos,path = heappop(todo)
                if pos == topos:
                    paths[frkey][tokey] = path
                    break
                for (dx,dy),key in deltas.items():
                    if (nxt := (pos[0]+dx,pos[1]+dy)) in keypad:
                        if not path: nxtcost = cost
                        else: nxtcost = cost + (key != path[-1])
                        heappush(todo,(nxtcost,nxt,path+key))
        return paths

    def build_graph(n):
        keypad = "0123456789A"
        ctlpad = "<>v^A"
        G = nx.DiGraph()

        machines = [Control() for _ in range(n)] + [Panel()]

        for cs in product(ctlpad,repeat=n):
            cs = "".join(cs)
            for p in keypad:
                cur = cs + p
                for press in ctlpad:
                    for m,k in zip(machines,cs+p):
                        m.set(k)
                    try:
                        action = press
                        for m in machines:
                            if action:
                                action = m.move(action)
                        nxt = "".join(m.key for m in machines)
                        G.add_edge(cur,nxt,label=press)
                    except KeyError:
                        pass
        return G

    def run_presses(self,data,n):
        result = 0
        G = AocDay21.build_graph(n)
        for code in data.splitlines():
            source = 'A' * (n+1)
            presses = ""
            for c in code:
                target = 'A' * n + c
                path = nx.shortest_path(G, source=source, target=target)
                source = target

                for i in range(len(path) - 1):
                    presses += G[path[i]][path[i + 1]]['label']

                presses += "A"
            
            result += len(presses) * int(code[:-1])
        return result

    def run_silver(self,data):
        return self.run_presses(data,2)

    def run_gold(self,data):
        return sum(AocDay21.fewest_my_presses(26,code) * int(code[:-1]) for code in data.splitlines())

    # Too slow!
    def run_gold_too_slow(self,data):
        return self.run_presses(data,25)

    # Works for test data but not real data.
    def run_gold_broken(self,data):
        keypad = {
            (0,0):"7",
            (1,0):"8",
            (2,0):"9",
            (0,1):"4",
            (1,1):"5",
            (2,1):"6",
            (0,2):"1",
            (1,2):"2",
            (2,2):"3",
            (1,3):"0",
            (2,3):"A",
        }
        ctlpad = {
            (1,0):"^",
            (2,0):"A",
            (0,1):"<",
            (1,1):"v",
            (2,1):">"
        }
        keypaths = AocDay21.routes(keypad)
        ctlpaths = AocDay21.routes(ctlpad)

        result = 0
        for code in data.splitlines():
            presses = ""
            fr = 'A'
            for to in code:
                presses += keypaths[fr][to] + 'A'
                fr = to
            for _ in range(2):
                nxtpresses = ""
                fr = 'A'
                for to in presses:
                    nxtpresses += ctlpaths[fr][to] + 'A'
                    fr = to
                presses = nxtpresses
            print(code,len(presses), presses)
            result += int(code[:-1]) * len(presses)
        return result
 
if __name__ == "__main__":

    silver_tests = ["""029A
980A
179A
456A
379A""",""""""]

    gold_tests = ["""""",""""""]

    data = """839A
169A
579A
670A
638A"""

    answer = AocDay21(data,silver_tests,gold_tests,argv)

    print(answer)
