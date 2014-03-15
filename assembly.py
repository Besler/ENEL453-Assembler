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
CONSTANT_MAX = 255; # Largest number in 8 unsigned bits
CONSTANT_MIN = 0; # Only using unsigned bits
ADDRESS_MAX = 255; # Largest address
ADDRESS_MIN = 0; # Can't go lower than zero
INSTRUCTION_DICT = {
    'load'    : 0x0,
    'move'    : 0x2,
    'add'     : 0x3,
    'sub'     : 0x4,
    'sr'      : 0x5,
    'sl'      : 0x6,
    'and'     : 0x7,
    'or'      : 0x8,
    'inv'     : 0x9,
    'j'       : 0xA,
    'jaz'     : 0xB,
    'jal'     : 0xC,
    'jr'      : 0xD,
    'wri'     : 0xE,
    'str'     : 0xF
    };
INSTRUCTION_LENGTH_DICT = {
    'load'    : 3,
    'move'    : 2,
    'add'     : 2,
    'sub'     : 2,
    'sr'      : 1,
    'sl'      : 1,
    'and'     : 2,
    'or'      : 2,
    'inv'     : 1,
    'j'       : 2,
    'jaz'     : 2,
    'jal'     : 2,
    'jr'      : 1,
    'wri'     : 2,
    'str'     : 2
    };
# Helper functions
def doExit(error):
  print "ERROR: {}".format(error);
  print "Exiting..."
  os.sys.exit(1);


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
  jal   [Address]                         {Jump and link (sub routine)}
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

def getInstructionCode(lineList, LineCount):
  '''Return the instruction as a binary value'''
  code = INSTRUCTION_DICT[lineList[0]];
  instruction = '{0:012b}'.format(0);

  if(len(lineList) != INSTRUCTION_LENGTH_DICT[lineList[0]]):
    doExit("Invalid number of arguments to {0} instruciton on line {1}".format(lineList[0], LineCount));

  try:
    if(len(lineList) == 3):
      # Test bounds of constant
      if(int(lineList[1]) > CONSTANT_MAX or int(lineList[1]) < CONSTANT_MIN):
        doExit("Invalid constant range for instruction on line {}".format(LineCount));
      else:
        #Determine which register we are storing it in
        if(lineList[2] == 'reg0'):
          instruction = '0000' + '{:08b}'.format(int(lineList[1]));
        elif(lineList[2] == 'reg1'):
          instruction = '0001' + '{:08b}'.format(int(lineList[1]));
        else:
          doExit("Unkown register {0} for load instruciton on line {1}".format(lineList[2], LineCount));
    elif(code == 0x2): #move
      #Determine which register we are storing it in
      if(lineList[1] == 'reg0'):
        instruction = '0010' + '00000000';
      elif(lineList[1] == 'reg1'):
        instruction = '0010' + '10000000';
      else:
        doExit("Unkown register {0} for move instruciton on line {1}".format(lineList[1], LineCount));
    elif(code == 0x3): #add
      if(lineList[1] == 'reg0'):
        instruction = '0011' + '00000000';
      elif(lineList[1] == 'reg1'):
        instruction = '0011' + '10000000';
      else:
        doExit("Unkown register {0} for add instruciton on line {1}".format(lineList[1], LineCount));
    elif(code == 0x4): #sub
      if(lineList[1] == 'reg0'):
        instruction = '0100' + '00000000';
      elif(lineList[1] == 'reg1'):
        instruction = '0100' + '10000000';
      else:
        doExit("Unkown register {0} for sub instruciton on line {1}".format(lineList[1], LineCount));
    elif(code == 0x5): #sr
      instruction = '0101' + '00000000';
    elif(code == 0x6): #sl
      instruction = '0110' + '00000000';
    elif(code == 0x7): #and
      if(lineList[1] == 'reg0'):
        instruction = '0111' + '00000000';
      elif(lineList[1] == 'reg1'):
        instruction = '0111' + '10000000';
      else:
        doExit("Unkown register {0} for and instruciton on line {1}".format(lineList[1], LineCount));
    elif(code == 0x8): #or
      if(lineList[1] == 'reg0'):
        instruction = '1000' + '00000000';
      elif(lineList[1] == 'reg1'):
        instruction = '1000' + '10000000';
      else:
        doExit("Unkown register {0} for or instruciton on line {1}".format(lineList[1], LineCount));
    elif(code == 0x9): #inv
      instruction = '1001' + '00000000';
    elif(code == 0xA): #j
      if(int(lineList[1]) > ADDRESS_MAX or int(lineList[1]) < ADDRESS_MIN):
        doExit("Invalid address range for instruction on line {}".format(LineCount));
      else:
        instruction = '1010' + '{:08b}'.format(int(lineList[1]));
    elif(code == 0xB): #jaz
      if(int(lineList[1]) > ADDRESS_MAX or int(lineList[1]) < ADDRESS_MIN):
        doExit("Invalid address range for instruction on line {}".format(LineCount));
      else:
        instruction = '1011' + '{:08b}'.format(int(lineList[1]));
    elif(code == 0xC): #jal
      if(int(lineList[1]) > ADDRESS_MAX or int(lineList[1]) < ADDRESS_MIN):
        doExit("Invalid address range for instruction on line {}".format(LineCount));
      else:
        instruction = '1100' + '{:08b}'.format(int(lineList[1]));
    elif(code == 0XD): #jr
      instruction = '1101' + '00000000';
    elif(code == 0xE): #wri
      if(lineList[2] == 'reg0'):
        instruction = '1110' + '00000' + '000';
      elif(lineList[2] == 'reg1'):
        instruction = '1110' + '00000' + '001';
      elif(lineList[2] == 'P1'):
        instruction = '1110' + '00000' + '010';
      elif(lineList[2] == 'P2'):
        instruction = '1110' + '00000' + '011';
      elif(lineList[2] == 'Tx'):
        instruction = '1110' + '00000' + '100';
      else:
        doExit("Unkown register {0} for wri instruciton on line {1}".format(lineList[2], LineCount));
    elif(code == 0xF): #str
      if(lineList[1] == 'reg0'):
        instruction = '1111' + '00000000';
      elif(lineList[1] == 'reg1'):
        instruction = '1111' + '10000000';
      else:
        doExit("Unkown register {0} for str instruciton on line {1}".format(lineList[1], LineCount));
  except:
    doExit("Unkown error occured on line {}".format(LineCount));
  return instruction;

