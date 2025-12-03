from collections import Counter

data = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

def hand_rank(cards):
    FIVEOFAKIND = 7
    FOUROFAKIND = 6
    FULLHOUSE = 5
    THREEOFAKIND = 4
    TWOPAIRS = 3
    ONEPAIR = 2
    HIGHCARD = 1

    h = Counter(cards)
    num_different_cards = len(h)
    max_of_one_card = max(h.values())
    match num_different_cards:
        case 1: return FIVEOFAKIND
        case 2: return FOUROFAKIND if max_of_one_card == 4 else FULLHOUSE
        case 3: return THREEOFAKIND if max_of_one_card == 3 else TWOPAIRS
        case 4: return ONEPAIR
        case other: return HIGHCARD

J_AS_JACK = 11
J_AS_JOKER = 1
card_values = {"T":10,"J":J_AS_JACK,"Q":12,"K":13,"A":14,"9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2}
hands = []

for line in data.splitlines():
    hand,bet = line.split()
    hand = [card_values[c] for c in hand]
    sortable = [hand_rank(hand),hand,int(bet)]
    hands.append(sortable)
hands.sort()

total = 0
rank = 0
for hand in hands:
    rank += 1
    bet = hand[-1]
    total += rank * bet

print(total)
