
data = (324,50000000)
test = (3,50)

def run(data):
	step,loops = data
	buflen = 1
	ans = None
	pos = 0
	for i in range(1,loops):
		pos = (pos + step) % buflen
		if pos == 0:
			ans = i
		buflen += 1
		pos += 1

	return ans

print(run(test))
print(run(data))
