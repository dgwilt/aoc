#!/usr/local/bin/python3

data = ".^^^^^.^^^..^^^^^...^.^..^^^.^^....^.^...^^^...^^^^..^...^...^^.^.^.......^..^^...^.^.^^..^^^^^...^."

# Transform safe into 1 and trap into 0
first_row = [1 if c == "." else 0 for c in data]
first_safe = sum(first_row)
midlen = len(data)-1

rows1 = 40
rows2 = 400000

def run(rows):
	next_row = first_row
	answer = first_safe

	for row in range(rows-1):
		this_row = next_row
		# Some boolean algebra can show that this is the formula for the next row
		next_row = [this_row[1]] + [1 if this_row[i+1] == this_row[i-1] else 0 for i in range(1,midlen)] + [this_row[-2]]
		answer += sum(next_row)
	return answer

print(run(rows1))
print(run(rows2))
