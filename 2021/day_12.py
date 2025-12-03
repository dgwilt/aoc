#!/usr/bin/env python3 
from collections import defaultdict
from sys import argv
from aoc import AocDay

class AocDay12(AocDay):

    START, END = 'start', 'end'

    @staticmethod
    def build_graph(data):
        # Build graph
        G = defaultdict(set)
        for a,b in [line.split("-") for line in data.splitlines()]:
            # Undirected graph, so add edges in both directions
            for fr,to in ((a,b),(b,a)): 
                # Don't add any paths that go to the start or from the end
                if to != AocDay12.START and fr != AocDay12.END: G[fr].add(to)
        return G

    @staticmethod
    def count_paths(G,start,end,can_revisit_lower=False):
        # Do a DFS (Any exhaustive search is OK)
        stack = [(start,set(),can_revisit_lower)]
        paths = 0
        while stack:
            # For 'all paths' need to keep a track of what has been visited on each path rather than a global visited set
            cave,visited,can_revisit_lower = stack.pop()
            if cave.islower() and cave in visited:
                if can_revisit_lower:
                    # Use up our one chance to revisit a lower-case cave
                    can_revisit_lower = False
                else: continue
            paths += (cave == end)
            stack.extend([(next,visited.union({cave}),can_revisit_lower) for next in G[cave]])
        return paths

    def run_silver(self,data):
        G = AocDay12.build_graph(data)
        return AocDay12.count_paths(G,AocDay12.START,AocDay12.END)
        
    def run_gold(self,data):
        G = AocDay12.build_graph(data)
        return AocDay12.count_paths(G,AocDay12.START,AocDay12.END,can_revisit_lower=True)

if __name__ == "__main__":

    data = """LP-cb
PK-yk
bf-end
PK-my
end-cb
BN-yk
cd-yk
cb-lj
yk-bf
bf-lj
BN-bf
PK-cb
end-BN
my-start
LP-yk
PK-bf
my-BN
start-PK
yk-EP
lj-BN
lj-start
my-lj
bf-LP"""

    silver_tests = ["""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""","""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""","""start-A
start-b
A-c
A-b
b-d
A-end
b-end"""]

    gold_tests = ["""""",""""""]

    answer = AocDay12(data,silver_tests,gold_tests,argv)

    print(answer)
