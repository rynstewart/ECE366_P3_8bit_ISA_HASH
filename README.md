# Hash function on 8-bit ISA

Supported Instructions:

Instruction format: 4 bits OP code, 2 bits rd, 2 bits rs

example: `0000 dd ss`

## Hash Instruction Ideas

|Instruction Name |OP code |
|-----------------|--------|
|mult             |1101    |
|xor              |1001    |
|l2b              |0100    |
|s2b              |0101    |

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
