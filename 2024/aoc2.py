data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

safe = 0

levels = data.splitlines()
for level in levels:
    row = level.split()
    for i in range(len(row)):
        row[i] = int(row[i])

    # NB for later; row with position x removed is row[:x] + row[x+1:]

    # Calculate changes
    deltas = []
    for i in range(len(row)-1):
        deltas.append(row[i+1] - row[i])

    # Are they all increasing or decreasing?
    increasing = True
    decreasing = True
    for d in deltas:
        if d < 0:
            increasing = False
        if d > 0:
            decreasing = False

    # Are the changes in range?
    gapOk = True
    for d in deltas:
        if abs(d) < 1 or abs(d) > 3:
            gapOk = False
            break

    if gapOk and (increasing or decreasing):
        safe = safe + 1

print(safe)
