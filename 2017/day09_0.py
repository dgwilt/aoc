from re import sub

data = open('day09_0.txt').read()

test = ["{{<!>},{<!>},{<!>},{<a>}}","{{{},{},{{}}}}"]

def run(data):
	data = sub(r'!.','',data)
	data = sub(r'<.*?>','',data)
	depth = 0
	ans = 0
	for l in data:
		if l == "{":
			depth += 1
		elif l == "}":
			ans += depth
			depth -= 1

	return ans

for t in test:
	print(run(t))
print(run(data))
