from itertools import combinations

data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

grid = data.splitlines()
width = len(grid[0])
height = len(grid)
city = set()
antennas = {}

for x in range(width):
    for y in range(height):
        pos = (x,y)
        city.add(pos)
        frequency = grid[y][x]
        if frequency != ".":
            if frequency not in antennas:
                antennas[frequency] = []
            antennas[frequency].append(pos)

antinodes = set()
for pos in antennas.values():
    for a,b in combinations(pos, 2):
        ab = (b[0] - a[0], b[1] - a[1])    # Vector from a to b

        b_plus_ab = (b[0] + ab[0], b[1] + ab[1])
        if b_plus_ab in city:
            antinodes.add(b_plus_ab)

        a_minus_ab = (a[0] - ab[0], a[1] - ab[1])
        if a_minus_ab in city:
            antinodes.add(a_minus_ab)

print(len(antinodes))
