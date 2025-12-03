#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay

class AocDay11(AocDay):

    def count_flashes(self,grid):
        for cell in grid: grid[cell] += 1
        flashed = set()
        while flashing := {k for k,v in grid.items() if v>9 and k not in flashed}:
            flashed |= flashing
            for cell in flashing:
                for pos in self.adjacent8(*cell): grid[pos] += 1
        for cell in flashed: grid[cell] = 0
        return len(flashed)

    def run_silver(self,data):
        grid = self.densenumbermap()
        return sum(self.count_flashes(grid) for _ in range(100))
        
    def run_gold(self,data):
        grid = self.densenumbermap()
        return next(step for step,flashes in enumerate((self.count_flashes(grid) for _ in range(1000)),start=1) if flashes == 100)

if __name__ == "__main__":

    data = """1172728874
6751454281
2612343533
1884877511
7574346247
2117413745
7766736517
4331783444
4841215828
6857766273"""

    silver_tests = ["""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""",""""""]

    gold_tests = ["""""",""""""]

    answer = AocDay11(data,silver_tests,gold_tests,argv)

    print(answer)
