data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

# => Set the total to its starting value
total = ____

for line in data.splitlines():
    minpos = len(line)
    maxpos = 0
    # => For 'Gold' star, add names of digits to this list ...
    for digit in ["1","2","3","4","5","6","7","8","9"]:
        pos = line.find(digit) # This looks for the digit in the line, starting from the left
        # => Complete the comparison to look for the smallest position
        if pos != -1 and pos < ____ :
            # => Store the digit as the first digit
            firstdigit = ____
            minpos = pos

        pos = line.rfind(digit) # This looks for the digit in the line, starting from the right
        # => Complete the comparison to look for the largest position
        if pos != -1 and pos > ____: 
            # => Store the digit as the last digit
            lastdigit = ____
            maxpos = pos

    # => For 'Gold' star, convert names of digits to numbers here ...

    # => Use concatenation to build the 2-digit number
    number = ____

    # => Convert the number to an integer and add it to the total
    total = total + ____(number)

print(total)
