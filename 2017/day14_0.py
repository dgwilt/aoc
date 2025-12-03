from day10_1 import run as knothash

data = "jzgqcdpd"
test = "flqrgnkx"

def run(data):
	return sum(["{:b}".format(int(knothash("{}-{}".format(data,i),256),16)).count("1") for i in range(128)])

print(run(test))
print(run(data))
