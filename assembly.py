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
E                 D(3:0) selects either Reg0 '000' or
                  Reg1 '001' or output port P1 '010' or
                  output port P2 '011' or UART transmit
                  register '100'                        Write value in accumulator to selected destination
F                 d7 selects register Reg0 or Reg1      Store UART received byte into selected register
'''

# Imports
import argparse;
import os;

# Constants and Globals
FILE_EXTENSION = str('ass');
DOT_FILE_EXTENSION = str('.{}'.format(FILE_EXTENSION));

# Helper functions
def printInstructions():
  print """Instruction Set:
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
  jar   [Address]                         {Jump and link (sub routine)}
  jr                                      {Jump return (From sub routine)}
  wri   [Reg0, Reg1, P1, P2, Tx]          {Write accum to register}
  str   [Reg0, Reg1]                      {Store Rx from UART into register}

Examples:
  load 25 Reg0 #Comment, Comment, Comment
  load 1 Reg1
  move Reg0
  add Reg1
  sub Reg0
  wri P1      # p+++++++

List of Register:
  Reg0:   General Purpose Register
  Reg1:   General Purpose Register
  P1:     Register reading into first digit of seven segment display
  P2:     Register reading into second digit of seven segment display
  UART:   UART send register
  Rx:     UART receive register"""
  return;

# Parse Arguments
parser = argparse.ArgumentParser(description='An assembler for a small processor build in ENEL453',
                                version=0.1
                                );
parser.add_argument(  'filename',
                      help='File name of the file you would like to convert to assembly',
                      nargs=1,
                      );
parser.add_argument(  '-i', '--instructions',
                      help='Print Instructions and exit',
                      action='store_true'
                      );
parser.add_argument(  '-d', '--decimal',
                      help='Output in decimal, default is hex',
                      action='store_true'
                      );
args = parser.parse_args();

# If they want to see the instruction set, let them have it
if(args.instructions == True):
  printInstructions();
  print "Exiting...";
  os.sys.exit(0);

for name in args.filename:
  # Attempt to open output file
  try:
    out = open(os.path.splitext(name)[0] + DOT_FILE_EXTENSION, 'w');
  except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror);
  except ValueError:
    print "Unable to convert file names to strings";
    print "Exiting...";

  # Read line by line to parse
  with open(name) as f:
    # Keep a line counter for error handling
    Line = int(0);

    # Loop though lines handling them all
    for line in f.readlines():
      Line += 1;


























