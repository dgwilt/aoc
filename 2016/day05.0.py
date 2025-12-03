#!/usr/local/bin/python3
data=b'reyedfim'

import hashlib
num = 0
pwd = ""
while len(pwd) < 8:
	m = hashlib.md5()
	m.update(data)
	m.update(str(num).encode('utf-8'))
	d = m.hexdigest()
	if d[:5] == "00000":
		pwd += d[5]
	num += 1

print(pwd)