def fixString(line):
  '''Fix the string we receive for any not wanted characters'''
  # Remove comments, deal with empty lines                            # Example '    LoAd     123   Reg0   #Mean #Comment'
  if('#' in line):                                                    # '    LoAd     123   Reg0   '
    line = line[0:line.find('#')];
  line = line.strip(); #Remove leading and trailing whitespace      # 'LoAd     123   Reg0'
  # If empty, continue
  if(line == ''):
    return [];

  # Remove cases where there are extra spaces between characters
  lineList = [c for c in line.lower().split(' ')];
  while '' in lineList:
    lineList.remove('')                                               # ['load','123','reg0']

  return lineList;

# Parse Arguments
parser = argparse.ArgumentParser( description='An assembler for a small processor build in ENEL453',
                                  version=0.1
                                  );

parser.add_argument(  'filename',
                      help='File name of the file you would like to convert to assembly',
                      nargs='*',
                      );
parser.add_argument(  '-i', '--instructions',
                      action='store_true',
                      help='Print Instructions and exit'
                      );
parser.add_argument(  '-b', '--binary',
                      help='Output in binary, default is hex',
                      action='store_true',
                      default=False
                      );
args = parser.parse_args();

if args.instructions:
  printInstructions();

if len(args.filename) == 0:
  parser.print_help();
  doExit("Did not receive a file to assemble");

for name in args.filename:
  # Attempt to open output file
  try:
    out = open(os.path.splitext(name)[0] + DOT_FILE_EXTENSION, 'w');
  except IOError as e:
    doExit("I/O error({0}): {1}".format(e.errno, e.strerror));
  except ValueError:
    doExit("Unable to convert file names to strings");

  # Read line by line to parse
  with open(name) as f:
    # Keep a line counter for error handling
    LineCount = int(0);

    # Loop though lines handling them all
    for line in f.readlines():
      LineCount += 1;

      lineList = fixString(line);
      if(lineList == []):
        continue;

      if lineList[0] in INSTRUCTION_DICT:
        instructionCode = getInstructionCode(lineList, LineCount);
      else:
        doExit('Unkown code {0} at line {1}'.format(lineList, LineCount));

      if(args.decimal == False):
        instructionCode = "{0:#05X}".format(int(instructionCode,2));

      out.write(instructionCode);
      out.write('\n');
  out.close();























