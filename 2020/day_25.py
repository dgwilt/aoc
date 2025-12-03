#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay

class AocDay25(AocDay):
    
    def transform(self,subject,loop):
        v = 1
        for _ in range(loop):
            v = v*subject % 20201227
        return v

    def find_loop(self,pk):
        v = 1
        l = 0
        subject = 7
        while v != pk:
            l += 1
            v = v*subject % 20201227
        return l

    def run_silver(self,data):
        pk_card, pk_door = [int(i) for i in data.splitlines()]
        loop_card = self.find_loop(pk_card)
        encryption_card = self.transform(pk_door,loop_card)
        return encryption_card
        
    def run_gold(self,data):
        self.setup(data)
        return AocDay.NOSOL

if __name__ == "__main__":

    silver_tests = ["""5764801
17807724""",""""""]

    gold_tests = ["""""",""""""]

    data = """8421034
15993936"""

    answer = AocDay25(data,silver_tests,gold_tests,argv)

    print(answer)
