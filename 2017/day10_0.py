datalen = 256
data = "225,171,131,2,35,5,0,13,1,246,54,97,255,98,254,110"

testdatalen = 5
test = "3,4,1,5"

def run(data,datalen):
	lengths = [int(i) for i in data.split(",")]
	nums = list(range(datalen))
	fst = 0
	skip = 0
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

	return nums[0]*nums[1]

print(run(test,testdatalen))
print(run(data,datalen))
