#!/usr/bin/env python3 
from itertools import product
from sys import argv
from aoc import AocDay
from functools import lru_cache

class AocDay21(AocDay):

    def run_silver(self,data):
        WINSCORE = 1000
        pos = [int(i)-1 for i in data.split(",")]
        scores = [0,0]
        die = 0
        while all(s<WINSCORE for s in scores):
            for i in range(2):
                total = 3*die + 6
                die += 3
                pos[i] = (pos[i] + total) % 10
                scores[i] += pos[i] + 1
                if scores[i] >= WINSCORE: break
        return min(scores) * die

    QUANTUMDIE = list(sum(die) for die in product(range(1,4),range(1,4),range(1,4)))

    @lru_cache(maxsize=None)
    def count_wins(a, b):
        awins, bwins = 0,0
        for total in AocDay21.QUANTUMDIE:
            pos_a = (a[0] + total) % 10
            score_a = a[1] + pos_a + 1
            if score_a >= 21:
                awins += 1
            else:
                roll_bwins, roll_awins = AocDay21.count_wins(b, (pos_a,score_a))
                awins += roll_awins
                bwins += roll_bwins
        return awins, bwins
        
    def run_gold(self,data):
        p1,p2 = [int(i)-1 for i in data.split(",")]
        return max(AocDay21.count_wins((p1, 0), (p2, 0)))

if __name__ == "__main__":

    silver_tests = ["4,8"]

    gold_tests = ["""""",""""""]

    data = "1,2"

    answer = AocDay21(data,silver_tests,gold_tests,argv)

    print(answer)
