data = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

maps = data.split("\n\n")
seeds = [int(i) for i in maps[0].split(": ")[1].split()]

transformer = {}
for m in maps[1:]:
  lines = m.splitlines()
  fr,to = lines[0].split()[0].split("-to-")
  transformer[fr] = {}
  transformer[fr]['data'] = []
  transformer[fr]['to'] = to
  for line in lines[1:]:
    transformer[fr]['data'].append([int(i) for i in line.split()])

def transform(n,mappings):
  for to,fr,size in mappings:
    if fr <= n < fr + size:
      return n - fr + to
  return n # Was not mapped

results = []
for s in seeds:
  typ = "seed"
  while typ in transformer:
    s = transform(s,transformer[typ]['data'])
    typ = transformer[typ]['to']
  results.append(s)

print(min(results))
