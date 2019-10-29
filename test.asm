init $3, 0x8
init $2, 0x1
add $3, $3
ld $1, $2
add $1, $1
st $1, $2
#addi $2, 0x3
sltR0 $2, $3
bezR0 2
jmp 0xFFF6
halt

