data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

def check(target,total,nums):
    if len(nums) == 0:
        return (target == total)
    else:
        next_num = nums[0]
        other_nums = nums[1:]
        return (   check(target,total + next_num,other_nums)
                or check(target,total * next_num,other_nums)
                # or check(target,int(str(total) + str(next_num)),other_nums) # Part two
                )

answer = 0
for line in data.splitlines():
    record = line.split(": ")
    target = int(record[0])
    nums = record[1].split(" ")
    for i in range(len(nums)):
        nums[i] = int(nums[i])
    if check(target,0,nums):
        answer = answer + target

print(answer)
