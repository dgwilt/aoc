#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay
from re import compile

class AocDay2(AocDay):

    def find_invalid(self,data,invalid):
        answer = 0
        for ids in data.split(","):
            fr,to = [int(i) for i in ids.split("-")]
            answer += sum(id for id in range(fr,to+1) if invalid.match(str(id)))
        return answer

    def run_silver(self,data):
        return self.find_invalid(data,compile(r'\A(\d+)\1\Z'))
        
    def run_gold(self,data):
        return self.find_invalid(data,compile(r'\A(\d+)(\1)+\Z'))

if __name__ == "__main__":

    silver_tests = ["""11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124""",""""""]

    gold_tests = ["""""",""""""]

    data = """2200670-2267527,265-409,38866-50720,7697424-7724736,33303664-33374980,687053-834889,953123-983345,3691832-3890175,26544-37124,7219840722-7219900143,7575626241-7575840141,1-18,1995-2479,101904-163230,97916763-98009247,52011-79060,31-49,4578-6831,3310890-3365637,414256-608125,552-1005,16995-24728,6985-10895,878311-912296,59-93,9978301-10012088,17302200-17437063,1786628373-1786840083,6955834840-6955903320,983351-1034902,842824238-842861540,14027173-14217812"""

    answer = AocDay2(data,silver_tests,gold_tests,argv)

    print(answer)
