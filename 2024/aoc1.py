data = """3   4
4   3
2   5
1   3
3   9
3   3"""

firstcol = []
secondcol = []
for line in data.splitlines():
    nums = line.split()
    a = int(nums[0])
    b = int(nums[1])
    firstcol.append(a)
    secondcol.append(b)

firstcol.sort()
secondcol.sort()

numlines = len(firstcol)
silver_answer = 0
for count in range(numlines):
    a = firstcol[count]
    b = secondcol[count]
    distance = abs(a-b)
    silver_answer = silver_answer + distance

print(silver_answer)

gold_answer = 0
for num in firstcol:
    gold_answer = gold_answer + num * secondcol.count(num)

print(gold_answer)
