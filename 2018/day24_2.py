from re import search

data = """Immune System:
123 units each with 8524 hit points with an attack that does 612 slashing damage at initiative 11
148 units each with 4377 hit points (weak to slashing, bludgeoning) with an attack that does 263 cold damage at initiative 1
6488 units each with 2522 hit points (weak to fire) with an attack that does 3 bludgeoning damage at initiative 19
821 units each with 8034 hit points (immune to cold, bludgeoning) with an attack that does 92 cold damage at initiative 17
1163 units each with 4739 hit points (weak to cold) with an attack that does 40 bludgeoning damage at initiative 14
1141 units each with 4570 hit points (weak to fire, slashing) with an attack that does 32 radiation damage at initiative 18
108 units each with 2954 hit points with an attack that does 262 radiation damage at initiative 8
4752 units each with 6337 hit points (weak to bludgeoning, cold; immune to slashing) with an attack that does 13 cold damage at initiative 20
4489 units each with 9894 hit points (weak to slashing) with an attack that does 20 slashing damage at initiative 12
331 units each with 12535 hit points with an attack that does 300 slashing damage at initiative 15

Infection:
853 units each with 13840 hit points (weak to bludgeoning, cold) with an attack that does 26 fire damage at initiative 3
450 units each with 62973 hit points (weak to slashing) with an attack that does 220 fire damage at initiative 13
3777 units each with 35038 hit points (weak to cold) with an attack that does 18 radiation damage at initiative 7
96 units each with 43975 hit points (immune to bludgeoning; weak to cold, slashing) with an attack that does 862 radiation damage at initiative 16
1536 units each with 14280 hit points (weak to cold, fire; immune to bludgeoning) with an attack that does 18 slashing damage at initiative 2
3696 units each with 36133 hit points (weak to radiation; immune to cold, fire) with an attack that does 18 bludgeoning damage at initiative 10
3126 units each with 39578 hit points (weak to cold) with an attack that does 22 radiation damage at initiative 4
1128 units each with 13298 hit points (weak to bludgeoning, slashing) with an attack that does 23 fire damage at initiative 6
7539 units each with 6367 hit points (weak to fire; immune to radiation) with an attack that does 1 slashing damage at initiative 5
1886 units each with 45342 hit points (weak to fire, cold) with an attack that does 45 cold damage at initiative 9"""

tests = ["""Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
"""]

