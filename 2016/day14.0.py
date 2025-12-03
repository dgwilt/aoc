#!/usr/local/bin/python3
data='qzyelonm'
#data = 'abc'

from hashlib import md5
import re

index = 0
pwd = ""

threes = {}
success = set()

def get_digest(num):
	return md5("{}{}".format(data,num).encode('utf-8')).hexdigest()

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

	if len(success) >= 100:
		s = sorted(list(success))
		print(s[63])
		break

	index += 1
