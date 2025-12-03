data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

grid = []
for row in data.splitlines():
    grid.append(list(row))

width = len(grid[0])
height = len(grid)

# Find all the symbols in the grid
surrounding = [[0,1],[0,-1],[1,0],[-1,0],[-1,-1],[-1,1],[1,1],[1,-1]]
total = 0
for sx0 in range(width):
    for sy0 in range(height):
        symCheck = grid[sy0][sx0]
        if symCheck != "." and not symCheck.isdigit(): # Any symbol
            numbersAroundSymbol = []
            for dx,dy in surrounding:
                x0 = sx0 + dx
                y0 = sy0 + dy
                if grid[y0][x0].isdigit():
                    for searchx in (1,-1):
                        x = x0 + searchx
                        while 0 <= x < width and grid[y0][x].isdigit():
                            if searchx == 1:
                                # Moving right from original
                                grid[y0][x0] += grid[y0][x]
                            elif searchx == -1:
                                # Moving left from original
                                grid[y0][x0] = grid[y0][x] + grid[y0][x0]

                            grid[y0][x] = "."
                            x += searchx

                    numbersAroundSymbol.append(int(grid[y0][x0]))
            total += sum(numbersAroundSymbol)
            
print(total)
