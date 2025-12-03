#!/usr/bin/env python3 

data = """193651-649729"""

tests = ["""""",""""""]

def run(data):
    a,b = [int(i) for i in data.split("-")]
    ascending = lambda p : all(p[i] >= p[i-1] for i in range(1,6))
    anymatch = lambda p : any(p[i] == p[i-1] for i in range(1,6))
    numbers_as_strings = (str(x) for x in range(a,b+1))
    return len(list(filter(lambda p: ascending(p) and anymatch(p), numbers_as_strings)))

for test in [t for t in tests if t]:
    try: print(run(test))
    except Exception as e: 
        print(f"Error: {e}")
    
print(run(data))
