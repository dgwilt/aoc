data = """Time:      7  15   30
Distance:  9  40  200"""

lines = data.splitlines()
times = [int(i) for i in lines[0].split()[1:]]
distances = [int(i) for i in lines[1].split()[1:]]
ways = []
for i in range(len(times)):
    time = times[i]
    distance = distances[i]

    better = 0
    for button in range(1,time):
        if button * (time-button) > distance:
            better = better + 1
    ways.append(better)

result = 1
for way in ways:
    result = result * way

print(result)