class Group:
    def __init__(self,nunits,hp,dtype,dlevel,initiative,name,army):
        self.name = name
        self.hp = hp        
        self.nunits = nunits
        self.initiative = initiative
        self.dtype = dtype
        self.immune = set()
        self.weak = set()
        self.dlevel = dlevel
        self.army = army

    def num_units(self):
        return self.nunits

    def get_army(self):
        return self.army

    def get_dlevel(self):
        return self.dlevel

    def get_dtype(self):
        return self.dtype

    def get_initiative(self):
        return self.initiative

    def add_immune(self,i):
        self.immune.add(i)

    def add_weak(self,i):
        self.weak.add(i)

    def assess_damage(self,other):
        if other.get_dtype() in self.immune:
            return 0
        elif other.get_dtype() in self.weak:
            return 2*other.get_dlevel()*other.num_units()
        else:
            return other.get_dlevel()*other.num_units()

    def get_name(self):
        return self.name

    def get_power(self):
        return self.nunits * self.dlevel

    def attacked_by(self,other):
        damage = self.assess_damage(other)
        destroyed = min(self.nunits,damage//self.hp)
        self.nunits = self.nunits - destroyed

    def __repr__(self):
        return f'{self.name} contains {self.nunits}'

class Army:
    def __init__(self,name):
        self.name = name
        self.groups = []

    def get_name(self):
        return self.name

    def add_group(self,g):
        self.groups.append(g)

    def num_groups(self):
        return len(self.groups)

    def bury_the_dead(self):
        self.groups = [g for g in self.groups if g.num_units() > 0]

    def num_units(self):
        return sum(g.num_units() for g in self.groups)

    def get_groups(self):
        return sorted(self.groups,reverse=True, key=lambda g:(g.get_power(),g.get_initiative()))

    def __repr__(self):
        return self.name + "\n" + "\n".join(str(g) for g in self.groups)

def build_armies(data,boost):
    armies = []
    for l in data.splitlines():
        if l.strip() == "":
            continue
        if l.startswith("Immune") or l.startswith("Infection"):
            anum = 0
            aname = l[:-1]
            armies.append(Army(aname))
        else:
            anum += 1
            m1 = search(r'(\d+) units each with (\d+) hit points \((.*?)\)? with an attack that does (\d+) (\w+) damage at initiative (\d+)',l)
            if m1:
                nunits,hp,wi,dlevel,dtype,initiative = m1.group(1,2,3,4,5,6)
            else:
                nunits,hp,dlevel,dtype,initiative = search(r'(\d+) units each with (\d+) hit points with an attack that does (\d+) (\w+) damage at initiative (\d+)',l).group(1,2,3,4,5)
                wi = ""
            nunits,hp,dlevel,initiative = [int(i) for i in [nunits,hp,dlevel,initiative]]

            if "Immune" in aname:
                dlevel += boost

            name = f'{aname} Group {anum}'
            g = Group(nunits,hp,dtype,dlevel,initiative,name,aname)
            for x in wi.split(";"):
                x = x.strip()
                if x.startswith("weak"):
                    for w in x.replace("weak to","").strip().split(","):
                        g.add_weak(w.strip())
                elif x.startswith("immune"):
                    for i in x.replace("immune to","").strip().split(","):
                        g.add_immune(i.strip())
            armies[-1].add_group(g)
    return armies


def battle(data,boost):
    allunits = 0
    armies = build_armies(data,boost)
    while all(a.num_groups()>0 for a in armies):
        allgroups = []
        for a in armies:
            allgroups.extend(a.get_groups())

        # Target selection phase
        targets = {}
        ignore = []
        for a in sorted(allgroups,key=lambda g:(g.get_power(),g.get_initiative()),reverse=True):
            dmax = None
            dgroup = None
            for d in [g for g in allgroups if g.get_army() != a.get_army() and g.get_name() not in ignore]:
                damage = d.assess_damage(a)
                if dmax is None or damage > dmax:
                    dmax = damage
                    dgroup = d
                elif damage == dmax and d.get_power() > dgroup.get_power():
                    dgroup = d
                elif damage == dmax and d.get_power() == dgroup.get_power() and d.get_initiative() > dgroup.get_initiative():
                    dgroup = d

            if dgroup and dmax > 0:
                ignore.append(dgroup.get_name())
                targets[a.get_name()] = dgroup.get_name()

        # Attack phase, groups by descending initiative
        for attacking_group in sorted(allgroups, key=lambda g:g.get_initiative(), reverse=True):
            attacking_name = attacking_group.get_name()
            if attacking_group.num_units() == 0 or attacking_name not in targets:
                continue
            defending_name = targets[attacking_name]
            defending_group = [g for g in allgroups if g.get_name() == defending_name][0]
            defending_group.attacked_by(attacking_group)

        for a in armies:
            a.bury_the_dead()

        lastunits = allunits
        allunits = sum(a.num_units() for a in armies)
        if lastunits == allunits:
            return False,0

    alive = [a for a in armies if a.num_groups() > 0]
    return "Immune" in alive[0].get_name(), alive[0].num_units()

def run(data):
    boost = 40
    while True:
        immune_win, num_alive = battle(data,boost)
        if immune_win:
            return num_alive
        boost += 1

for test in [t for t in tests if t]:
    try: print(battle(test,1570))
    except Exception as e: print("Error:",e)
    
print(run(data))
