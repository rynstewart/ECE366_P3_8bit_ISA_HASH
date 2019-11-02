# Hash function on 8-bit ISA

This is a special instruction set developed for our Computer Organization class. The instructions and registers are only 8 bits long. They're are 4 addressable registers (0, 1, 2, 3), and 12 instructions currently supported.

Supported Instructions:

Instruction format: 4 bits OP code, 2 bits rd, 2 bits rs

example: `0000 dd ss`

## Hash Instruction Ideas
Note: branch type needs decision and may need increment

|Instruction Name |OP code |Description            |
|-----------------|--------|-----------------------|
|initui           |        |Intialize upper 4 bits of a register|
|initl            |        |Intialize lower 4 bits of a register|
|Fold             |1101    |Unsigned mult of an A and B into a C, then xor the hi and lo|
|xor              |1001    |
|sinc2b           |0101    |Stores two bits into mem and then increments address by two|
|s8b              |        |
|l8b              |0100    |
|andi             |        |
|srl              |        |
|addiu            |        |
|branch(+)        |        |special branch that increments a specific branch register|


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
