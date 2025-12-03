#!/usr/local/bin/python3

data = '''Disc #1 has 7 positions; at time=0, it is at position 0.
Disc #2 has 13 positions; at time=0, it is at position 0.
Disc #3 has 3 positions; at time=0, it is at position 2.
Disc #4 has 5 positions; at time=0, it is at position 2.
Disc #5 has 17 positions; at time=0, it is at position 0.
Disc #6 has 19 positions; at time=0, it is at position 7.
Disc #7 has 11 positions; at time=0, it is at position 0.'''

import re

pat = re.compile(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).')

discs = {}

for line in data.split("\n"):
	mpat = pat.search(line)
	if mpat:
		(d,npos,start) = [int(i) for i in mpat.group(1,2,3)]
		discs[d] = {'npos':npos,'pos':start}


def get_capsule(discs):
	return (True if sum([(discs[d]['pos'] + d) % discs[d]['npos'] for d in discs]) == 0 else False)

t = 0
while not get_capsule(discs):
	for d in discs:
		discs[d]['pos'] += 1 % discs[d]['npos']
	t += 1

print(t)
