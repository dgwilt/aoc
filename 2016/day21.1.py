#!/usr/local/bin/python3
import re

data = '''move position 2 to position 6
move position 0 to position 5
move position 6 to position 4
reverse positions 3 through 7
move position 1 to position 7
swap position 6 with position 3
swap letter g with letter b
swap position 2 with position 3
move position 4 to position 3
move position 6 to position 3
swap position 4 with position 1
swap letter b with letter f
reverse positions 3 through 4
swap letter f with letter e
reverse positions 2 through 7
rotate based on position of letter h
rotate based on position of letter a
rotate based on position of letter e
rotate based on position of letter h
rotate based on position of letter c
move position 5 to position 7
swap letter a with letter d
move position 5 to position 6
swap position 4 with position 0
swap position 4 with position 6
rotate left 6 steps
rotate right 4 steps
rotate right 5 steps
swap letter f with letter e
swap position 2 with position 7
rotate based on position of letter e
move position 4 to position 5
swap position 4 with position 2
rotate right 1 step
swap letter b with letter f
rotate based on position of letter b
reverse positions 3 through 5
move position 3 to position 1
rotate based on position of letter g
swap letter c with letter e
swap position 7 with position 3
move position 0 to position 3
rotate right 6 steps
reverse positions 1 through 3
swap letter d with letter e
reverse positions 3 through 5
move position 0 to position 3
swap letter c with letter e
move position 2 to position 7
swap letter g with letter b
rotate right 0 steps
reverse positions 1 through 3
swap letter h with letter d
move position 4 to position 0
move position 6 to position 3
swap letter a with letter c
reverse positions 3 through 6
swap letter h with letter g
move position 7 to position 2
rotate based on position of letter h
swap letter b with letter h
reverse positions 2 through 6
move position 6 to position 7
rotate based on position of letter a
rotate right 7 steps
reverse positions 1 through 6
move position 1 to position 6
rotate based on position of letter g
rotate based on position of letter d
move position 0 to position 4
rotate based on position of letter e
rotate based on position of letter d
rotate based on position of letter a
rotate based on position of letter a
rotate right 4 steps
rotate based on position of letter b
reverse positions 0 through 4
move position 1 to position 7
rotate based on position of letter e
move position 1 to position 7
swap letter f with letter h
move position 5 to position 1
rotate based on position of letter f
reverse positions 0 through 1
move position 2 to position 4
rotate based on position of letter a
swap letter b with letter d
move position 6 to position 0
swap letter e with letter b
rotate right 7 steps
move position 2 to position 7
rotate left 4 steps
swap position 6 with position 1
move position 3 to position 5
rotate right 7 steps
reverse positions 0 through 6
swap position 2 with position 1
reverse positions 4 through 6
rotate based on position of letter g
move position 6 to position 4'''

pwd = list('fbgdceah')

patterns = {
	'sp' : re.compile(r'swap position (\d+) with position (\d+)'),
	'sl' : re.compile(r'swap letter (\w) with letter (\w)'),
	'rn' : re.compile(r'rotate (left|right) (\d+) step'),
	'rl' : re.compile(r'rotate based on position of letter (\w)'),
	'rv' : re.compile(r'reverse positions (\d) through (\d)'),
	'mv' : re.compile(r'move position (\d) to position (\d)')
	}

for line in data.splitlines()[::-1]:

	for t,regex in patterns.items():
		m = regex.match(line)
		if m:
			break
			
	if t == 'sp':
		(p1,p2) = [int(i) for i in m.group(1,2)]
		pwd[p1],pwd[p2] = pwd[p2],pwd[p1]
	elif t == 'sl':
		(l1,l2) = m.group(1,2)
		p1 = pwd.index(l1)
		p2 = pwd.index(l2)
		pwd[p1],pwd[p2] = pwd[p2],pwd[p1]
	elif t == 'rn':
		(d,n) = m.group(1,2)
		n = int(n) if d[0] == 'r' else -int(n)
		pwd = pwd[n:] + pwd[:n]
	elif t == 'rl':
		l = m.group(1)
		rot = 0
		while True:
			pwd = pwd[1:] + pwd[:1]
			rot += 1
			p = pwd.index(l)
			n = (1 + p + (1 if p >= 4 else 0)) % len(pwd)
			if n == (rot % len(pwd)):
				break
	elif t == 'rv':
		(p1,p2) = [int(i) for i in m.group(1,2)]
		pwd = pwd[:p1] + pwd[p1:p2+1][::-1] + pwd[p2+1:]
	elif t == 'mv':
		(p1,p2) = [int(i) for i in m.group(1,2)]
		pwd.insert(p1,pwd.pop(p2))

print("".join(pwd))
