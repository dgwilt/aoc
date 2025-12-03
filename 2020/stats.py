from math import inf

stats = """
      -------Part 1--------   -------Part 2--------
Day       Time  Rank  Score       Time  Rank  Score
 17   02:29:13  5165      0   02:32:18  4630      0
 16   01:19:59  6288      0   02:02:28  4309      0
 15   01:50:30  7480      0   02:02:55  6462      0
 14   00:51:03  4587      0   01:28:00  3681      0
 13   00:49:48  6723      0   01:39:16  2668      0
 12   00:37:39  4975      0   00:55:09  3589      0
 11   01:35:42  7078      0   01:43:31  5122      0
 10   00:08:42  1683      0   00:49:48  2675      0
  9   00:31:12  6983      0   00:35:37  4957      0
  8   00:15:32  4158      0   00:33:10  3556      0
  7   00:15:08   575      0   01:32:09  5166      0
  6   00:04:19   702      0   00:06:56   424      0
  5   00:09:39  1146      0   00:12:22   825      0
  4   00:20:40  4150      0   00:34:36  1733      0
  3   00:04:52   642      0   00:08:42   653      0
  2   00:37:08  6422      0   00:41:01  5639      0
  1   00:45:18  5223      0   00:46:36  4684      0
"""

types = [int,str,int,int,str,int,int]
data = {}
for line in stats.splitlines():
    try: items = [t(v) for t,v in zip(types,line.split())]
    except ValueError: continue
    if len(items) == 7:
        day,t1,r1,s1,t2,r2,s2 = items
    elif len(items) == 4:
        day,t1,r1,s1 = items
        t2,r2,s2 = "",None,None
    else:
        continue
    times = []
    for time in (t1,t2):
        if time:
            hours, minutes, seconds = [int(i) for i in time.split(":")]
            time_in_seconds = hours * 60 * 60 + minutes * 60 + seconds
            times.append(time_in_seconds)
    data[day] = {'times':times, 'ranks': [r1,r2], 'scores':[s1,s2]}

results = {}
results["Number of days with any star"] = len(data)
results["Number of days with gold stars"] = sum([len(data[day]['times']) == 2 for day in data.keys()])

consecutive = 1
most_consecutive = 1
last = 0
for day in range(1,max(data.keys())):
    if day in data:
        if day == last+1:
            consecutive += 1
        else:
            consecutive = 1
        if consecutive > most_consecutive:
            most_consecutive = consecutive
        last = day
results["Number of consecutive days with any star"] = most_consecutive

# Number of consecutive days with a gold star
consecutive = 1
most_consecutive = 1
last = 0
for day in range(1,max(data.keys())):
    if day in data and len(data[day]['times']) == 2:
        if day == last+1:
            consecutive += 1
        else:
            consecutive = 1
        if consecutive > most_consecutive:
            most_consecutive = consecutive
        last = day
results["Number of consecutive days with a gold star"] = most_consecutive

# Best day-to-day silver rank improvement (&day)
best_silver_rank_improvement = inf
best_silver_rank_improvement_day = None
for day in range(1,max(data.keys())):
    if day in data and day-1 in data:
        silver_rank_improvement = data[day]['ranks'][0] - data[day-1]['ranks'][0]
        if silver_rank_improvement < best_silver_rank_improvement:
            best_silver_rank_improvement = silver_rank_improvement
            best_silver_rank_improvement_day = day
results["Best day-to-day silver rank improvement"] = (-best_silver_rank_improvement,best_silver_rank_improvement_day)

# Best day-to-day gold rank improvement (&day)
best_gold_rank_improvement = inf
best_gold_rank_improvement_day = None
for day in range(1,max(data.keys())):
    if day in data and day-1 in data and len(data[day]['times']) == 2 and len(data[day-1]['times']) == 2:
        gold_rank_improvement = data[day]['ranks'][1] - data[day-1]['ranks'][1]
        if gold_rank_improvement < best_gold_rank_improvement:
            best_gold_rank_improvement = gold_rank_improvement
            best_gold_rank_improvement_day = day
results["Best day-to-day gold rank improvement"] = (-best_gold_rank_improvement,best_gold_rank_improvement_day)

# Best silver rank (&day)
best_silver = inf
best_silver_day = None
for day in data:
    silver_rank = data[day]['ranks'][0]
    if silver_rank < best_silver:
        best_silver = silver_rank
        best_silver_day = day
results["Best silver rank"] = (best_silver,best_silver_day)

# Average silver rank 
silver_ranks = []
for day in data:
    silver_ranks.append(data[day]['ranks'][0])
results["Average silver rank"] = sum(silver_ranks)//len(silver_ranks)

# Best gold rank (&day)
best_gold = inf
best_gold_day = None
for day in data:
    if len(data[day]['ranks']) < 2: continue
    gold_rank = data[day]['ranks'][1]
    if gold_rank < best_gold:
        best_gold = gold_rank
        best_gold_day = day
results["Best gold rank"] = (best_gold,best_gold_day)

# Average gold rank 
gold_ranks = []
for day in data:
    if len(data[day]['ranks']) < 2: continue
    gold_ranks.append(data[day]['ranks'][1])
results["Average gold rank"] = sum(gold_ranks)//len(gold_ranks)

# Best rank improvement in a day silver -> gold (&day)
best_improvement = -inf
best_improvement_day = None
rank_improvements = []
for day in data:
    if len(data[day]['ranks']) < 2: continue
    improvement = data[day]['ranks'][0] - data[day]['ranks'][1]
    rank_improvements.append(improvement)
    if improvement > best_improvement:
        best_improvement = improvement
        best_improvement_day = day
results["Best rank improvement in a day"] = (best_improvement,best_improvement_day)
results["Average rank improvement in a day"] = sum(rank_improvements)//len(rank_improvements)

# Best rank improvement in a day silver -> gold (&day)
best_improvement = -inf
best_improvement_day = None
for day in data:
    if len(data[day]['ranks']) < 2: continue
    improvement = 100*(data[day]['ranks'][0] - data[day]['ranks'][1])//data[day]['ranks'][0]
    if improvement > best_improvement:
        best_improvement = improvement
        best_improvement_day = day
results["Best % rank improvement in a day"] = (best_improvement,best_improvement_day)

# Shortest time silver -> gold (&day)
shortest_gold_time = inf
shortest_gold_time_day = None
for day in data:
    if len(data[day]['times']) < 2: continue
    gold_time = data[day]['times'][1] - data[day]['times'][0]
    if gold_time < shortest_gold_time:
        shortest_gold_time = gold_time
        shortest_gold_time_day = day
results["Shortest time silver -> gold"] = (shortest_gold_time,shortest_gold_time_day)

# Average time silver -> gold
total_gold_time = 0
gold_days = 0
for day in data:
    if len(data[day]['times']) < 2: continue
    gold_time = data[day]['times'][1] - data[day]['times'][0]
    gold_days += 1
    total_gold_time += gold_time
results["Average time silver -> gold"] = total_gold_time//gold_days

# Number of global scores
global_scores = 0
global_total = 0
for stat in data.values():
    global_scores += len([s for s in stat['scores'] if s > 0])
    global_total += sum(stat['scores'])
results["Number of global scores"] = global_scores

# Total global score
results["Total global score"] = global_total

width = max([len(k) for k in results.keys()])

for stat,value in results.items():
    print(f"{stat:>{width}s} : {value}")
