data = (699,124)
test = (65,8921)

class Generator:
	def __init__(self,val,mul,mask):
		self.val = val
		self.mul = mul
		self.mask = mask

	def next(self):
		while True:
			self.val = (self.val * self.mul) % 0x7FFFFFFF
			if self.val & self.mask == 0:
				break

	def lower(self):
		return self.val & 0xFFFF

def run(data):	
	vala,valb = data
	gena = Generator(vala,16807,0x3)
	genb = Generator(valb,48271,0x7)
	numpairs = 5000000
	ans = 0
	for _ in range(numpairs):
		gena.next()
		genb.next()
		if gena.lower() == genb.lower():
			ans += 1

	return ans

print(run(test))
print(run(data))
