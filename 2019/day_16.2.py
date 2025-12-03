#!/usr/bin/env python3 

data = [100,"59775675999083203307460316227239534744196788252810996056267313158415747954523514450220630777434694464147859581700598049220155996171361500188470573584309935232530483361639265796594588423475377664322506657596419440442622029687655170723364080344399753761821561397734310612361082481766777063437812858875338922334089288117184890884363091417446200960308625363997089394409607215164553325263177638484872071167142885096660905078567883997320316971939560903959842723210017598426984179521683810628956529638813221927079630736290924180307474765551066444888559156901159193212333302170502387548724998221103376187508278234838899434485116047387731626309521488967864391"]

tests = [[100,"03036732577212944063491565474664"]]

# The trick here is that if the offset puts your pattern in the second half of the list, then it is simply the sum of the last n items (mod 10), which you can iterate through. Then produce your total working from the back of the list to keep your partial sums and save work.
def phase(nums):
    total = 0
    for i in range(1,len(nums)+1):
        total += nums[-i]
        total %= 10
        nums[-i] = total

def run(data):
    phases, nums = data
    offset = int(nums[:7])
    nums *= 10000
    assert(offset >= len(nums)//2 and offset < len(nums))
    nums = [int(i) for i in nums[offset:]]
    for _ in range(phases):
        phase(nums)

    return "".join([str(i) for i in nums[:8]])

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: 
        print(f"Error: {e}")

print(run(data))