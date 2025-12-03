#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay

class AocDay22(AocDay):

    def winning_hand_score(self):
        l = len(self.winning_hand)
        return sum(n*(l-i) for i,n in enumerate(self.winning_hand))

    def setup(self,data):
        return [tuple([int(card) for card in player.splitlines()[1:]]) for player in data.split("\n\n")]

    def nexthands(self,hands):
        w = self.winner
        winnings = (hands[w][0],hands[1-w][0])
        return [h[1:] + (winnings if p == w else ()) for p,h in enumerate(hands)]

    def set_winner_by_highest(self,hands):
        self.winner = hands[0][0] < hands[1][0]

    def set_winner(self,hands):
        for player,h in enumerate(hands):
            if h:
                self.winner = player
                self.winning_hand = h
                return

    def run_silver(self,data):
        hands = self.setup(data)
        while all(hands):
            self.set_winner_by_highest(hands)
            hands = self.nexthands(hands)

        self.set_winner(hands)
        return self.winning_hand_score()

    def end_because_already_seen(self,hands,seen):
        for h,s in zip(hands,seen):
            if h in s:
                self.winner = 0
                self.winning_hand = hands[0]
                return True
            s.add(h)
        return False

    def set_winner_by_combat(self,hands):
        seen = [set() for _ in range(len(hands))]
        while all(hands):
            if self.end_because_already_seen(hands,seen): return

            if any(len(h) - 1 < h[0] for h in hands):
                self.set_winner_by_highest(hands)
            else:
                self.set_winner_by_combat([h[1:1+h[0]] for h in hands])

            hands = self.nexthands(hands)

        self.set_winner(hands)

    def run_gold(self,data):
        self.set_winner_by_combat(self.setup(data))
        return self.winning_hand_score()

if __name__ == "__main__":

    silver_tests = ["""Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""",""""""]

    gold_tests = ["""Player 1:
43
19

Player 2:
2
29
14""",""""""]

    data = """Player 1:
28
3
35
27
19
40
14
15
17
22
45
47
26
13
32
38
43
24
29
5
31
48
49
41
25

Player 2:
34
12
2
50
16
1
44
11
36
6
10
42
20
8
46
9
37
4
7
18
23
39
30
33
21"""

    answer = AocDay22(data,silver_tests,gold_tests,argv)

    print(answer)
