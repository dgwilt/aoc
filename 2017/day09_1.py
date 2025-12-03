from re import sub,findall

data = open('day09_0.txt').read()

test = ["{{<!>},{<!>},{<!>},{<a>}}","{{{},{},{{}}}}",'<{o"i!a,<{i<a>']

def run(data):
	data = sub(r'!.','',data)
	ans = sum([len(garbage) for garbage in findall(r'<(.*?)>',data)])
	return ans

for t in test:
	print(run(t))
print(run(data))
