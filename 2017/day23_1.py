data = (105700, 122700, 17)

def literal_translation(fr, to, step):
	h = 0
	for b in range(fr, to + 1, step):
		f = 1
		for d in range(2, b + 1):
			for e in range(2, b + 1):
				if b == d * e:
					f = 0
		if f == 0:
			h += 1
	return h

def primesfrom3to(n):
    sieve = [True] * (n + 1)
    for x in range(3, int(n**0.5) + 1, 2):
        for y in range(3, (n//x) + 1, 2):
            sieve[x * y] = False

    return set([i for i in range(3, n, 2) if sieve[i]])

def optimized_translation(fr,to,step):
	to += 1
	primes = primesfrom3to(to)
	return len([n for n in range(fr, to, step) if n not in primes])

def run(data):
	fr, to, step = data
	#return literal_translation(fr, to, step) 
	return optimized_translation(fr, to, step)

print(run(data))
