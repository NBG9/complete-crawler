# Find Valptr, Mincode, Maxcode and Huffval from JpegSnoop (DHT) Huffman tables

# Huffman table sample
t = """Codes of length 01 bits (000 total): 
    Codes of length 02 bits (002 total): 01 00 
    Codes of length 03 bits (002 total): 02 11 
    Codes of length 04 bits (001 total): 03 
    Codes of length 05 bits (002 total): 04 21 
    Codes of length 06 bits (003 total): 12 31 41 
    Codes of length 07 bits (005 total): 05 51 13 61 22 
    Codes of length 08 bits (005 total): 06 71 81 91 32 
    Codes of length 09 bits (004 total): A1 B1 F0 14 
    Codes of length 10 bits (005 total): C1 D1 E1 23 42 
    Codes of length 11 bits (006 total): 15 52 62 72 F1 33 
    Codes of length 12 bits (004 total): 24 34 43 82 
    Codes of length 13 bits (008 total): 16 92 53 25 A2 63 B2 C2 
    Codes of length 14 bits (003 total): 07 73 D2 
    Codes of length 15 bits (003 total): 35 E2 44 
    Codes of length 16 bits (109 total): 83 17 54 93 08 09 0A 18 19 26 36 45 1A 27 64 74 55 37 F2 A3 B3 C3 28 29 D3 E3 F3 84 94 A4 B4 C4 D4 E4 F4 65 75 85 95 A5 B5 C5 D5 E5 F5 46 56 66 76 86 96 A6 B6 C6 D6 E6 F6 47 57 67 77 87 97 A7 B7 C7 D7 E7 F7 38 48 58 68 78 88 98 A8 B8 C8 D8 E8 F8 39 49 59 69 79 89 99 A9 B9 C9 D9 E9 F9 2A 3A 4A 5A 6A 7A 8A 9A AA BA CA DA EA FA"""

# Split lines
lines = t.split("Codes of length")

# Matrix of separate values
lines2d = []

for line in lines[1::]:
    ar = []
    if line.strip()[line.find(":")::] == '':
        ar.append('')
    else:
        list = (line[line.find(": ") + 2::].strip()).split(" ")
        for val in list:
            ar.append(int(val, 16))
    lines2d.append(ar)

# Initialize three arrays
minval = [0]*16
maxval = [-1]*16
valptr = [0] * 16

# Initialize counter (valptr)
ctr = 0

# find valptrs
for i, line in enumerate(lines[1::]):
    num = line[line.find("(") + 1:line.find(" tot")]
    if len(num) == 0 or num == '000':
        continue
    valptr[i] = ctr
    ctr += int(num)

# Initialize counter (Min/Max val)
p = 0

# find Min/Max vals
for i, line in enumerate(lines2d):
    if len(line)==1 and line[0]=='' and i != 0:
        p = p - 1
        p = p+1
        p = p*2
        continue
    if len(line)==1 and line[0]=='' and i == 0:
        continue
    minval[i]=p
    p=p+len(line)-1
    maxval[i]=p
    p=2*(p+1)

# Find HuffVals of table
huffvals = []
for val in lines2d:
    for val2 in val:
        if  val2 != '':
            huffvals.append(val2)
        # else:
        #     huffvals.append(0)

# Print output
print("valptr: " + str(valptr))
print("min: " + str(minval))
print("max: " + str(maxval))
print("Huffval: " + str(huffvals))

# Sample output:

# valptr:
# [0, 0, 1, 6, 7, 8, 9, 10, 11, 0, 0, 0, 0, 0, 0, 0]
# min:
# [0, 0, 2, 14, 30, 62, 126, 254, 510, 0, 0, 0, 0, 0, 0, 0]
# max:
# [-1, 0, 6, 14, 30, 62, 126, 254, 510, -1, -1, -1, -1, -1, -1, -1]
# Huffval:
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


