# OOPDProject

Instruction details :
Format:-
<instruction_name> <operands>

Operands are specified in following manner:
'Rx' = Rth register
'#x' = immediate value x
'?' = Either register or immediate value

How to run this code:
1. Open terminal in the same folder where the python and input file are stored.
2. Syntax : python <python_file_name> <input_file_name>
Example : python 8085Assembler.py input.OOPD.txt

(a) Arithmetic operations
-> add Rx1 Rx2
Addition of Rx1 and Rx2 stored in accumulator. 
-> ada Rx 
Addition of Rx and accumulator stored in accumulator.
-> add2 Rx1 Rx2 Rx3
Addition of Rx1, Rx2 and Rx3 stored in accumulator.
-> sub Rx1 Rx2
Subtraction of Rx1 and Rx2 stored in accumulator.
-> suba Rx 
Subtraction of Rx and accumulator stored in accumulator.
-> sub2 Rx1 Rx2 Rx3
Subtraction of Rx1, Rx2 and Rx3 stored in accumulator.
-> mul Rx1 Rx2
Multiplication of Rx1 and Rx2 stored in accumulator.
-> muli Rx 
Multiplication of Rx and accumulator stored in accumulator.
-> div Rx1 Rx2
Division of Rx1 and Rx2 stored in accumulator.
-> divi Rx 
Division of Rx and accumulator stored in accumulator.

(b) Logical operations
-> or Rx1 Rx2 
-> ora Rx
Stores the OR operation results of accumulator and Rx into accumulator register.
-> and  Rx1 Rx2
Bitwise AND operation between Rx1 and Rx2. Results stored in accumulator.
-> anda Rx
Stores the AND operation results of accumulator and Rx into accumulator register.
-> not  Rx
Stores the NOT operation results of accumulator and Rx into accumulator register. Not that this gives the result in 2's complement form.

(c) Memory operations
-> mov Rx ?
Moves either value stored in the register or immediate value into the register Rx.
For example:
mov R1 R2
mov R1 #10
-> ld Rx
Sets the accumulator to the value stors at address contained in the register Rx.
-> str Rx
Set the value of memory location to the value stored in the accumulator register.

(d) Branch instruction
-> jz Rx1 Rx2 
Jumps to the adress location stores in register Rx2 if Rx1 value is zero. 
-> jnz Rx Rx 
Jumps to the adress location stores in register Rx2 if Rx1 value is not zero.

(e) Control operations
-> hlt
Halts the program execution. Necessary to put at the end of input code file.

(f) Input and Output command
-> in <port_name>
Takes the value on the port into the accumulator register. "port_name" here is filename written as name.
Example:-
in P1
Here, P1 is the name of the port. P1.txt file would be the file corresponding to this port. This file acts as a port from which the value is to be read.
-> out ?
Prints the value of the register Rx to OutputFile.txt. Also, it can print a string as well.


Some general features and constraints in the assembler:-
1. Input code is case insensitive.
2. Serial execution and branching.
3. There are 6 valid general purposre registers (R1-R6).
4. There are two special purpose registers (accumulator and Program Counter)