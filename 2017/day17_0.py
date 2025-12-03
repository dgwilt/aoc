
data = (324,2018)

test = (3,9)

def run(data):
	step,loops = data
	buf = [0]
	pos = 0
	for i in range(1,loops):
		pos = (pos + step) % len(buf)
		buf.insert(pos+1,i)
		pos += 1

	return buf[(pos + 1) % len(buf)]

print(run(test))
print(run(data))
