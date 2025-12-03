#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay, prod
from functools import lru_cache

class AocDay10(AocDay):

    def diffs(self,data):
        nums = [0] + sorted([int(i) for i in data.splitlines()])
        return [nums[i] - nums[i-1] for i in range(1,len(nums))] + [3]

    def run_silver(self,data):
        diffs = self.diffs(data)
        return diffs.count(1) * diffs.count(3)

    def run_gold_dp(self,data):
        paths_to = {0:1} 
        for n in sorted([int(i) for i in data.splitlines()]):
            paths_to[n] = sum(paths_to.get(i,0) for i in range(n-3,n))
        return max(paths_to.values())
        
    def run_gold_str(self,data):
        diffs = "".join(str(d) for d in self.diffs(data))
        diffs = diffs.replace("1111","7").replace("111","4").replace("11","2").replace("3","")
        return prod([int(d) for d in diffs])

    def run_gold(self,data):
        return self.run_gold_dp(data)
        #return self.run_gold_str(data)

if __name__ == "__main__":

    data = """138
3
108
64
92
112
44
53
27
20
23
77
119
62
121
11
2
37
148
34
83
24
10
79
96
98
127
7
115
19
16
78
133
61
82
91
145
39
33
13
97
55
141
1
134
40
71
54
103
101
26
47
90
72
126
124
110
131
58
12
142
105
63
75
50
95
69
25
68
144
86
132
89
128
135
65
125
76
116
32
18
6
38
109
111
30
70
143
104
102
120
31
41
17"""

    silver_tests = ["""16
10
15
5
1
11
7
19
6
12
4""","""28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""]

    gold_tests = ["""""",""""""]

    answer = AocDay10(data,silver_tests,gold_tests,argv)

    print(answer)
