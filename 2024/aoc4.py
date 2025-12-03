data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

grid = data.splitlines()
width = len(grid[0])
height = len(grid)

xmas = 0
found = ["XMAS","SAMX"]
for x in range(width):
    for y in range(height):
        # Horizontal right
        if x <= width - 4 and grid[y][x:x+4] in found:
            xmas = xmas + 1
        # Vertical down
        if y <= height - 4 and "".join(grid[y+r][x] for r in range(4)) in found:
            xmas = xmas + 1
        # Diagonal down-right
        if y <= height - 4 and x <= width - 4 and "".join(grid[y+i][x+i] for i in range(4)) in found:
            xmas = xmas + 1
        # Diagonal up-right
        if y >= 3 and x <= width - 4 and "".join(grid[y-i][x+i] for i in range(4)) in found:
            xmas = xmas + 1

print(xmas)

xmas = 0
found = ["MSMS","MSSM","SMMS","SMSM"]
for x in range(width-2):
    for y in range(height-2):
        if grid[y+1][x+1] == "A":
            # Top-left, bottom-right, bottom-left, top-right
            corners = grid[x][y] + grid[y+2][x+2] + grid[y+2][x] + grid[y][x+2]
            if corners in found:
                xmas = xmas + 1

print(xmas)
