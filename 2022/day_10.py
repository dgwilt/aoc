#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay
import turtle

class AocDay10(AocDay):

    VISUALIZE = False

    def turtle_setup(self):
        turtle.Screen().screensize(900, 300)
        self.pen = turtle.Turtle()
        self.pen.speed("slow")
        self.pen.shape("square")
        self.pen.hideturtle()
        self.pen.penup()

    def visualize(self,result,row,x):
        self.pen.setposition(-400 + x*20,60-row*20)
        self.pen.showturtle()
        if result[-1] != " ":
            self.pen.stamp()
        self.pen.hideturtle()

    def make_dataseries(self,data):
        X = 1
        dataseries = [X]
        for line in data.splitlines():
            fields = line.split()
            if fields[0] == "noop":
                dataseries.append(X)
            elif fields[0] == "addx":
                dataseries.append(X)
                X += int(fields[1])
                dataseries.append(X)
        return dataseries

    def run_silver(self,data):
        dataseries = self.make_dataseries(data)
        return sum(t*dataseries[t-1] for t in range(20,221,40))

    def run_gold(self,data):
        if AocDay10.VISUALIZE: self.turtle_setup()
        dataseries = self.make_dataseries(data)
        result = "\n"
        for row in range(6):
            for x in range(40):
                sprite = dataseries[40*row + x]
                result += "█" if sprite-2 < x < sprite+2 else " "
                if AocDay10.VISUALIZE: self.visualize(result,row,x)
            result += "\n"
        if AocDay10.VISUALIZE: turtle.done()
        return result

if __name__ == "__main__":

    silver_tests = ["""addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""",""""""]

    gold_tests = ["""""",""""""]

    data = """noop
noop
noop
addx 6
addx -1
addx 5
noop
noop
noop
addx 5
addx 11
addx -10
addx 4
noop
addx 5
noop
noop
noop
addx 1
noop
addx 4
addx 5
noop
noop
noop
addx -35
addx -2
addx 5
addx 2
addx 3
addx -2
addx 2
addx 5
addx 2
addx 3
addx -2
addx 2
addx 5
addx 2
addx 3
addx -28
addx 28
addx 5
addx 2
addx -9
addx 10
addx -38
noop
addx 3
addx 2
addx 7
noop
noop
addx -9
addx 10
addx 4
addx 2
addx 3
noop
noop
addx -2
addx 7
noop
noop
noop
addx 3
addx 5
addx 2
noop
noop
noop
addx -35
noop
noop
noop
addx 5
addx 2
noop
addx 3
noop
noop
noop
addx 5
addx 3
addx -2
addx 2
addx 5
addx 2
addx -25
noop
addx 30
noop
addx 1
noop
addx 2
noop
addx 3
addx -38
noop
addx 7
addx -2
addx 5
addx 2
addx -8
addx 13
addx -2
noop
addx 3
addx 2
addx 5
addx 2
addx -15
noop
addx 20
addx 3
noop
addx 2
addx -4
addx 5
addx -38
addx 8
noop
noop
noop
noop
noop
noop
addx 2
addx 17
addx -10
addx 3
noop
addx 2
addx 1
addx -16
addx 19
addx 2
noop
addx 2
addx 5
addx 2
noop
noop
noop
noop
noop
noop"""

    answer = AocDay10(data,silver_tests,gold_tests,argv)

    print(answer)
