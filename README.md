ENEL453-Assembler
=================

An assembler for a simple processor designed in ENEL453.  This supports comments, removal of white space, and writes out both hex and binary files.

## Usage
```
  usage: assembly.py [-h] [-v] [-i] [-b] [filename [filename ...]]
```
## Instruction Set
```
  load  [Constant]      [Reg0, Reg1]      {load constant to register}
  move  [Reg0, Reg1]                      {To Accum}
  add   [Reg0, Reg1]                      {To Accum}
  sub   [Reg0, Reg1]                      {From Accum}
  sl                                      {Shift accum left}
  sr                                      {Shift accum right}
  and   [Reg0, Reg1]                      {With Accum}
  or    [Reg0, Reg1]                      {With Accum}
  inv                                     {Invert Accum}
  j     [Address]                         {Jump to address}
  jaz   [Address]                         {Jump to address if accum zero}
  jal   [Address]                         {Jump and link (sub routine)}
  jr                                      {Jump return (From sub routine)}
  wri   [Reg0, Reg1, P1, P2, Tx]          {Write accum to register}
  str   [Reg0, Reg1]                      {Store Rx from UART into register}
```

## Examples:
```
  load 25 Reg0 #Comment, Comment, Comment
  load 1 Reg1
  move Reg0
  add Reg1
  sub Reg0
  wri P1      # p+++++++
```

## List of Register:
  Reg0:   General Purpose Register

  Reg1:   General Purpose Register

  P1:     Register reading into first digit of seven segment display

  P2:     Register reading into second digit of seven segment display

  Tx:     UART transmit register

  Rx:     UART receive register

