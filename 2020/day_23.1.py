#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay

class AocDay23(AocDay):

    def play_cups(self,moves,cupnums):
        highest = max(cupnums)
        label = cupnums[0]
        self.after = {cupnums[i]:cupnums[i+1] for i in range(len(cupnums)-1)}
        self.after[cupnums[-1]] = label
        for _ in range(moves):
            takenums = []
            n = label
            for _ in range(3):
                n = self.after[n]
                takenums.append(n)
            self.after[label] = self.after[n]

            dst = label - 1
            if dst == 0: dst = highest
            while dst in takenums:
                dst -= 1
                if dst == 0: dst = highest

            self.after[dst], self.after[takenums[-1]] = takenums[0], self.after[dst]
            label = self.after[label]

    def run_silver(self,data):
        cupnums = [int(c) for c in data]
        self.play_cups(100,cupnums)
        n = self.after[1]
        result = ""
        for _ in range(8):
            result += str(n)
            n = self.after[n]
        return result
        
    def run_gold(self,data):
        cupnums = [int(i) for i in data] + [i for i in range(len(data)+1,1000001)]
        self.play_cups(10000000,cupnums)
        n1 = self.after[1]
        n2 = self.after[n1]
        return n1 * n2

if __name__ == "__main__":

    silver_tests = ["389125467"]

    gold_tests = ["""""",""""""]

    data = "219347865"

    answer = AocDay23(data,silver_tests,gold_tests,argv)

    print(answer)
