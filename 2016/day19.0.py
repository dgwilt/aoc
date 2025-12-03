#!/usr/local/bin/python3

noof_elves = 3012210

class Elf:
	def __init__(self,number):
		self.number = number
		self.left = None
		self.right = None

	def take_position(self,l,r):
		self.right = r
		self.left = l

	def take_presents(self):
		self.right.left = self.left
		self.left.right = self.right

elves = {e:Elf(e+1) for e in range(noof_elves)}

for e in range(noof_elves):
	elves[e].take_position(
		elves[(e+1)%noof_elves],
		elves[(e-1)%noof_elves])

current = elves[0]

for _ in range(noof_elves-1):
	current.left.take_presents()
	current = current.left

print(current.number)
