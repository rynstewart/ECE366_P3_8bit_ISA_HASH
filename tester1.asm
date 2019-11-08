# $8: B value
# $9: loop 100 count
# $10: A
# $11: addr
# $12: n count for collision
# $13: C
# $14: count 11111
# %15: 2
# $16: store largest c addr
# $17: store largest c value
# $18: compare c values/used as addr to store of largest c addr & value
# $19: temp, FFFF
# $20: temp, for folding
# $21: temp, loop 4 count
# $22: temp1
# $23: temp2

addi $8, $0 0xFA
addi $9, $0, 255
addi $10, $0, 1
ori $11, $0, 0x2020
ori $19, $0, 0xF0
addi $21, $0, 0
addi $15, $0, 2

loop_100:
addi $21, $0, 4

hash_1st:
multu $10, $8
mflo $22
and $23, $22, $19#$23 = A[15:0]
srl $23, $23, 4
andi $22, $22, 0xF#$22 = A[31:16]
xor $22, $22, $23
hash_4:
multu $22, $8
mflo $22
and $23, $22, $19#$23 = A[15:0]
srl $23, $23, 4
andi $22, $22, 0xF#$22 = A[31:16]
xor $22, $22, $23 #$22 = A
addi $21, $21, -1 #count--
bne $21, $0, hash_4
j lastSet

lastSet:
and $23, $22, $19#$23 = A[15:0]
srl $23, $23, 4
andi $22, $22, 0xF#$22 = A[31:16]
xor $13, $22, $23
andi $23, $13, 0xC #$23 = C[7:0]
srl $23, $23, 4
andi $22, $13, 0x3 #$22 = C[15:8]
xor $13, $22, $23 #$13: C

sw $13, 0($11)
addi $11, $11, 4
addi $10, $10, 1
addi $9, $9, -1

next:
bne $9, $0, loop_100

#reset registers for checking match

addi $9, $0, 1024#memory limit
addi $13, $0, 0#count0
addi $10, $0, 0#count1
addi $11, $0, 0#count2
addi $12, $0, 0#count3
addi $21, $0, 0#addr 
addi $17, $0, 0x0 #0x00011111
addi $18, $0, 0x1 #0x00111110
addi $19, $0, 0x2 #0x01111100
addi $20, $0, 0x3 #0x11111000

start:
lw $23, 0x2004($21)
beq $23, $17, count0

beq $23, $18, count1

beq $23, $19, count2

beq $23, $20, count3

count0:
addi $21, $21, 4
addi $13, $13, 1
bne $21, $9, start
j write #make sure move on

count1:
addi $21, $21, 4
addi $10, $10, 1
bne $21, $9, start
j write #make sure move on

count2:
addi $21, $21, 4
addi $11, $11, 1
bne $21, $9, start
j write #make sure move on

count3:
addi $21, $21, 4
addi $12, $12, 1
bne $21, $9, start
j write #make sure move on

write:#endl
sw $13, 0x2000($0)
sw $10, 0x2004($0)
sw $11, 0x2008($0)
sw $12, 0x200C($0)

