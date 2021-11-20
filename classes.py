
from multipledispatch import dispatch 
RAM_LOCATION_ONE = 11
MEMORY_SIZE = 100
outputFile = open("OutputFile.txt", "w")
# inputPort  = open("inputPort.txt", "r")
# outputPort = open("outputPort.txt", "w")
'''
Memory can also store the instructions and this way we can very easily acheive looping. With PC tracking, looping can be done easily.
We can also make PC tracking consistent with complete execution.
'''
register_list =['r1', 'r2', 'r3', 'r4', 'r5', 'r6']

instruction_list = {'add' : [2, "0000", "RR"],
                     'ada' : [1, "0001", "R"],
                     'ld' : [1, "0010", "R"],
                     'str' : [1, "0011", "R"],
                     'out' : [1, "0100", "R"],
                     'mov' : [2, "0101", "R?"],
                     'in' : [1, "0110", "?"]} # in needs only the port name hence port name can be anything :  We can also check for this later(Fix number of ports)


instructionList = []


class Memory:
    def __init__(self):
        print("Memory initialized")
        self.__Memory = [0]*MEMORY_SIZE
      
        self.ROMContent = ["Group","Members","are","Gagandeep","Rajat","Sindhu","Soumya","All","the","Best"]
        self.memoryBooting()
        # ROM can have error messages that can be accesed later 
    def memoryBooting(self):
        for i in range (0,RAM_LOCATION_ONE - 1):
            self.__Memory[i] = self.ROMContent[i] 

            '''For inplementing SQL database you just need to implement some queries'''
    def getDataAtLocation(self,loc):
        if(loc > MEMORY_SIZE or loc < 0):
            # Error logs can be created (IO class can be used)
            print("Wrong memory location: ", loc," accessed : Exiting")
            exit()
        if(loc + 1 > len(self.__Memory)):
            print("Random location accessed where no data was stored, exiting")
            exit()
        return self.__Memory[loc]
    def writeAtLocation(self,loc,data): # Can write any data, No constraint on writing specific data type

        if(loc < 11):
            # Error logs can be created (IO class can be used)
            print("Wrong memory location: ", loc," writing tried (writing to ROM) : Exiting")
            exit()
        if(loc > MEMORY_SIZE):
            # Error logs can be created (IO class can be used)
            print("Wrong memory location: ", loc," writing tried : Exiting")
            exit()
        
        self.__Memory[loc] = data
    def printMemoryStatus(self):
        for i in range (0, MEMORY_SIZE):
            print("Loc ", i, ": ", self.__Memory[i])

        # First 10 locations are ROM location  
        # We can store all the data in memory 
        # RAM has setters and getters bot h
        # ROM has getters only

        # Two functions
        # Read and writeAtLocation
        #! Read can be common to ROM and RAM . But only RAM should beb able to write at any location
class RAM(Memory):
    def __init__(self):
        Memory.__init__(self)
        self.__accumulatorReg = 0                                               # ! Abstraction (Something OOPS)
        self.__R1 = 0 # These can be shifter to RAM class later (child of memory)
        self.__R2 = 0
        self.__R3 = 0
        self.__R4 = 0
        self.__R5 = 0
        self.__R6 = 0
        self.__A = 0 # This is IO register
        # IN P -> this instruction means that any value at this port P should be stored into register A
        # OUT P -> Any value in register A should be outputted at the port P
        # We can realize a port by a file.
        
        self.initialLocation = RAM_LOCATION_ONE 
    def setR1(self,val):
        self.__R1 = val
    def setRegisterToValue(self, regString, val):
        if(regString.lower() == "r1"):
            self.__R1 = val
            print("Register R1 assigned a value :", val)
            print("Value of the R1 is  : ", self.__R1)
        elif(regString.lower() == "r2"):
            self.__R2 = val
        elif(regString.lower() == "r3"):
            self.__R3 = val
        elif(regString.lower() == "r4"):
            self.__R4 = val
        elif(regString.lower() == "r5"):
            self.__R5 = val
        elif(regString.lower() == "r6"):
            self.__R6 = val
        # elif(regString.lower() == )
    def returnRegisterValue(self,regString): # common getter
        if(regString.lower() == "r1"):
            return self.__R1
        elif(regString.lower() == "r2"):
            return self.__R2
        elif(regString.lower() == "r3"):
            return self.__R3
        elif(regString.lower() == "r4"):
            return self.__R4
        elif(regString.lower() == "r5"):
            return self.__R5
        elif(regString.lower() == "r6"):
            return self.__R6
        elif(regString.lower() == "zero"):
            return 0
    
    def printRegisterStatus(self):
        print("R1,R2,R3,R4,R5,R6 = ", self.__R1,",",self.__R2,",", self.__R3,",", self.__R4, ",", self.__R5, ",", self.__R6)

    def setAccumulator(self, value):
        self.__accumulatorReg = value
    def addToAccumulator(self,value): 
        self.__accumulatorReg += value
    def getAccumulator(self): # Accumulator Getter
        return self.__accumulatorReg

    def setRegA(self, value):
        self.__A = value
    def getRegA(self):
        return self.__A
    
