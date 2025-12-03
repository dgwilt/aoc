def run(data):
    r0,r1,r3,r4,r5 = [0]*5
    seen = set()
    while True:
        r4 = r3 | 0x10000
        r3 = 7041048
        while True:
            r3 += r4 & 0xFF
            r3 &= 0xFFFFFF
            r3 *= 65899
            r3 &= 0xFFFFFF
            if r4 < 0x100:
                if r3 in seen:
                    return lastseen
                seen.add(r3)
                lastseen = r3
                break
            r4 //= 0x100

print(run(""))