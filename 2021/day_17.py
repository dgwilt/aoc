#!/usr/bin/env python3 
from itertools import product
from sys import argv
from aoc import AocDay
from re import search
import turtle

class AocDay17(AocDay):

    VISUALISE = False

    def visualise():
        vx,vy,x1,x2,y1,y2 = AocDay17.START
        sign = lambda a: (a>0) - (a<0)
        x, y, hit, overshot = 0, 0, False, False

        probe = turtle.Turtle()
        probe.penup()
        probe.hideturtle()
        probe.setposition(-300,-300)
        probe.shape('circle')
        probe.showturtle()
        probe.pendown()

        while not (hit or overshot):
            x += vx
            y += vy
            vx -= sign(vx)
            vy -= 1
            overshot = x > x2 or y < y1
            hit = not overshot and x >= x1 and y <= y2
            probe.setposition((3*x)-300,(y//40)-300)

        turtle.done()

    def probe_sim(data):
        x1,x2,y1,y2 = [int(i) for i in search(r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)',data).groups()]
        heights = []
        sign = lambda a: (a>0) - (a<0)
        for vx,vy in product(range(1,150),range(-200,200)): # Ranges tweaked by hand for runtime
            x, y, ymax, hit, overshot, v0 = 0, 0, 0, False, False, (vx,vy)
            while not (hit or overshot):
                x += vx
                y += vy
                vx -= sign(vx)
                vy -= 1
                if y > ymax: ymax = y
                overshot = x > x2 or y < y1
                hit = not overshot and x >= x1 and y <= y2
                if hit: heights.append(ymax)
                if AocDay17.VISUALISE and hit and ymax == max(heights): AocDay17.START = (*v0,x1,x2,y1,y2) # For visualization
        return heights 

    def run_silver(self,data):
        result = max(AocDay17.probe_sim(data))
        if AocDay17.VISUALISE: AocDay17.visualise()
        return result

    def run_gold(self,data):
        return len(AocDay17.probe_sim(data))

if __name__ == "__main__":

    data = "target area: x=57..116, y=-198..-148"

    silver_tests = ["target area: x=20..30, y=-10..-5"]

    gold_tests = ["""""",""""""]

    answer = AocDay17(data,silver_tests,gold_tests,argv)

    print(answer)