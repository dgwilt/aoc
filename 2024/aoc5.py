data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

parsed = data.split("\n\n")
rules = parsed[0]
updates = parsed[1]

before = {}
after = {}
for rule in rules.splitlines():
    nums = rule.split("|")
    a = int(nums[0])
    b = int(nums[1])
    if b not in before:
        before[b] = []
    before[b].append(a)
    if a not in after:
        after[a] = []
    after[a].append(b)

pageTable = []
for update in updates.splitlines():
    nums = update.split(",")
    for i in range(len(nums)):
        nums[i] = int(nums[i])
    pageTable.append(nums)

silver_answer = 0
gold_answer = 0
for pages in pageTable:
    mid = len(pages)//2

    in_order = True
    for i in range(len(pages)):
        pnum = pages[i]
        must_be_after = after.get(pnum,[])
        must_be_before = before.get(pnum,[])
        pages_after = pages[i+1:]
        pages_before = pages[:i]
        if (any(p in must_be_before for p in pages_after) or 
            any(p in must_be_after for p in pages_before)):
            in_order = False
            break

    if in_order:
        silver_answer = silver_answer + pages[mid]
    else:
        ordered = [pages[0]]
        for pnum in pages[1:]:
            must_be_after = after.get(pnum,[])
            must_be_before = before.get(pnum,[])
            inserted = False
            for i in range(len(ordered)):
                pages_after = ordered[i:]
                pages_before = ordered[:i]
                if not(any(p in must_be_before for p in pages_after) or 
                       any(p in must_be_after for p in pages_before)):
                    ordered.insert(i,pnum)
                    inserted = True
                    break

            if not inserted:
                ordered.append(pnum)
        
        gold_answer = gold_answer + ordered[mid]

print(silver_answer)
print(gold_answer)
