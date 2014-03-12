'''
Opcode d(11:8)    Operand d(7:0)                        Operation
0                 8 bits representing a constant        Load constant to Reg0
1                 8 bits representing a constant        Load constant to Reg1
2                 d7 selects register Reg0 or Reg1      Load value of selected register to the ALU accumulator
3                 d7 selects register Reg0 or Reg1      Add value of selected register to ALU accumulator and store result in accumulator
4                 d7 selects register Reg0 or Reg1      Subtract value of selected register to ALU accumulator and store result in accumulator
5                 Not used                              Accumulator shift right
6                 Not used                              Accumulator shift left
7                 d7 selects register Reg0 or Reg1      AND accumulator with selected register and store result in accumulator
8                 d7 selects register Reg0 or Reg1      OR accumulator with selected register and store result in accumulator
9                 Not used                              Invert Accumulator bits
A                 8 bits represent address in
                  instruction memory                    Jump to address
B                 8 bits represent address in
                  instruction memory                    Jump to address if Accumulator is all zeros
C                 8 bits represent address in
                  instruction memory                    Jump subroutine (program counter value is stored for the subroutine return)
D                 Not used                              Return from subroutine (restore value of program counter)
E                 D(3:0) selects either Reg0 “000” or
                  Reg1 “001” or output port P1”010” or
                  output port P2 “011”or UART transmit
                  register “100”                        Write value in accumulator to selected destination
F                 d7 selects register Reg0 or Reg1      Store UART received byte into selected register
'''

import argparse;

# Load up file line by line and decode
parser = argparse.ArgumentParser(description="An assembler for a small processor build in ENEL453");







