#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay
from math import lcm, prod

class AocDay11(AocDay):

    def parse_monkeys(self,data):
        monkeys = []
        for monkey_text in data.split("\n\n"):
            items,opstr,mod,ift,iff = monkey_text.splitlines()[1:]
            monkeys.append({
                'total' : 0,
                'items' : [int(i) for i in items.split(":")[1].split(", ")],
                'opstr' : opstr.split("=")[1].strip().replace("old","{old}"),
                'mod'   : int(mod.split()[-1]),
                'throw' : (int(iff.split()[-1]),int(ift.split()[-1])),
            })
        return monkeys

    def run_rounds(self,monkeys,rounds,op):
        for _ in range(rounds):
            for monkey in monkeys:
                monkey['total'] += len(items := monkey['items'])
                for item in items:
                    worry = op(eval(monkey['opstr'].format(old=item)))
                    # Favourite line - use bool as 0/1 index into tuple
                    throw_to = monkey['throw'][worry % monkey['mod'] == 0]
                    monkeys[throw_to]['items'].append(worry)
                monkey['items'] = []

        return prod(sorted([m['total'] for m in monkeys])[-2:])

    def run_silver(self,data):
        return self.run_rounds(self.parse_monkeys(data),20,lambda w : w // 3)
        
    def run_gold(self,data):
        monkeys = self.parse_monkeys(data)
        mod = lcm(*[m['mod'] for m in monkeys])
        return self.run_rounds(monkeys,10000,lambda w : w % mod)

if __name__ == "__main__":

    silver_tests = ["""Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""",""""""]

    gold_tests = ["""""",""""""]

    data = """Monkey 0:
  Starting items: 57, 58
  Operation: new = old * 19
  Test: divisible by 7
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 66, 52, 59, 79, 94, 73
  Operation: new = old + 1
  Test: divisible by 19
    If true: throw to monkey 4
    If false: throw to monkey 6

Monkey 2:
  Starting items: 80
  Operation: new = old + 6
  Test: divisible by 5
    If true: throw to monkey 7
    If false: throw to monkey 5

Monkey 3:
  Starting items: 82, 81, 68, 66, 71, 83, 75, 97
  Operation: new = old + 5
  Test: divisible by 11
    If true: throw to monkey 5
    If false: throw to monkey 2

Monkey 4:
  Starting items: 55, 52, 67, 70, 69, 94, 90
  Operation: new = old * old
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 3

Monkey 5:
  Starting items: 69, 85, 89, 91
  Operation: new = old + 7
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 7

Monkey 6:
  Starting items: 75, 53, 73, 52, 75
  Operation: new = old * 7
  Test: divisible by 2
    If true: throw to monkey 0
    If false: throw to monkey 4

Monkey 7:
  Starting items: 94, 60, 79
  Operation: new = old + 2
  Test: divisible by 3
    If true: throw to monkey 1
    If false: throw to monkey 6"""

    answer = AocDay11(data,silver_tests,gold_tests,argv)

    print(answer)
