datalen = 256
data = "225,171,131,2,35,5,0,13,1,246,54,97,255,98,254,110"

testdatalen = 256
test = ["","AoC 2017","1,2,3","1,2,4"]

def run(data,datalen):
	startlengths = [ord(i) for i in data] + [17, 31, 73, 47, 23]
	nums = list(range(datalen))
	fst = 0
	skip = 0
	for _ in range(64):
		lengths = list(startlengths)
		for l in lengths:
			lst = (fst + l) % datalen
			if l > 1:
				if lst > fst:
					nums[fst:lst] = nums[fst:lst][::-1]
				else:
					newnums = (nums[fst:]+nums[:lst])[::-1]
					mid = datalen - fst
					nums[fst:] = newnums[:mid]
					nums[:lst] = newnums[mid:]

			fst = (fst + l + skip) % datalen
			skip += 1

	ans = ""
	blocksize = 16
	for start in range(0,256,blocksize):
		dense = 0
		for i in range(start,start+blocksize):
			dense ^= nums[i]
		ans += "{:02x}".format(dense)

	return ans

for t in test:
	print(run(t,testdatalen))
print(run(data,datalen))
