#!/usr/bin/env python3 
from itertools import combinations, product
from collections import deque
from sys import argv
from aoc import AocDay, prod
from re import search

class AocDay19(AocDay):

    def run_silver(self,data):
        result = 0
        for line in data.splitlines():
            qualities = []
            bp,ore_ore_cost,clay_ore_cost,obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost,geode_obsidian_cost = [int(i) for i in search(r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.',line).groups()]
            # Time of availability
            queue = deque([(1,0, 0, 0, 0,[1],[],[],[])])
            while queue:
                t,ore,clay,obsidian,geodes,ore_robots,clay_robots,obsidian_robots,geode_robots = queue.popleft()

                print(t,ore,clay,obsidian,geodes,ore_robots,clay_robots,obsidian_robots,geode_robots)
                
                next_geode_robots = geode_robots[:]
                next_obsidian_robots = obsidian_robots[:]

                # Making
                if obsidian >= geode_obsidian_cost and ore >= geode_ore_cost:
                    next_geode_robots.append(t+1)
                    obsidian -= geode_obsidian_cost
                    ore -= geode_ore_cost

                if clay >= obsidian_clay_cost and ore >= obsidian_ore_cost:
                    next_obsidian_robots.append(t+1)
                    clay -= obsidian_clay_cost
                    ore -= obsidian_ore_cost

                visited = set()
                for make_clay, make_ore in product((True,False),(True, False)):
                    next_clay_robots = clay_robots[:]
                    next_ore_robots = ore_robots[:]
                    next_ore = ore
                    next_clay = clay
                    next_obsidian = obsidian
                    next_geodes = geodes

                    if make_clay and next_ore >= clay_ore_cost:
                        next_clay_robots.append(t+1)
                        next_ore -= clay_ore_cost

                    if make_ore and next_ore >= ore_ore_cost:
                        next_ore_robots.append(t+1)
                        next_ore -= ore_ore_cost

                    # Collecting
                    for r in next_ore_robots:
                        if t >= r: next_ore += 1
                    for r in next_clay_robots:
                        if t >= r: next_clay += 1
                    for r in next_obsidian_robots:
                        if t >= r: next_obsidian += 1
                    for r in next_geode_robots:
                        if t >= r: next_geodes += 1
                    
                    if t == 24:
                        qualities.append(bp*next_geodes)
                        continue

                    # next = (t+1,next_ore,next_clay,next_obsidian,next_geodes,len(next_ore_robots),len(next_clay_robots),len(next_obsidian_robots),len(next_geode_robots))
                    # if next not in visited:
                    #     visited.add(next)
                    queue.append(
                        [t+1,next_ore,next_clay,next_obsidian,next_geodes,
                        next_ore_robots,next_clay_robots,next_obsidian_robots,next_geode_robots]
                    )
            result += max(qualities)

        return result
        
    def run_gold(self,data):
        pass

if __name__ == "__main__":

    silver_tests = ["""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""",""""""]

    gold_tests = ["""""",""""""]

    data = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 19 clay. Each geode robot costs 4 ore and 15 obsidian.
Blueprint 2: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 20 clay. Each geode robot costs 2 ore and 9 obsidian.
Blueprint 3: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 4 ore and 19 clay. Each geode robot costs 4 ore and 12 obsidian.
Blueprint 4: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 17 clay. Each geode robot costs 2 ore and 13 obsidian.
Blueprint 5: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 16 clay. Each geode robot costs 3 ore and 13 obsidian.
Blueprint 6: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 16 clay. Each geode robot costs 2 ore and 15 obsidian.
Blueprint 7: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 6 clay. Each geode robot costs 3 ore and 16 obsidian.
Blueprint 8: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 11 clay. Each geode robot costs 3 ore and 14 obsidian.
Blueprint 9: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 11 clay. Each geode robot costs 2 ore and 19 obsidian.
Blueprint 10: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 19 clay. Each geode robot costs 2 ore and 12 obsidian.
Blueprint 11: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 7 clay. Each geode robot costs 2 ore and 16 obsidian.
Blueprint 12: Each ore robot costs 2 ore. Each clay robot costs 2 ore. Each obsidian robot costs 2 ore and 7 clay. Each geode robot costs 2 ore and 14 obsidian.
Blueprint 13: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 11 clay. Each geode robot costs 3 ore and 8 obsidian.
Blueprint 14: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 4 ore and 8 obsidian.
Blueprint 15: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 16 clay. Each geode robot costs 3 ore and 14 obsidian.
Blueprint 16: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 18 clay. Each geode robot costs 4 ore and 8 obsidian.
Blueprint 17: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 11 clay. Each geode robot costs 4 ore and 7 obsidian.
Blueprint 18: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 8 clay. Each geode robot costs 3 ore and 9 obsidian.
Blueprint 19: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 13 clay. Each geode robot costs 3 ore and 11 obsidian.
Blueprint 20: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 17 clay. Each geode robot costs 3 ore and 11 obsidian.
Blueprint 21: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 20 clay. Each geode robot costs 3 ore and 18 obsidian.
Blueprint 22: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 20 clay. Each geode robot costs 3 ore and 14 obsidian.
Blueprint 23: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 7 clay. Each geode robot costs 3 ore and 8 obsidian.
Blueprint 24: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 20 clay. Each geode robot costs 2 ore and 19 obsidian.
Blueprint 25: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 20 clay. Each geode robot costs 3 ore and 15 obsidian.
Blueprint 26: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 19 clay. Each geode robot costs 3 ore and 17 obsidian.
Blueprint 27: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 9 clay. Each geode robot costs 3 ore and 19 obsidian.
Blueprint 28: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 19 clay. Each geode robot costs 2 ore and 20 obsidian.
Blueprint 29: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 10 clay. Each geode robot costs 3 ore and 14 obsidian.
Blueprint 30: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 12 clay. Each geode robot costs 4 ore and 19 obsidian."""

    answer = AocDay19(data,silver_tests,gold_tests,argv)

    print(answer)
