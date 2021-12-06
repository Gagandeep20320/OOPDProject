import sys
import classes
from multipledispatch import dispatch    

n = len(sys.argv)
print("Total arguments passed:", n)
print("\nName of Python script:", sys.argv[0])
inputFileName = sys.argv[1]
generateExecutionFile = False
executionFileName = "DUMMY"
if(n > 2):
    if(sys.argv[2] == "-execution_image"):
        generateExecutionFile = True
        executionFileName = sys.argv[3]
        
def main():
    try:
        classes.instructionDecoderGlobal.parseFileDecodeInstructions(inputFileName, executionFileName, generateExecutionFile)
    except Exception as eef:
        print(eef)
if __name__== "__main__":
    main()

