#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay

class AocDay6(AocDay):

    @staticmethod
    def fish_sim(data,days):
        fish = [data.count(str(n)) for n in range(9)] # Could have used a deque if going for more days
        for _ in range(days):
            spawning = fish.pop(0)
            fish.append(spawning)
            fish[6] += spawning
        return sum(fish)

    def run_silver(self,data):
        return AocDay6.fish_sim(data,80)

    def run_gold(self,data):
        return AocDay6.fish_sim(data,256)

if __name__ == "__main__":

    data = """3,5,3,5,1,3,1,1,5,5,1,1,1,2,2,2,3,1,1,5,1,1,5,5,3,2,2,5,4,4,1,5,1,4,4,5,2,4,1,1,5,3,1,1,4,1,1,1,1,4,1,1,1,1,2,1,1,4,1,1,1,2,3,5,5,1,1,3,1,4,1,3,4,5,1,4,5,1,1,4,1,3,1,5,1,2,1,1,2,1,4,1,1,1,4,4,3,1,1,1,1,1,4,1,4,5,2,1,4,5,4,1,1,1,2,2,1,4,4,1,1,4,1,1,1,2,3,4,2,4,1,1,5,4,2,1,5,1,1,5,1,2,1,1,1,5,5,2,1,4,3,1,2,2,4,1,2,1,1,5,1,3,2,4,3,1,4,3,1,2,1,1,1,1,1,4,3,3,1,3,1,1,5,1,1,1,1,3,3,1,3,5,1,5,5,2,1,2,1,4,2,3,4,1,4,2,4,2,5,3,4,3,5,1,2,1,1,4,1,3,5,1,4,1,2,4,3,1,5,1,1,2,2,4,2,3,1,1,1,5,2,1,4,1,1,1,4,1,3,3,2,4,1,4,2,5,1,5,2,1,4,1,3,1,2,5,5,4,1,2,3,3,2,2,1,3,3,1,4,4,1,1,4,1,1,5,1,2,4,2,1,4,1,1,4,3,5,1,2,1"""

    silver_tests = ["""3,4,3,1,2""",""""""]

    gold_tests = ["""""",""""""]

    answer = AocDay6(data,silver_tests,gold_tests,argv)

    print(answer)
