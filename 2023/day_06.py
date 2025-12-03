#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay, prod

class AocDay6(AocDay):

    def rootdiff(a,b,c):
        const = -b/(2*a)
        plusminus = (b**2 - (4*a*c))**0.5 / (2*a)
        #          floor                negative, so int is closer to 0
        return int(const - plusminus) - int(const + plusminus)
    
    def run_silver(self,data):
        lines = data.splitlines()
        times = [int(i) for i in lines[0].split()[1:]]
        distances = [int(i) for i in lines[1].split()[1:]]
        ways = []
        for time,distance in zip(times,distances):
            #ways.append(sum(button * (time-button) > distance for button in range(1,time)))
            ways.append(AocDay6.rootdiff(-1,time,-distance)) # Solving the quadratic -button**2 + time*button - distance > 0
        return prod(ways)
        
    def run_gold(self,data):
        lines = data.splitlines()
        time = int("".join([i for i in lines[0].split()[1:]]))
        distance = int("".join([i for i in lines[1].split()[1:]]))
        #return sum(button * (time-button) > distance for button in range(1,time))
        return AocDay6.rootdiff(-1,time,-distance) # Solving the quadratic -button**2 + time*button - distance > 0

if __name__ == "__main__":

    silver_tests = ["""Time:      7  15   30
Distance:  9  40  200""",""""""]

    gold_tests = ["""""",""""""]

    data = """Time:        61     70     90     66
Distance:   643   1184   1362   1041"""

    answer = AocDay6(data,silver_tests,gold_tests,argv)

    print(answer)
