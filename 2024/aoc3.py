import re

data = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

result = 0
for instruction in re.findall(r"mul\(\d+,\d+\)",data):
    instruction = instruction[4:-1]
    nums = instruction.split(",")
    a = int(nums[0])
    b = int(nums[1])
    result = result + (a * b)

print(result)
