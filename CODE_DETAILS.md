What all can this code do?
1. Validate the passed command
2. Create list of instructions.
3. Execute all the commands along with fetching. We can extend this to executing all the command list together once fetching is complete.

Details of the code:-
1. We have 6 registers available with us (R1-R6)
2. There is one accumulator

* The instructions are language insensitive.
Instruction Set :-
ADD <RegisterName> <RegisterName> : Put sum of both registers into the accumulator 
ADA <RegisterName> : Sum register value and accumulator
STR <RegisterName> : Copy the content of accumulator to the memory location
LD <RegisterName> : Copy the content of location into accumulator
OUT <RegisterName> : Display the valu of the register name mentioned to the standard output
MOV <RegisterName> #<ImmediateValue> : Moves the immediate value into the register specified
// :  This would mean comment
Instructions to be added :-
ADD2 <Reg1> <Reg2> <Reg3> : Add Reg1 and Reg2, and store value in Reg1
SUB2 <Reg1> <Reg2> <Reg3> : Subtract Reg3 from Reg2 and store value in Reg1
SUB <RegisterName> <RegisterName> : Subtract first register from second and put into the accumulator
SUBA <RegisterName> : Subtract register value from Acc and store into the accumulator
MUL  : All three types same as SUB/ADD
DIV : All three types same as SUB/ADD

STR -> RAM
LD -> ROM

Memory:-
    Using a list as an attribute of the Memory class and member functions perform the read and write action.
    First few memory locations are conserved as ROM memory.
    # Inplementing memory was required as stated in the problem statement
    # Implementing memory was also necessary to make statements like Load and Store work (Addressing schemes)
InstructionDecoder:-
    * This class as asked for in the problem desription is able to parse the file and do the decoding of the instructions.
    * Also this class has all the functions related to validation of instruction fetched.

IMPORTANT : Instruction Validation
! Important part is the format in which we are storing the information (hard coded) related to acceptable syntax.
! With addition of each new command in the program, we would also need to update this one



Features to be added later.
1. Program counter 
2. We can also implement a very simple stack with Stack pointer in picture.

PARTITION FOR CHANGES TO BE MADE IN THE CODE:-
{
                     

RAJAT :

ADD2 <Reg1> <Reg2> <Reg3> : Add Reg1 and Reg2, and store value in Reg1
SUB2 <Reg1> <Reg2> <Reg3> : Subtract Reg3 from Reg2 and store value in Reg1
SUB <RegisterName> <RegisterName> : Subtract first register from second and put into the accumulator
SUBA <RegisterName> : Subtract register value from Acc and store into the accumulator
'mul' : [2, "0111", "RR"],
                     'muli' : [1, "1000", "R"],
                     'div' : [2, "1001", "RR"],
                     'divi' : [1, "1010", "R"]} 
SOUMYA :

MUL  : All three types same as SUB/ADD --- Implemented This. Need some more here. Will do so----required changes done
DIV : All three types same as SUB/ADD  ----Implemented This. Need to handle case of zero. Will do so
#################### Exception handling (Using try catch block)###################
'ld' : [1, "0010", "R"],
'str' : [1, "0011", "R"],

SINDHU :
OR 
AND 
NOT
We would need bits for this.
We acan assume 8 bit register -> internally dec - 8 bit binary (predefined function to be used)
'add' : [2, "0000", "RR"],
'ada' : [1, "0001", "R"],        
'mov' : [2, "0101", "R?"],
'in' : [1, "0110", "?"],


Doxygen? -> Comments 

GAGANDEEP : 

* Demo ? 
Input file ?
Logical program : Loop

- Loop Implementation
JZ -> Pre req: PC, Memory
JZ LABEL
Debug MOV
See that the parent classes should have some significant role(Not just dummies)

