#!/usr/bin/env python3 
from os import system
from os.path import exists as file_exists

for day in range(1,26):
    file = f"day_{day:02d}.py"
    if file_exists(file):
        print(f"\nDay {day}:")
        system(f"{file} s")
        system(f"{file} g")
