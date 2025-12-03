#!/usr/local/bin/python3
data='qzyelonm'

from hashlib import md5
import re

index = 0
pwd = ""

threes = {}
success = set()

def get_digest(num):
	tohash = "{}{}".format(data,num)
	for _ in range(2017):
		digest = md5(tohash.encode('utf-8')).hexdigest()
		tohash = digest
	return digest

while True:
	digest = get_digest(index)

	for p in re.findall(r'(.)\1\1',digest):
		if p not in threes:
			threes[p] = []
		threes[p].append(index)
		# Only take the first match
		break

	for five in re.findall(r'(.)\1\1\1\1',digest):
		if five in threes:
			for three in threes[five]:
				if three < index and three > index - 999:
					success.add(three)

	# Need to go higher than 63 to pick up all possible sets of three
	if len(success) >= 100:
		s = sorted(list(success))
		print(s[63])
		break

	index += 1
