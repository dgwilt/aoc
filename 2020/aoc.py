from sys import stderr
from sys import version
from collections import defaultdict
from re import compile

# Yuck! My work laptop is 3.7 and my home laptop is 3.8
if version.startswith("3.8"):
    # Python 3.8
    import math
    def prod(nums):
        return math.prod(nums)
else:
    # Pre-Python 3.8
    def prod(nums):
        from functools import reduce
        from operator import mul
        return reduce(mul,nums)

def chinese_remainder(n, a):
    sum = 0
    pn = prod(n)
    for n_i, a_i in zip(n, a):
        p = pn // n_i
        sum += a_i * modinv(p, n_i) * p
    return sum % pn

def egcd(a, b):
    if a == 0:
        return (0, 1)
    y, x = egcd(b % a, a)
    return (x - (b // a) * y, y)

def modinv(a, m):
    x, _ = egcd(a, m)
    return x % m

class V2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __lshift__(self,deg):
        deg %= 360
        if deg == 90:
            return V2(-self.y,self.x)
        elif deg == 180:
            return V2(-self.x,-self.y)
        elif deg == 270:
            return V2(self.y,-self.x)
        elif deg == 0:
            return self
        else:
            raise NotImplementedError
        
    def __rshift__(self,deg):
        deg %= 360
        if deg == 270:
            return V2(-self.y,self.x)
        elif deg == 180:
            return V2(-self.x,-self.y)
        elif deg == 90:
            return V2(self.y,-self.x)
        elif deg == 0:
            return self
        else:
            raise NotImplementedError

    def __sub__(self,o):
        return V2(self.x-o.x,self.y-o.y)

    def __isub__(self,o):
        self.x -= o.x
        self.y -= o.y
        return self

    def __add__(self,o):
        return V2(self.x+o.x,self.y+o.y)

    def __iadd__(self,o):
        self.x += o.x
        self.y += o.y
        return self

    def __mul__(self,n):
        return V2(n*self.x,n*self.y)

    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def __repr__(self):
        return f"({self.x},{self.y})" 

    def __str__(self):
        return self.__repr__()

class AocDay:

    SILVER = 'silver'
    GOLD = 'gold'
    NOSOL = ""
    MODES = ('st','s','gt','g','gst')

    def __init__(self,data,silver_tests,gold_tests,argv):
        if not data: data = ""
        if not silver_tests: silver_tests = []
        if not gold_tests: gold_tests = []
        if len(argv) < 2: mode = None
        else: mode = argv[1]

        self.data = data
        self.tests = {AocDay.SILVER : silver_tests, AocDay.GOLD : gold_tests}
        if mode in AocDay.MODES:
            self.mode = mode
        else:
            self.mode = AocDay.MODES[0]
            print(f"No mode given, using {self.mode} by default",file=stderr)
        
        # Useful stuff to have
        self.udlr = {'U':(0,-1),'D':(0,1),'L':(-1,0),'R':(1,0)}
        self.nswe = {'N':(0,-1),'S':(0,1),'W':(-1,0),'E':(1,0)}
        self.grid = defaultdict(int)
        self.pos = (0,0)
        self.parser_cfg = {}

    def move(self,dir):
        if dir in self.udlr: delta = self.udlr[dir]
        elif dir in self.nswe: delta = self.nswe[dir]
        else: delta = (0,0)
        self.pos = tuple(self.pos[i] + delta[i] for i in range(2))

    def parser_setup(self,types,pat):
        self.parser_cfg['types'] = types
        self.parser_cfg['pat']   = compile(pat)

    def parser(self,data):
        pat = self.parser_cfg['pat']
        types = self.parser_cfg['types']
        fields = list(range(1,len(types)+1))
        for line in data.splitlines():
            yield (t(item) for t,item in zip(types,pat.search(line).group(*fields)))

    def run_silver(self,data):
        raise NotImplementedError

    def run_gold(self,data):
        raise NotImplementedError

    def as_lines(self,data):
        return data.splitlines()

    def as_nums(self,data):
        return [int(i) for i in data.splitlines()]

    def __repr__(self):
        if self.mode == AocDay.MODES[0]:
            result = "\n".join(str(self.run_silver(t)) for t in self.tests[AocDay.SILVER] if t)
        elif self.mode == AocDay.MODES[1]:
            result = str(self.run_silver(self.data))
        elif self.mode == AocDay.MODES[2]:
            result = "\n".join(str(self.run_gold(t)) for t in self.tests[AocDay.GOLD] if t)
        elif self.mode == AocDay.MODES[3]:
            result = str(self.run_gold(self.data))
        elif self.mode == AocDay.MODES[4]:
            # Run gold with silver tests
            result = "\n".join(str(self.run_gold(t)) for t in self.tests[AocDay.SILVER] if t)
        else:
            # Should be impossible!
            raise ValueError
        return result
