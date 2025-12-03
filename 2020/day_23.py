#!/usr/bin/env python3 
from sys import argv
from aoc import AocDay

class Node:

    def __init__(self,v):
        self.v = v
        self.next = None

class CircularList:

    def __init__(self,nums):
        self.nodes = {}
        prev = None
        for n in nums:
            node = Node(n)
            if prev:
                prev.next = node
            self.nodes[n] = node
            prev = node
        first = self.nodes[nums[0]]
        last = self.nodes[nums[-1]]
        last.next = first
        self.highest = max(nums)

    def take_three_after(self,val):
        cur = self.nodes[val]
        start = cur.next
        end = start.next.next
        cur.next = end.next
        return start, end

    def insert_after(self,val,start,end):
        pre = self.nodes[val]
        post = pre.next
        pre.next = start
        end.next = post

class AocDay23(AocDay):

    def destination(self,start,dst,cups):
        takenums = [start.v,start.next.v,start.next.next.v]
        while (dst := cups.highest if dst == 1 else dst - 1) in takenums:
            pass
        return dst

    def play_cups(self,moves,cupnums):
        label = cupnums[0]
        cups = CircularList(cupnums)
        for _ in range(moves):
            start,end = cups.take_three_after(label)
            destination = self.destination(start,label,cups)
            cups.insert_after(destination,start,end)
            label = cups.nodes[label].next.v
        return cups.nodes[1].next

    def to_str(self,node,n):
        result = ""
        for _ in range(n):
            result += str(node.v)
            node = node.next
        return result

    def run_silver(self,data):
        cupnums = [int(c) for c in data]
        after_one = self.play_cups(100,cupnums)
        return self.to_str(after_one,len(cupnums)-1)
        
    def run_gold(self,data):
        cupnums = [int(i) for i in data] + [i for i in range(len(data)+1,1000001)]
        after_one = self.play_cups(10000000,cupnums)
        return after_one.v * after_one.next.v

if __name__ == "__main__":

    silver_tests = ["389125467"]

    gold_tests = ["""""",""""""]

    data = "219347865"

    answer = AocDay23(data,silver_tests,gold_tests,argv)

    print(answer)
