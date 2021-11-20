import sys
import classes
from multipledispatch import dispatch    
# MOV R1 #10
# MOV R2 #20
# ADD R1 R2
# SUB R1 R2
# ADA R1
# ADA R2
# ! More checking of the validateInstruction function is needed. Immediate validation still not complete
# from classes import Add

# We will create just 6 registers, one accumulator. 
# Might or might not create program counter etc.
inputFileName = "input.OOPD.txt"
def main():
    classes.instructionDecoderGlobal.parseFileDecodeInstructions(inputFileName)
if __name__== "__main__":
    # imm = '#10.2'
    # print(isImmediateValid(imm,10))
    # instructionString = "ADD R1"
    # validateInstruction(instructionString, 1)
    main()
    # classes.RAMObjectGlobal.writeAtLocation(12,"w")
    # print(type(classes.RAMObjectGlobal.getDataAtLocation(12)))
    # classes.RAMObjectGlobal.printMemoryStatus()
    # for ins in instructionList:
    #     ins.performOperation()
    #     print("Operation being performed")
