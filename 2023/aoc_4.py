data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

total = 0
for line in data.splitlines():
    numbers = line.split(": ")[1]
    wins,mine = numbers.split(" | ")
    
    winning_numbers = set(wins)
    my_numbers = set(mine)

    matches = len(winning_numbers & my_numbers)
    if matches != 0:
        total = total + 2**(matches - 1)

print(total)
