#!/usr/bin/env python3 

data = [10007,"""deal with increment 41
cut 6859
deal with increment 23
cut -4435
deal into new stack
deal with increment 27
cut -337
deal with increment 50
cut 5290
deal into new stack
deal with increment 59
cut -9939
deal with increment 32
cut 4074
deal with increment 25
cut -2391
deal into new stack
deal with increment 40
cut -8095
deal with increment 44
cut 9150
deal with increment 5
cut -5330
deal with increment 61
cut -1038
deal with increment 3
cut 2873
deal with increment 56
cut 6080
deal with increment 59
cut -6859
deal with increment 21
cut -2316
deal with increment 42
cut -8349
deal with increment 60
cut 5774
deal with increment 63
cut -1754
deal with increment 48
cut 4009
deal with increment 10
cut -7026
deal with increment 73
cut 3867
deal into new stack
cut 3754
deal with increment 23
cut 4222
deal with increment 23
deal into new stack
cut 7294
deal into new stack
deal with increment 13
cut -9537
deal with increment 20
cut 2910
deal with increment 30
deal into new stack
cut 9409
deal with increment 23
deal into new stack
deal with increment 32
cut 6945
deal with increment 21
deal into new stack
cut -3297
deal with increment 75
cut -5300
deal into new stack
deal with increment 29
cut 8131
deal with increment 50
cut -8998
deal with increment 19
cut -1983
deal with increment 13
deal into new stack
cut -7555
deal with increment 62
cut 5612
deal with increment 14
cut -412
deal with increment 46
cut -7349
deal with increment 57
cut -8783
deal with increment 33
deal into new stack
deal with increment 56
cut 4283
deal into new stack
cut 8053
deal with increment 7
cut -2776
deal with increment 66
cut -9633
deal with increment 62
deal into new stack
deal with increment 12"""]

tests = [[10,"""deal with increment 7
deal into new stack
deal into new stack
"""],[10,"""cut 6
deal with increment 7
deal into new stack"""],[10,"""deal with increment 7
deal with increment 9
cut -2"""],[10,"""deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""]]

def run(data):
    ncards,inst = data
    cards = list(range(ncards))
    for line in inst.splitlines():
        words = line.split()
        if words[0] == "cut":
            n = int(words[1])
            cards = cards[n:] + cards[:n]
        elif words[1] == "into":
            cards.reverse()
        else:
            inc = int(words[3])
            pos = 0
            nextcards = [None] * ncards
            for i in range(ncards):
                while nextcards[pos] != None: pos = (pos + 1) % ncards
                nextcards[pos] = cards[i]
                pos = (pos + inc) % ncards
            cards = nextcards

    if len(cards) > 10:
        return cards.index(2019)
    else:
        return cards

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: 
        print(f"Error: {e}")

print(run(data))