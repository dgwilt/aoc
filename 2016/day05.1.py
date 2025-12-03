#!/usr/local/bin/python3
data=b'reyedfim'

import hashlib
num = 0
pwd = [None]*8
got = 0

while got < 8:
	m = hashlib.md5()
	m.update(data)
	m.update(str(num).encode('utf-8'))
	d = m.hexdigest()
	if d[:5] == "00000":
		if d[5].isdigit():
			pos = int(d[5])
			if pos < 8 and pwd[pos] is None:
				pwd[pos] = d[6]
				got += 1
	num += 1

print("".join(pwd))
