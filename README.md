# Hash function on 8-bit ISA

This is a special instruction set developed for our Computer Organization class. The instructions and registers are only 8 bits long. They're are 4 addressable registers (0, 1, 2, 3), and 12 instructions currently supported.

Supported Instructions:

Instruction format: 4 bits OP code, 2 bits rd, 2 bits rs

example: `0000 dd ss`

mc1 for testing purposes(2 lines):
01011111
00011010

## Hash Instruction Ideas
Note: branch type needs decision and may need increment
M: might not need
N: need work on
l8: need to show memory and add memory content

|Instruction Name |OP code |Description            |
|-----------------|--------|-----------------------|
|initlo           |0000    |Intialize lower 4 bits of a register $6(unaddresable)|
|initui           |0001    |Intialize upper 4 bits of a register $6(unaddresable)|
|                 |0010    ||
|sinc2b  N        |0011    |Stores two bits into mem and then increments address by two|
|l8               |0100    ||
|s8               |0101    |Just store 8 bits|
|addu             |0110    ||
|addiu            |0111    ||
|and     M        |1000    ||
|xor              |1001    ||
|andi             |1010    ||
|bezR0            |1011    ||
|jmp              |1100    ||
|Fold             |1101    |Unsigned mult of an A and B into a C, then xor the hi and lo. Always performs with $6. |
|branch(+)        |1110    |special branch that increments a specific branch register, in this case it's A = [1:255]|
|                 |1111    ||


## Work Split

|Group Member     |function|
|-----------------|--------|
|Christina        |sub     |
|                 |addi    |
|                 |xor     |
|                 |slt     |
|Marah            |init    |
|                 |ld      |
|                 |st      |
|                 |add     |
|Ryn              |bezR0   |
|                 |jmp     |
|                 |halt    |

## Meeting Logs

|Date    |attended     |Discussed    |
|--------|-------------|-------------|
|10/23/19|Christina, Marah, and Ryn|Starting with example 8 bit ISA, and split up work between group members.|
|11/01/19|Christina and Ryn|Discussed and considered instructions ideas.|
