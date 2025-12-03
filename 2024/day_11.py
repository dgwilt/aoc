#!/usr/bin/env python3 
from collections import defaultdict
from sys import argv
from aoc import AocDay

class AocDay11(AocDay):

    def run_silver_orig(self,data):
        BLINKS = 25
        stones = [int(i) for i in data.split()]
        for _ in range(BLINKS):
            max,i = len(stones),0
            while i < max:
                if stones[i] == 0:
                    stones[i] = 1
                elif (l := len(s := str(stones[i]))) % 2 == 0:
                    stones[i] = int(s[:(half := l//2)])
                    stones.append(int(s[half:]))
                else:
                    stones[i] *= 2024
                i += 1
        return len(stones)

    def run_blinks(self,data,blinks):
        stones = {int(i):1 for i in data.split()}
        for _ in range(blinks):
            nxt = defaultdict(int)
            nxt[1] = stones.pop(0,0)
            for stone,count in stones.items():
                if (l := len(string := str(stone))) % 2 == 0: # Slightly over-walrused
                    nxt[int(string[:(half := l//2)])] += count
                    nxt[int(string[half:])] += count
                else:
                    nxt[stone * 2024] += count
            stones = nxt
        return sum(stones.values())

    def run_silver(self,data):
        orig = self.run_silver_orig(data)
        new = self.run_blinks(data,25)
        assert(orig == new)
        return new

    def run_gold(self,data):
        return self.run_blinks(data,75)

if __name__ == "__main__":

    silver_tests = ["""0""",""""""]

    gold_tests = ["""""",""""""]

    data = """64599 31 674832 2659361 1 0 8867 321"""

    answer = AocDay11(data,silver_tests,gold_tests,argv)

    print(answer)
