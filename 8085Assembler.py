import sys
import classes
from multipledispatch import dispatch    
executionFileName = "execution.png"
inputFileName = "input.OOPD.txt"
        
def main(inputFileName):
    try:
        classes.instructionDecoderGlobal.parseFileDecodeInstructions(inputFileName, executionFileName)
    except Exception as eef:
        print(eef)
if __name__== "__main__":
    main(inputFileName)

