10011111 #1 = F0
00011010 #1 = FA
#stuff for setting of loop
11010100 #fold a and b 1st
11010100 #fold a and b 2nd
11010100 #fold a and b 3rd
11010100 #fold a and b 4th
11010100 #fold a and b 5th

#down to 4 bits
11110101 #$1 = $1-$1 = 0
00011111 #$1 = 0F
01101000 #$2 = $2 + $0 (C)
10001001 #$2 = lower 4 bits of C
11110101 #$1 = $1-$1 = 0
00010100 #$1 = 4
10100001 #$3 = upper 4 bits
00101011 #C = $3 xor $2

#down to 2 bits
11110101 #$1 = $1-$1 = 0
00010011 #1 = 0011
11111010 #$2 = 0
01101000 #$2 = $2 + $0 (C)
10001001 #$2 = lower 2 bits of C
11110101 #$1 = $1-$1 = 0
00010010 #$1 = 2
10100001 #$3 = upper 2 bits
00101011 #C = $3 xor $2

#storing
00110000

#branching
11110101 #$1 = 0
11100000 #special branch (if A is != 255 then A++ and jump to line 0)



