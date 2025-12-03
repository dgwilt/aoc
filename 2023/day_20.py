#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay, prod, lcm

class Component:
    LOW,HIGH = False, True

    def __init__(self,name):
        self.name = name
        self.to = []
        self.fr = []
        self.outqueue = []
        self.pulses = {Component.LOW:0,Component.HIGH:0}

    def connect(self,other):
        self.to.append(other)
        other.fr.append(self)

    def recv(self,fr,pulse):
        self.pulses[pulse] += 1

    def process(self):
        if self.outqueue:
            for pulse in self.outqueue:
                for component in self.to:
                    component.recv(self.name,pulse)
            self.outqueue = []
            for component in self.to:
                component.process()

    def init(self):
        pass

class Button(Component):
    def __init__(self,to):
        super().__init__("Button")
        self.to = to
        self.pushes = 0

    def push(self,count=1):
        for _ in range(count):
            self.to.recv(self.name,Component.LOW)
            self.to.process()
        self.pushes += count
        return True

class Broadcast(Component):
    def __init__(self,name):
        super().__init__(name)

    def recv(self,fr,pulse):
        super().recv(fr,pulse)
        self.outqueue.append(pulse)
        
class Conjunction(Component):
    def __init__(self,name):
        super().__init__(name)

    def init(self):
        self.remember = {fr.name:Component.LOW for fr in self.fr}

    def recv(self,fr,pulse):
        super().recv(fr,pulse)
        self.remember[fr] = pulse
        self.outqueue.append(not all(self.remember.values()))
        
class FlipFlop(Component):
    def __init__(self,name):
        super().__init__(name)
        self.state = Component.LOW

    def recv(self,fr,pulse):
        super().recv(fr,pulse)
        if pulse == Component.LOW:
            self.state = not self.state
            self.outqueue.append(self.state)

class AocDay20(AocDay):

    def parser(self,data):
        circuit = {}
        connections = {}
        mapper = {"&":Conjunction,"%":FlipFlop}
        for line in data.splitlines():
            fr,to = line.split(" -> ")
            tos = to.split(", ")
            if fr[0] in "&%":
                comp,name = mapper[fr[0]],fr[1:]
            else:
                comp, name = Broadcast, fr
            circuit[name] = comp(name)
            connections[name] = tos

        # Any generic components to add?
        outputs = [to for c in circuit for to in connections[c] if to not in circuit]
        for name in outputs:
            circuit[name] = Component(name)
            connections[name] = []

        # Connect
        for fr in circuit:
            comp1 = circuit[fr]
            for to in connections[fr]:
                comp2 = circuit[to]
                comp1.connect(comp2)

        # Init
        for c in circuit:
            circuit[c].init()

        return circuit, Button(circuit['broadcaster'])
    
    def run_silver(self,data):
        circuit, button = self.parser(data)
        button.push(1000)
        return prod(sum(circuit[c].pulses[pulse] for c in circuit) for pulse in (Component.LOW,Component.HIGH))

    def run_gold(self,data):
        circuit, button = self.parser(data)

        OUTPUT = 'rx'
        low_cycle_length = {c:0 for c in [c.name for out in circuit[OUTPUT].fr for c in circuit[out.name].fr]}

        while button.push():
            for comp in [c for c,p in low_cycle_length.items() if p == 0 and circuit[c].pulses[Component.LOW] > 0]:
                low_cycle_length[comp] = button.pushes
                if all(low_cycle_length.values()):
                    return lcm(low_cycle_length.values())
    
if __name__ == "__main__":

    silver_tests = ["""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""","""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""]

    gold_tests = ["""""",""""""]

    data = """%ls -> gl
%rz -> vm, gl
broadcaster -> rz, fp, kv, fd
%ql -> bn
%bm -> hr, fj
%fp -> cc, gk
&lk -> nc
%xg -> gl, mz
%dg -> gk, mp
%zg -> ls, gl
%lg -> hr
%pt -> lg, hr
%sp -> mj
%ms -> gl, hx
%kj -> fl, gk
%bn -> rj, gk
%xc -> vq
%fl -> gk
%dh -> hr, nm
%jk -> gk, dg
%tf -> cb
%kd -> cm, nr
&hr -> hh, kv, xl, qq
%kv -> xr, hr
%hq -> ql
&fn -> nc
%vm -> gl, xn
%jh -> nr, kd
%mz -> dd
%tp -> hq
%cf -> nr
%gr -> jh
%jd -> hr, bm
%xr -> qq, hr
%cm -> nr, cf
&fh -> nc
%rb -> xl, hr
&nc -> rx
%mp -> gk, kj
&nr -> fd, gr, fn, cb, tf, xc, vq
&gl -> fh, xn, sp, mz, rz, mj, dd
%rj -> jk
&hh -> nc
%fd -> nr, df
&gk -> lk, tp, fp, ql, hq, rj
%fj -> pt, hr
%qq -> dh
%df -> nr, nv
%mj -> ms
%xn -> xg
%cc -> gk, tp
%nm -> rb, hr
%dd -> sp
%vq -> gr
%cb -> xc
%nv -> tf, nr
%xl -> jd
%hx -> gl, zg"""

    answer = AocDay20(data,silver_tests,gold_tests,argv)

    print(answer)
