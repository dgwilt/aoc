data = """2333133121414131402"""

id = 0
block = 0
used = []
free = []
is_used_block = True

for i in range(len(data)):
    size = int(data[i])
    if size > 0:
        block_descriptor = [block,size,id]
        if is_used_block:
            used.append(block_descriptor)
        else:
            free.append(block_descriptor)
    block += size
    if is_used_block:
        id += 1
    is_used_block = not is_used_block

BLOCK,SIZE,ID = 0,1,2
END = -1 # Used blocks comes from the end
START = 0 # Free blocks come from the start

reallocated = []
while used[END][BLOCK] > free[START][BLOCK]:
    transfer_size = min(free[START][SIZE], used[END][SIZE])

    block_descriptor = [free[START][BLOCK],transfer_size,used[END][ID]]
    reallocated.append(block_descriptor)

    used[END][SIZE] -= transfer_size
    if used[END][SIZE] == 0:
        del used[END]

    free[START][SIZE] -= transfer_size
    free[START][BLOCK] += transfer_size
    if free[START][SIZE] == 0:
        del free[START]

answer = 0
for (block,size,id) in used + reallocated:
    for b in range(block,block+size):
        answer = answer + (b * id)
print(answer)
