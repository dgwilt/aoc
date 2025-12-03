#!/usr/local/bin/python3

data = "01111001100111011"
length1 = 272
length2 = 35651584

def run(length):
	a = data
	trans = str.maketrans("01", "10")
	while len(a) < length:
		b = a[::-1].translate(trans)
		a = a + "0" + b

	a = a[:length]
	checksum = ""
	
	while True:
		for i in range(0,len(a),2):
			checksum += "1" if a[i] == a[i+1] else "0"
		if len(checksum) % 2 != 0:
			break
		a,checksum = checksum,""

	return checksum

print(run(length1))
print(run(length2))
