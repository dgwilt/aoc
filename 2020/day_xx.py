#!/usr/bin/env python3 
from re import compile, sub, search
from itertools import combinations, permutations, product
from collections import defaultdict, Counter, deque
from string import ascii_uppercase, ascii_lowercase
from sys import argv
from aoc import AocDay, prod
from functools import reduce, partial
from math import ceil

class AocDayX(AocDay):

    def __init__(self,*args):
        super().__init__(*args)
        self.parser_setup(types=( ), pat=r' ')

    def setup(self,data):
        pass

    def run_silver(self,data):
        self.setup(data)
        return AocDay.NOSOL
        
    def run_gold(self,data):
        self.setup(data)
        return AocDay.NOSOL

if __name__ == "__main__":

    data = """"""

    silver_tests = ["""""",""""""]

    gold_tests = ["""""",""""""]

    answer = AocDayX(data,silver_tests,gold_tests,argv)

    print(answer)
