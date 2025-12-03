#!/usr/local/bin/python3
from hashlib import md5

data = "pxxbnzuo"

def isopen(d):
	dooropen = "bcdef"
	return d in dooropen

def get_next_states(state):
	(up,down,left,right) = [i for i in range(4)]
	path = state[1]
	x = state[0][0]
	y = state[0][1]
	doors = md5((data+path).encode('utf-8')).hexdigest()[:4]
	next_states = []
	if isopen(doors[up]) and y > 0:
		ns = ((x,y-1),path+"U")
		next_states.append(ns)
	if isopen(doors[down]) and y < 3:
		ns = ((x,y+1),path+"D")
		next_states.append(ns)
	if isopen(doors[right]) and x < 3:
		ns = ((x+1,y),path+"R")
		next_states.append(ns)
	if isopen(doors[left]) and x > 0:
		ns = ((x-1,y),path+"L")
		next_states.append(ns)
	return next_states

def run():
	vault = (3,3)
	start = (0,0)
	cur_states = [(start,"")]
	while True:
		next_states = []
		for state in cur_states:
			if state[0] == vault:
				longest = len(state[1])
				continue
			next_states.extend(get_next_states(state))
		if len(next_states) == 0:
			return longest
		cur_states = next_states

print(run())
