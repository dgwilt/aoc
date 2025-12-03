#!/usr/bin/env python3 
from itertools import product
from collections import deque
from sys import argv
from aoc import AocDay
import matplotlib.pyplot as plt
import numpy as np

class AocDay12(AocDay):

    VISUALIZE = False
    def visualize(self,map,xdim,ydim):
        _, ax = plt.subplots(subplot_kw={"projection": "3d"})
        X, Y = np.meshgrid(range(xdim), range(ydim))
        Z = np.array([[map[(x,y)] - ord('a') for x in range(xdim)] for y in range(ydim)])
        ax.plot_surface(X, Y, Z, cmap=plt.get_cmap('terrain'))
        # Saved for the show_path() method
        self.ax = ax
        self.plt = plt

    def show_path(self,path):
        X = [p[0] for p in path]
        Y = [p[1] for p in path]
        Z = [p[2] - ord('a') + 27 for p in path]
        self.ax.plot(X, Y, Z, linewidth=3)
        self.plt.show()

    def make_map(self,data):
        grid = data.splitlines()
        xdim = len(grid[0])
        ydim = len(grid)
        map = {(x,y):ord(grid[y][x]) for x,y in product(range(xdim),range(ydim))}
        lowest = tuple([k for k,v in map.items() if v == ord('S')][0])
        highest = tuple([k for k,v in map.items() if v == ord('E')][0])
        map[lowest] = ord('a')
        map[highest] = ord('z')
        self.grid = map # Saved for the adjacent4() method

        if AocDay12.VISUALIZE: self.visualize(map,xdim,ydim)
        return map, lowest, highest

    # General BFS with path
    def bfs(self,map,start,ends,rule):
        visited = set()
        queue = deque([(start,map[start],0,[(*start,map[start])])])
        while queue:
            pos,height,steps,path = queue.popleft()
            if pos in ends:
                if AocDay12.VISUALIZE: self.show_path(path)
                return steps

            if pos in visited:
                continue

            visited.add(pos)
            for next in [p for p in self.adjacent4(*pos) if rule(map,p,height)]:
                queue.append((next,map[next],steps+1,path+[(*next,map[next])]))

    def run_silver(self,data):
        map, lowest, highest = self.make_map(data)
        rule = lambda m,p,h: m[p] <= h + 1
        # Search from lowest to highest
        return self.bfs(map,lowest,set([highest]),rule)

    def run_gold(self,data):
        map, _, highest = self.make_map(data)
        all_lowest = set(k for k,v in map.items() if v == ord('a'))
        rule = lambda m,p,h: m[p] >= h - 1
        # Search from highest to any of the lowest
        return self.bfs(map,highest,all_lowest,rule)

