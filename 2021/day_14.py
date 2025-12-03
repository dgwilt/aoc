#!/usr/bin/env python3 
from collections import defaultdict
from sys import argv
from aoc import AocDay

class AocDay14(AocDay):

    @staticmethod
    def run_polymer(data,steps):
        template,insertions = data.split("\n\n")

        rules = {}
        for fr,to in [line.split(" -> ") for line in insertions.splitlines()]:
            rules[fr] = to

        polymer = defaultdict(int)
        for i in range(len(template)-1):
            polymer[template[i:i+2]] += 1

        for _ in range(steps):
            next_polymer = defaultdict(int)
            for pair,count in polymer.items():
                new_element = rules[pair]
                next_polymer[pair[0] + new_element] += count
                next_polymer[new_element + pair[1]] += count
            polymer = next_polymer

        elements = defaultdict(int)
        for pair,count in polymer.items():
            elements[pair[0]] += count
        elements[template[-1]] += 1

        return max(elements.values()) - min(elements.values())

    def run_silver(self,data):
        return AocDay14.run_polymer(data,10)

    def run_gold(self,data):
        return AocDay14.run_polymer(data,40)

if __name__ == "__main__":

    data = """SHPPPVOFPBFCHHBKBNCV

HK -> C
SP -> H
VH -> K
KS -> B
BC -> S
PS -> K
PN -> S
NC -> F
CV -> B
SH -> K
SK -> H
KK -> O
HO -> V
HP -> C
HB -> S
NB -> N
HC -> K
SB -> O
SN -> C
BP -> H
FC -> V
CF -> C
FB -> F
VP -> S
PO -> N
HN -> N
BS -> O
NF -> H
BH -> O
NK -> B
KC -> B
OS -> S
BB -> S
SV -> K
CH -> B
OB -> K
FV -> B
CP -> V
FP -> C
VC -> K
FS -> S
SS -> F
VK -> C
SF -> B
VS -> B
CC -> P
SC -> S
HS -> K
CN -> C
BN -> N
BK -> B
FN -> H
OK -> S
FO -> S
VB -> C
FH -> S
KN -> K
CK -> B
KV -> P
NP -> P
CB -> N
KB -> C
FK -> K
BO -> O
OV -> B
OC -> B
NO -> F
VF -> V
VO -> B
FF -> K
PP -> O
VV -> K
PC -> N
OF -> S
PV -> P
PB -> C
KO -> V
BF -> N
OO -> K
NV -> P
PK -> V
BV -> C
HH -> K
PH -> S
OH -> B
HF -> S
NH -> H
NN -> K
KF -> H
ON -> N
PF -> H
CS -> H
CO -> O
SO -> K
HV -> N
NS -> N
KP -> S
OP -> N
KH -> P
VN -> H"""

    silver_tests = ["""NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""",""""""]

    gold_tests = ["""""",""""""]

    answer = AocDay14(data,silver_tests,gold_tests,argv)

    print(answer)
