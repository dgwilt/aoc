def run(data):
    # Once you go through the code in detail, it's the sum of 
    # the factors of r3, which gets made much bigger when r0 is set to 1

    r3 = (2 * 2 * 19 * 11) + (4 * 22) + 6 

    if data == 1:
        r3 += ((27 * 28) + 29) * 30 * 14 * 32

    return sum(i + r3//i for i in range(1,int(r3**0.5)+1) if r3 % i == 0)

print(run(0))
print(run(1))
