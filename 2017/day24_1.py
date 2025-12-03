data = """31/13
34/4
49/49
23/37
47/45
32/4
12/35
37/30
41/48
0/47
32/30
12/5
37/31
7/41
10/28
35/4
28/35
20/29
32/20
31/43
48/14
10/11
27/6
9/24
8/28
45/48
8/1
16/19
45/45
0/4
29/33
2/5
33/9
11/7
32/10
44/1
40/32
2/45
16/16
1/18
38/36
34/24
39/44
32/37
26/46
25/33
9/10
0/29
38/8
33/33
49/19
18/20
49/39
18/39
26/13
19/32"""

test = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""

def otherend(part,start):
	return part[0] if start == part[1] else part[1]

def run(data):
	all_parts = set([tuple(int(i) for i in line.split("/")) for line in data.split("\n")])

	start = 0
	startparts = [part for part in all_parts if start in part]

	bridges = [set([part]) for part in startparts]
	ends = [otherend(part,start) for part in startparts]

	finishedbridges = []

	while bridges:
		nextbridges = []
		nextends = []
		for bridge, start in zip(bridges, ends): # The end of the bridge is the start of the next piece
			available_parts = all_parts - bridge
			nextparts = [p for p in available_parts if start in p]
			for part in nextparts:
				nextbridges.append(bridge | set([part]))
				nextends.append(otherend(part,start))

			if not nextparts:
				finishedbridges.append(bridge)
			
		bridges = nextbridges
		ends = nextends

	lengths = [len(bridge) for bridge in finishedbridges]
	longest = max(lengths)
	strengths = [sum([sum(part) for part in bridge]) for bridge in finishedbridges]
	return max([strengths[i] for i,l in enumerate(lengths) if l == longest])

print(run(test))
print(run(data))
