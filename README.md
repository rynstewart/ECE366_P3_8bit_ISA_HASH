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
initlo & inithi only work with setting $1. OP codes 0001
and 1001  aren't usable because of this. 

|Instruction Name |OP code |Description            |
|-----------------|--------|-----------------------|
|initlo           |00      |Intialize lower 4 bits of register 1|
|inithi           |10      |Intialize upper 4 bits of a register 1|
|LA               |0000    |Loads special register A ($6) into specified register since register A is not addressable|
|xor              |0010    ||
|sinc2b           |0011    |Stores two bits into mem and then increments address by two|
|pat_Count        |0101    |Counts the number of times 00, 01, 10, 11 appear|
|addu             |0110    ||
|and1             |1000    ||
|srl              |1010    |All bits in $3 will be shifted to lower bits |
|Hash_branch      |1110    |special branch that increments a specific branch register, in this case it's A = [1:255]|
|Fold             |1101    |Unsigned mult of an A and B into a C, then xor the hi and lo. Always performs with $6. |


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