class ALU:
    def __init__(self):
        print("ALU Object created")
class Add(ALU): # All ADD ADA (Add to acc ) can create a single object 
    # this defines the type of operation
    def __init__(self, insString):
        ALU.__init__(self)
        # self.opcode = "0000"
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "add":
            print("ADD class object created")
            self.opcode = "0000" # ! This needs to be removed since this is already hard coded
            self.numOperands = 2
            self.reg1 = insString.split()[1] # String 
            self.reg2 = insString.split()[2]
        elif opcode == "ada":
            print("ADA class object created")
            self.opcode = "0001"
            self.numOperands = 1
            self.reg1 = insString.split()[1]  # String 
            self.reg2 = "ZERO"
        self.performOperation()
    @dispatch(object, object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    def addition(self, reg1, reg2):
        # reg1Val = getValueOfRegister(self.reg1) # now I will pass the integer value rather than the string (I can get the register in the last function that I call)
        # reg2Val = getValueOfRegister(self.reg2)
        # sum = reg1Val + reg2Val
        sum = reg1 + reg2
        RAMObjectGlobal.setAccumulator(sum)
        print("Executing ADD command")
        print("Sum of ", reg1, " and ", reg2, "Was calculated to be :", sum)
        return sum
    @dispatch(object)
    def addition(self, reg1):
        RAMObjectGlobal.addToAccumulator(reg1)
        sum = RAMObjectGlobal.getAccumulator()
        print("Executing ADA command")
        print("Sum of ", reg1, " and Accumulator reg", "Was calculated to be :", sum)
        return sum
    def performOperation(self):
        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        if self.numOperands == 1:
            sum = self.addition(reg1Val)
        else:
            sum = self.addition(reg1Val, reg2Val)
        # if self.opcode == "0001": #ada command
            # RAMObjectGlobal.addToAccumulator(sum)
            # print("Value ", sum, " was added to the acc || Accumulator Status : ",RAMObjectGlobal.getAccumulator() )
        return sum
        
RAMObjectGlobal = RAM()
def getValueOfRegister(regString): # We will be keeping track of the register vaues separately
    # ! this has to be be defined under the class memory
    registerValue = RAMObjectGlobal.returnRegisterValue(regString)
    return registerValue

class InstructionDecoder:
    def __init__(self):
        self.temp = 0
    def parseFileDecodeInstructions(self, inputFile):
        with open(inputFile, 'r') as f:
            lineNumber = 0
            for line in f:
                lineNumber += 1
               
                if(line[0:2] == "//"): # ! Handles a comment
                    continue
                self.validateInstruction(line, lineNumber)
                instructionObject = self.createInstructionObject(line)
                instructionList.append(instructionObject) # Add the validate instruction functions here.

    def createInstructionObject(self,instructionString):
        opcode = instructionString.split()[0]
        print("Opcode : ", opcode)
        # if opcode.lower() == "add" or "ada":
        if opcode.lower() == "add" or opcode.lower() == "ada":
            addObject = Add(instructionString) # Object once created by itself performs all the validation and execution
            instructionList.append(addObject)
        if opcode.lower() == "sub":
            print( "SUB instruction identified" )
        # if opcode.lower() == "str":
        if opcode.lower() == "ld":
            print( "LD instruction decode stage")
            ldObject = LD(instructionString)
            instructionList.append(ldObject)
        if opcode.lower() == "str":
            print( "STR instruction decode stage")
            strObject = STR(instructionString)
            instructionList.append(strObject)
        if opcode.lower() == "out":
            print("OUT instruction encountered")
            outObject = OUT(instructionString)
            instructionList.append(outObject)
        if opcode.lower() == "mov":
            print("MOV instruction encountered")
            movObject = MOV(instructionString)
            instructionList.append(movObject)
        if opcode.lower() == "in":
            print("IN statement")
            inObject = IN(instructionString)
            instructionList.append(inObject)
        
    def validateInstruction(self, instructionString, lineNumber):
        insName = instructionString.split()[0]
        if insName.lower() not in instruction_list:
            print("The command mentioned does not exist ,line number:" ,lineNumber)
            exit()
        instruction = instruction_list[insName.lower()]
        numOperands = instruction[0]
        opcode = instruction[1]
        operandTypes = instruction[2]
        isInsLenCorr = self.isInstructionLengthCorrect(instructionString, numOperands + 1)
        if isInsLenCorr == False:
            print("More/Less operands were expected, Line number : ", lineNumber)
            exit()
        print ("operandTypes : ", operandTypes)
        for i in range (0,numOperands-1): # Assuming there are only 2 operands at max for any operation (This can be expanded later)
            operand = instructionString.split()[i+1]
            if operandTypes.lower()[i] == "r":
                print("Checking if the register is valid or not")
                isRegVal = self.isRegisterValid(operand, lineNumber)
                if isRegVal == False:
                    exit()
            if operandTypes.lower()[i] == "#":
                print("Checking if the #val is valid or not")
                isImmVal = self.isImmediateValid(operand, lineNumber)
                if isImmVal == False:
                    exit()
    def isImmediateValid(self,inputString, lineNumber): # Does not allow floating point values
        if inputString[0].lower() == "#":
            splitElement = inputString[1:]
            print("Value is ", splitElement)
            if splitElement.isdigit() == True:
                return True
            print("ERROR : Immediate value can only be numerical value ,Line number :", lineNumber)
            return False
        else:
            print("ERROR : Immediate value token was expected : ", lineNumber)
            return False
    def isInstructionLengthCorrect(self,instructionString, insLength):
        lenOfInstruction = len(instructionString.split())
        if lenOfInstruction == insLength:
            return True
        else:
            print("Length found : ", lenOfInstruction)
            return False
    
    def isRegisterValid(self,inputString, lineNumber): # This would return false if register does not exist OR it is not even a register
        if inputString[0].lower() == "r":
            for reg in register_list:
                if reg == inputString.lower():
                
                    return True
            print("ERROR : Register number out of range ,Line number :", lineNumber)
            return False
        else:
            print("ERROR : Register token was expected : ", lineNumber)
            return False


    '''
    1. Operator : I can identify what is the number of operands
        Only validation related to the operator can be to identify whether or not this operator is non existant.
        I would also knwo what is the "Type" of the operands that I expect.
        Ex : ADI (Add immediate) should have a numerical value in form #<value> (Type immediate)
        ADD : I would have 2 registers
        ADI : I would have just one register
    2. Operand : These would simply be either number, registerName, Address
        I would need to validate operator by checking the type or the format.
        ! Attribute : 1. Number of operands -> X ERROR
        2. Type of operand -> X ERROR
    '''
instructionDecoderGlobal = InstructionDecoder()

class IO:
    def __init__(self):
        temp = 0
class Output(IO):
    def __init__(self):
        IO.__init__(self)
    def printToStdout(self, printStatement):
        print(printStatement)

class LD(Memory):
    def __init__(self, insString):
        Memory.__init__(self)
        self.opcode = insString.split()[0]
        self.opcode = self.opcode.lower()
        self.reg = insString.split()[1]
        self.performAction()
        print("Value of the accumulator is : ", RAMObjectGlobal.getAccumulator())
    # def storeValueAtMemoryToAccumulator(self):
    #     memoryLocation = getValueOfRegister(self.reg) # this is the memory location
    def performAction(self):
        memoryLocation = getValueOfRegister(self.reg) # this is the memory location
        RAMObjectGlobal.setAccumulator(RAMObjectGlobal.getDataAtLocation(memoryLocation))
    

class STR(Memory):
    def __init__(self, insString):
        Memory.__init__(self)
        self.opcode = insString.split()[0]
        self.opcode = self.opcode.lower()
        self.reg = insString.split()[1]
        self.performAction()
        print("Value of the accumulator while performing STORE is : ", RAMObjectGlobal.getAccumulator())
    # def storeValueAtMemoryToAccumulator(self):
    #     memoryLocation = getValueOfRegister(self.reg) # this is the memory location
    def performAction(self):
        memoryLocation = getValueOfRegister(self.reg) # this is the memory location
        RAMObjectGlobal.writeAtLocation(memoryLocation, RAMObjectGlobal.getAccumulator())
        print("Memory status : ")
        RAMObjectGlobal.printMemoryStatus()
class MOV(RAM):
    def __init__(self, insString):
        RAM.__init__(self)
        self.opcode = insString.split()[0]
        self.opcode = self.opcode.lower()
        self.reg1 = insString.split()[1]
        self.reg2 = insString.split()[2]
        self.performAction()
    def performAction(self):
        if(self.reg2[0].lower() == "r"):
            reg2Val = self.getValueOfRegister(self.reg2)
            RAMObjectGlobal.setRegisterToValue(self.reg1, reg2Val)
        elif(self.reg2[0] == "#"):
            print("Assigning the imm value")
            immVal = int(self.reg2[1:])
            print(self.reg2[1:])
            # print(type(immVal))
            RAMObjectGlobal.setRegisterToValue(self.reg1, immVal)
            RAMObjectGlobal.printRegisterStatus()
class IO():
    def __init__(self):
        self.__outFile = outputFile
        # self.__inputPortFile = inputPort # Can we also feed the file name from the code itself?
        # self.__outputPortFile = outputPort
    def toTerminal(self, x):
        print(x)
    def toOutput(self, x):
        # print("TO be printed : ", x)
        self.__outFile.write(x)
        self.__outFile.write("\n")

class OUT(IO):
    def __init__(self, insString):
        IO.__init__(self)
        self.opcode = insString.split()[0]
        self.opcode = self.opcode.lower()
        self.reg = insString.split()[1]
        self.performAction()
    def __writeToOutFile(self, string):
        self.toOutput(string)
    def __display(self,string):
        print(string)
    def performAction(self):
        regVal = getValueOfRegister(self.reg)
        self.__display(regVal)
        self.__writeToOutFile(str(regVal))
        RAMObjectGlobal.printRegisterStatus()
        
    
class IN(IO):
    def __init__(self, insString):
        IO.__init__(self)
        self.opcode = insString.split()[0]
        self.opcode = self.opcode.lower()
        self.port = insString.split()[1]
        self.performAction()
    def readFromPort(self, portFileName):
        portFile = open(portFileName+".txt", "r")
        readValue = portFile.read()
        RAMObjectGlobal.setRegA(int(readValue))
        print("Value read from the port : ", readValue)
        print("Value set to reg A : ", RAMObjectGlobal.getRegA())

    def performAction(self):
        self.readFromPort(self.port)

'''
Ideo of IO:-
1. Output : output has to be printed using this. This should pront the operation that is happening.
'''


'''TO DO
    1. Implement doxygen 
    2. Github
    3. Classes structure visualization ->  Can be done
    4. Profiling report ***
    5. Package implementation ***
    6. Different variations of methods
'''

# ! Instructions should also be stored in memory