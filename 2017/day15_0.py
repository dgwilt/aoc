data = (699,124)
test = (65,8921)

class Generator:
	def __init__(self,val,mul):
		self.val = val
		self.mul = mul

	def next(self):
		self.val = (self.val * self.mul) % 0x7FFFFFFF

	def lower(self):
		return self.val & 0xFFFF

def run(data):
	vala,valb = data
	gena = Generator(vala,16807)
	genb = Generator(valb,48271)
	numpairs = 40000000
	ans = 0
	for _ in range(numpairs):
		gena.next()
		genb.next()
		if gena.lower() == genb.lower():
			ans += 1

	return ans

print(run(test))
print(run(data))
