#!/usr/local/bin/python3
from itertools import combinations

class Finished(Exception):
    pass

def get_digest(floors,lift):
	digest = ",".join(("{},{},{},{}".format(i,
						"L" if i == lift else ".",
						"".join(sorted(f['C'])),
						"".join(sorted(f['R']))) for i,f in enumerate(floors)))
	return digest

def floor_safe(chips,rtgs):
	if len(rtgs) == 0:
		return True
	else:
		for c in chips:
			if c not in rtgs:
				return False
		return True

def score(floors):
	# Items get a higher score for being on a higher floor
	return sum(((i+1)*(len(floors[i]['C']) + len(floors[i]['R'])) for i in range(len(floors))))

def all_things_to_move(chips,rtgs):
	for both in (c for c in chips if c in rtgs):
		yield {'C':[both],'R':[both]}
		break

	for noof_items in (2,1):
		for c in combinations(chips,noof_items):
			yield {'C':list(c),'R':[]}
		for r in combinations(rtgs,noof_items):
			yield {'R':list(r),'C':[]}

def get_next_states(state,visited,maxscore):
	floors = state[0]
	lift_from = state[1]

	# Find where the lift_from is
	floor = floors[lift_from]
	chips = floor['C']
	rtgs = floor['R']

	next_states = []
	for move in all_things_to_move(chips,rtgs):
		chip_from = [c for c in chips if c not in move['C']]
		rtg_from = [r for r in rtgs if r not in move['R']]
		if floor_safe(chip_from,rtg_from):
			for lift_to in (f for f in (lift_from+1,lift_from-1) if f in range(len(floors))):
				floor_to = floors[lift_to]
				chip_to = floor_to['C'] + move['C']
				rtg_to = floor_to['R'] + move['R']
				# Check if the floor we are moving to is also safe
				if floor_safe(chip_to,rtg_to):
					# Have to take a copy of floors here so we don't change the original list
					next_floors = floors[:]
					next_floors[lift_from] = {'C':chip_from,'R':rtg_from}
					next_floors[lift_to] = {'C':chip_to,'R':rtg_to}
					# Return states that we have not visited before
					digest = get_digest(next_floors,lift_to)
					if digest not in visited:
						s = score(next_floors)
						if s == maxscore:
							raise Finished
						next_states.append((next_floors,lift_to,s))
						visited.add(digest)

	return next_states

def run(prune,floors):
	items = sum((len(f['C']) for f in floors))
	lift = 0
	maxscore = items * 2 * len(floors)

	cur_states = [(floors,lift,score(floors))]
	visited = set([get_digest(floors,lift)])

	moves = 0
	while True:
		next_states = []
		moves += 1
		for state in cur_states:
			try:
				next_states.extend(get_next_states(state,visited,maxscore))
			except Finished:
				return moves
		next_states.sort(key=lambda x: x[2],reverse=True)
		# Trim to the top promising states
		cur_states = next_states[:prune]
		print(".",end="",flush=True)

# Generate the starting data structure by hand rather than parse the input
floors = [
	{'C':['P','S'],			'R':['P','S']},			# Floor 1
	{'C':['R','C'],			'R':['T','R','C']},		# Floor 2
	{'C':['T'],				'R':[]},				# Floor 3
	{'C':[],				'R':[]}					# Floor 4
]

# Increase the pruning level if not getting the right answer!
prune = 1000

print("\nAnswer 1 =",run(prune,floors))

# Generate the starting data structure by hand rather than parse the input
floors = [
	{'C':['P','S','D','E'],	'R':['P','S','D','E']},	# Floor 1
	{'C':['R','C'],			'R':['T','R','C']},		# Floor 2
	{'C':['T'],				'R':[]},				# Floor 3
	{'C':[],				'R':[]}					# Floor 4
]

# Increase the pruning level if not getting the right answer!
prune = 7500

print("\nAnswer 2 =",run(prune,floors))