if __name__ == "__main__":

    silver_tests = ["""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""",""""""]

    gold_tests = ["""""",""""""]

    data = """abcccccccccccccccccccccccccccccccaaaaaaaaaaaaaaaaccaaaaaaaaccccccccccccccccccccccccccccccccccccaaaaaa
abcccccccccccccccccccccccccccccccaaaaaaaaaaaaaaaaaccaaaaaaccccccccccccccccccccccccccccccccccccccaaaaa
abcccccccccccccccccccccccccccccccccaaaaaaaacccaaaaccaaaaaaccccccccccccccccccccaaaccccccccccccccccaaaa
abcccccccccccccccccccccccccccccccccccaaaaaaaccaaccccaaaaaaccccccccccccccccccccaaaccccccccccccccccaaaa
abcccccccccccccccccccccccccccccaaacccaaaaaaaacccccccaaccaaccccccccccccccccccccaaaccccccccccccccccaaac
abcccccccccccccccccccccccccccccaaaaaaaaacaaaacccccccccccccccaccaaccccccccccccciiaaccaaaccccccccccaacc
abccccccccaaccccccccccccccccccaaaaaaaaaaccaaacccccccccccccccaaaaaccccccccacaiiiiijjaaaacccccccccccccc
abacccaaccaacccccccccccccccccaaaaaaaaaaccccacccccaaaaccccccccaaaaacccccccaaiiiiijjjjaaaccccccaacccccc
abacccaaaaaacccccccccccccccccaaaaaaaaccccccccccccaaaacccccccaaaaaacccccccaiiiioojjjjjacccaaaaaacccccc
abcccccaaaaaaacccccccccccccccccaaaaaaccccaaccccccaaaacccccccaaaaccccccccciiinnoooojjjjcccaaaaaaaccccc
abccccccaaaaaccccccccccccccccccaaaaaacccaaaaccccccaaacccccccccaaaccccccchiinnnooooojjjjcccaaaaaaacccc
abcccccaaaaacccccccccccccccccccaacccccccaaaaccccccccccccccccccccccccccchhiinnnuuoooojjjjkcaaaaaaacccc
abccccaaacaaccccccccccccccccccccccccccccaaaaccccccccccccccccccaaacccchhhhhnnntuuuoooojjkkkkaaaacccccc
abccccccccaacccccccccccccccccccccccccccccccccccccccccccccccccccaacchhhhhhnnnnttuuuuoookkkkkkkaacccccc
abcccccccccccccccccccaacaaccccccccccccccccccccccccccccccccccaacaahhhhhhnnnnntttxuuuoopppppkkkkacccccc
abcccccccccccccccccccaaaaacccccccccaccccccccccccccccccccccccaaaaahhhhmnnnnntttxxxuuupppppppkkkccccccc
abccccccccccccccccccccaaaaacccccaaaacccccccccccccccccccccccccaaaghhhmmmmttttttxxxxuuuuuupppkkkccccccc
abcccccccccccccccccccaaaaaaaccccaaaaaaccccccccccccccccccccccccaagggmmmmtttttttxxxxuuuuuuvppkkkccccccc
abcccccccccccccccccccaaaaaaaaaaacaaaaacccccccccccccccccccccccaaagggmmmttttxxxxxxxyyyyyvvvppkkkccccccc
abccccccccccccccccccccaaaaaaaaaaaaaaaccccccccccccccccccccaacaaaagggmmmtttxxxxxxxyyyyyyvvppplllccccccc
SbcccccccccccccccccccaaaaaaaaaacaccaaccccccccccccccccccccaaaaaccgggmmmsssxxxxEzzzyyyyvvvpplllcccccccc
abcccccccccccccccccccccaaaaaaccccccccccccccaacaaccccccccaaaaaccccgggmmmsssxxxxyyyyyvvvvqqplllcccccccc
abccccccccccccccccccccccaaaaaacccccccccccccaaaacccccccccaaaaaacccgggmmmmsssswwyyyyyvvvqqqlllccccccccc
abcccccccccccccccccccccaaaaaaaccccccccccccaaaaacccccccccccaaaaccccgggmmmmsswwyyyyyyyvvqqllllccccccccc
abcccccccccccccccccccccaaaccaaacccccccccccaaaaaaccccccccccaccccccccgggooosswwwywwyyyvvqqlllcccccccccc
abccccccccccccccccccccccacccccccccccccccccacaaaacccccccccccccccccccfffooosswwwwwwwwvvvqqqllcccccccccc
abccccccccccccccccccccccccccccccccccccccccccaacccccccccccccccccccccfffooosswwwwwrwwvvvqqqllcccccccccc
abccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccffooossswwwrrrwvvvqqqmmcccccccccc
abccccaaacccccccccccccccccccccccccccccccccccccccccccccccccccccccccccffooosssrrrrrrrrqqqqmmmcccccccccc
abccccaaacaacccccaaccccaaaacccccccccccccccccccccccccccccccccccccccccffooossrrrrrnrrrqqqqmmmcccaaacccc
abcccccaaaaaccaaaaacccaaaaacccccccccccccccccccccccccccccccccccccccccfffoooorrnnnnnnmqqmmmmmcccaaacccc
abccaaaaaaaacccaaaaaccaaaaaaccccccccccccccccccccccccccccccccccccccccfffooonnnnnnnnnmmmmmmmcccaaaccccc
abcccaaaaacccccaaaaaccaaaaaaccccccaacccccccccccccccccccccccccccccccccfffoonnnnneddnmmmmmmccccaaaccccc
abccccaaaaacccaaaaacccaaaaaacccccaaaaaaccccccccccccccccccccaaccccccccffeeeeeeeeeddddddddccccaaaaccccc
abccccaacaaacccccaacccccaacccccccaaaaaaaccccccccccccccccaaaaaccccccccceeeeeeeeeedddddddddccaccaaccccc
abccccaacccccccccccccccccccccccccaaaaaaaccaaaccccccccccccaaaaaccccccccceeeeeeeeaaaaddddddcccccccccccc
abcccccccccccaaccccccccccccccccccccccaaaaaaaaacccccccccccaaaaacccccccccccccaaaacaaaacccccccccccccccaa
abccccccccaacaaacccccccccccccccccccccaaaaaaaacccccccccccaaaaaccccccccccccccaaaccaaaaccccccccccccccaaa
abccccccccaaaaacccccccccccccccccccccacaaaaaaccccccccccccccaaacccccccccccccccaccccaaacccccccccccacaaaa
abcccccccccaaaaaaccccccccccccccccaaaaaaaaaaacccccccccccccccccccccccccccccccccccccccacccccccccccaaaaaa
abcccccccaaaaaaaaccccccccccccccccaaaaaaaaaaaaacccccccccccccccccccccccccccccccccccccccccccccccccaaaaaa"""

    answer = AocDay12(data,silver_tests,gold_tests,argv)

    print(answer)
