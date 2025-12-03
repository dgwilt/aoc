#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay

class AocDay24(AocDay):

    # Solution courtesy of https://www.reddit.com/user/i_have_no_biscuits/

    def f(a,b,c, z, w):
        z2 = z // a
        if (z % 26 + b) != w:
            z2 = z2 * 26 + w + c
        return z2

    def run_monad(data,fn):
        data = [line.split() for line in data.splitlines()]
        params = []
        for i in range(0, 18*14, 18):
            a = int(data[i+4][-1])
            b = int(data[i+5][-1])
            c = int(data[i+15][-1])
            params.append((a, b, c))

        zs = {0: 0}
        for a,b,c in params:
            next_zs = {}
            for z, inp in zs.items():
                for w in range(1,10):
                    new_z = AocDay24.f(a,b,c,z,w)
                    if a == 1 or (a == 26 and new_z < z):
                        new_inp = 10 * inp + w
                        next_zs[new_z] = fn(next_zs.get(new_z,new_inp), new_inp)
        
            zs = next_zs
        return zs[0]

    def run_silver(self,data):
        return AocDay24.run_monad(data,max)
        
    def run_gold(self,data):
        return AocDay24.run_monad(data,min)

if __name__ == "__main__":

    silver_tests = ["""""",""""""]

    gold_tests = ["""""",""""""]

    data = """inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 11
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 5
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 0
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -6
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -6
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -6
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -16
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -4
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -2
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y"""

    answer = AocDay24(data,silver_tests,gold_tests,argv)

    print(answer)
