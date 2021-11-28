
from io import open_code
from multipledispatch import dispatch 
RAM_LOCATION_ONE = 11
MEMORY_SIZE = 1000
CODE_STORAGE_LOCATION_ONE = 511
outputFile = open("OutputFile.txt", "w")
# inputPort  = open("inputPort.txt", "r")
# outputPort = open("outputPort.txt", "w")
'''
Memory can also store the instructions and this way we can very easily acheive looping. With PC tracking, looping can be done easily.
We can also make PC tracking consistent with complete execution.
'''
register_list =['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'a']

instruction_list = {'add' : [2, "0000", "RR"],
                     'ada' : [1, "0001", "R"],
                     'ld' : [1, "0010", "R"],
                     'str' : [1, "0011", "R"],
                     'out' : [1, "0100", "R"],
                     'mov' : [2, "0101", "R?"],
                     'in' : [1, "0110", "?"],
                     'mul' : [2, "0111", "RR"],
                     'muli' : [1, "1000", "R"],
                     'div' : [2, "1001", "RR"],
                     'divi' : [1, "1010", "R"],
                     'hlt' : [0, "1011", "?"],
                     'jz' : [2, "1110", "RR"],
                     'jnz' : [2, "10000", "RR"],
                     'sub' : [2, "1111", "RR"],
                     'or' : [2,"10001","RR"],
                     'and' : [2,"10010","RR"],
                     'ora' : [1,"10011","R"],
                     'anda' : [1,"10100","R"],
                     'not' : [1,"10101","R"],
                     'add2' : [3,"1100","RRR"],
                     'suba' : [1, "1101", "RR"],
                     'sub2' : [3, "11111", "RRR"]} # Jump to the location stored in the Register 2 if Register 1 is zero in value


instructionList = []

def getValueOfRegister(regString): # We will be keeping track of the register vaues separately
    # ! this has to be be defined under the class memory
    registerValue = RAMObjectGlobal.returnRegisterValue(regString)
    return registerValue

class Memory:
    def __init__(self):
        print("Memory initialized")
        self.__Memory = [0]*MEMORY_SIZE
        print("Program counter initialized to ", CODE_STORAGE_LOCATION_ONE)
        self.__programCounter = CODE_STORAGE_LOCATION_ONE
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
    def setProgramCounterTo(self, val):
        print("PC value set to :", val,"(Line number: ",val - CODE_STORAGE_LOCATION_ONE ,")")
        self.__programCounter = val
    def getProgramCounter(self):
        return self.__programCounter

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
        self.__R1 = 10 # These can be shifter to RAM class later (child of memory)
        self.__R2 = 5
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
        elif(regString.lower() == "a"):
            self.__A = val
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
        elif (regString.lower() == 'a'):
            return self.__A
    
    def printRegisterStatus(self):
        print("R1,R2,R3,R4,R5,R6,A = ", self.__R1,",",self.__R2,",", self.__R3,",", self.__R4, ",", self.__R5, ",", self.__R6, ",", self.__A)

    def setAccumulator(self, value):
        self.__A = value
    def addToAccumulator(self,value): 
        print("Value stored in Accumulator: ", self.__A)
        self.__A += value
    def getAccumulator(self): # Accumulator Getter
        return self.__A
    def multiplyToAccumulator(self,value): 
        print("Value stored in Accumulator: ", self.__A)
        self.__A *= value
    def orToAccumulator(self,value): 
        print("Value stored in Accumulator: ", self.__A)
        self.__A |= value
    def andToAccumulator(self,value): 
        print("Value stored in Accumulator: ", self.__A)
        self.__A &= value    

    def divideToAccumulator(self,value): 
        print("Value stored in Accumulator: ", self.__A)      
        try:
            self.__A /= value
        except Exception as e:
            print("Cannot execute division operation because of exception ", e)
        else:
            quot = RAMObjectGlobal.getAccumulator()
            print("Executing DIVI command")
            print("Quotient of Accumulator reg and ", value, "is calculated to be :", quot)
            return quot



    def setRegA(self, value):
        self.__A = value
    def getRegA(self):
        return self.__A
    def performLoadInstruction(self, reg):
        memoryLocation = getValueOfRegister(reg) # this is the memory location
        self.setAccumulator(self.getDataAtLocation(memoryLocation))
    def performStoreInstruction(self, reg):
        memoryLocation = getValueOfRegister(self.reg) # this is the memory location
        self.writeAtLocation(memoryLocation, self.getAccumulator())

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
            print("executing ADD")
            self.opcode = "0000" # ! This needs to be removed since this is already hard coded
            self.numOperands = 2
            self.reg1 = insString.split()[1] # String 
            self.reg2 = insString.split()[2]
            self.reg3 = "ZERO"
            # self.performOperation()    
        elif opcode == "ada":
            print("ADA class object created")
            print("executing ADA")
            self.opcode = "0001"
            self.numOperands = 1
            self.reg1 = insString.split()[1]  # String 
            self.reg2 = "ZERO"
            self.reg3 = "ZERO"
            # self.performOperation()
        elif opcode == "add2":
            print("ADD class object created")
            print("executing ADD2")
            self.opcode = "1100" # ! This needs to be removed since this is already hard coded
            self.numOperands = 3
            self.reg1 = insString.split()[1]
            self.reg2 = insString.split()[2] # String 
            self.reg3 = insString.split()[3]
            # self.performOperation()
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
        print("Accumulator value after ADD command ", RAMObjectGlobal.getAccumulator())
        return sum
    @dispatch(object)
    def addition(self, reg1):
        RAMObjectGlobal.addToAccumulator(reg1)
        sum = RAMObjectGlobal.getAccumulator()
        print("Executing ADA command")
        print("Sum of ", reg1, " and Accumulator reg", "Was calculated to be :", sum)
        print("Accumulator value after ADA command ", RAMObjectGlobal.getAccumulator())
        # RAMObjectGlobal.printRegisterStatus()
        return sum
    @dispatch(object,object,object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    def addition(self, reg1, reg2,reg3):
        # reg1Val = getValueOfRegister(self.reg1) # now I will pass the integer value rather than the string (I can get the register in the last function that I call)
        # reg2Val = getValueOfRegister(self.reg2)
        # sum = reg1Val + reg2Val
        sum = reg2 + reg3 
        RAMObjectGlobal.setRegisterToValue(self.reg1,sum)
        print("Executing ADD2 command")
        print("Sum of ", reg2, " and ", reg3, "Was calculated to be :", sum)
        # print("Register value after ADD2 command ", RAMObjectGlobal.returnRegisterValue())
        RAMObjectGlobal.printRegisterStatus()
        return sum     
    def performOperation(self):
        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        reg3Val = getValueOfRegister(self.reg3)

        if self.numOperands == 1:
            sum = self.addition(reg1Val)
        elif self.numOperands == 2:
            sum = self.addition(reg1Val, reg2Val)
        elif self.numOperands == 3:
            sum = self.addition(reg1Val,reg2Val, reg3Val)    
        # if self.opcode == "0001": #ada command
            # RAMObjectGlobal.addToAccumulator(sum)
            # print("Value ", sum, " was added to the acc || Accumulator Status : ",RAMObjectGlobal.getAccumulator() )
        return sum
class Sub(ALU):
    def __init__(self, insString):
        ALU.__init__(self)
        # self.opcode = "0000"
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "sub":
            print("SUB class object created")
            self.opcode = "0000" # ! This needs to be removed since this is already hard coded
            self.numOperands = 2
            self.reg1 = insString.split()[1] # String 
            self.reg2 = insString.split()[2]
            self.reg3 = "ZERO"
            # self.performOperation()
        elif opcode == "suba":
            print("SUB class object created")
            self.opcode = "1101"
            self.numOperands = 1
            self.reg1 = insString.split()[1]  # String 
            self.reg2 = "ZERO"
            self.reg3 = "ZERO"
            # self.performOperation()
        elif opcode == "sub2":
            print(" SUB class object created")
            self.opcode = "11111" # ! This needs to be removed since this is already hard coded
            self.numOperands = 3
            self.reg1 = insString.split()[1]
            self.reg2 = insString.split()[2] # String 
            self.reg3 = insString.split()[3]
            # self.reg3 = "ZERO"
            # self.performOperation()
        self.performOperation()    
        # self.performOperation(getValueOfRegister(self.reg1), getValueOfRegister(self.reg2))
    @dispatch(object, object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    def subtraction(self, reg1, reg2):
        # reg1Val = getValueOfRegister(self.reg1) # now I will pass the integer value rather than the string (I can get the register in the last function that I call)
        # reg2Val = getValueOfRegister(self.reg2)
        # sum = reg1Val + reg2Val
        difference = reg2 - reg1
        RAMObjectGlobal.setAccumulator(difference)
        print("Executing SUB command")
        print("Difference of ", reg1, " and ", reg2, "Was calculated to be :", difference)
        return difference
    @dispatch(object)
    def subtraction(self, reg1):
        newreg1 = reg1*(-1)
        RAMObjectGlobal.addToAccumulator(newreg1)
        difference = RAMObjectGlobal.getAccumulator()
        print("Executing SUBA command")
        print("Difference of ", reg1, " and Accumulator reg", "Was calculated to be :", difference)
        RAMObjectGlobal.printRegisterStatus()
        return difference
    @dispatch(object, object,object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    def subtraction(self, reg1, reg2,reg3):
        # reg1Val = getValueOfRegister(self.reg1) # now I will pass the integer value rather than the string (I can get the register in the last function that I call)
        # reg2Val = getValueOfRegister(self.reg2)
        # sum = reg1Val + reg2Val
        difference = reg2 - reg3 
        RAMObjectGlobal.setRegisterToValue(self.reg1,difference)
        print("Executing SUB2 command")
        print("Difference of ", reg2, " and ", reg3, "Was calculated to be :", difference)
        RAMObjectGlobal.printRegisterStatus()
        return difference     
    def performOperation(self):
        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        reg3Val = getValueOfRegister(self.reg3)

        if self.numOperands == 1:
            difference = self.subtraction(reg1Val)
        elif self.numOperands == 2:
            difference = self.subtraction(reg1Val, reg2Val)
        elif self.numOperands == 3:
            difference = self.subtraction(reg1Val,reg2Val, reg3Val)    
        # if self.opcode == "0001": #ada command
            # RAMObjectGlobal.addToAccumulator(sum)
            # print("Value ", sum, " was added to the acc || Accumulator Status : ",RAMObjectGlobal.getAccumulator() )
        return difference    
    # @dispatch(object, object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    # def performOperation(self, reg1, reg2):
    #     # reg1Val = getValueOfRegister(self.reg1) # now I will pass the integer value rather than the string (I can get the register in the last function that I call)
    #     # reg2Val = getValueOfRegister(self.reg2)
    #     # sum = reg1Val + reg2Val
    #     diff = reg1 - reg2
    #     RAMObjectGlobal.setAccumulator(diff)
    #     print("Executing SUB command")
    #     print("Subtraction of ", reg1, " and ", reg2, "Was calculated to be :", diff)
    #     return sum
RAMObjectGlobal = RAM()

class InstructionDecoder:
    def __init__(self):
        self.temp = 0
    def parseFileDecodeInstructions(self, inputFile):
        self.parseFileStoreToMemory(inputFile)
        while RAMObjectGlobal.getProgramCounter() < MEMORY_SIZE:
            line = RAMObjectGlobal.getDataAtLocation(RAMObjectGlobal.getProgramCounter())
            RAMObjectGlobal.setProgramCounterTo(RAMObjectGlobal.getProgramCounter() + 1)
            if(line[0:2] == "//"): # ! Handles a comment
                continue
            self.validateInstruction(line, RAMObjectGlobal.getProgramCounter() - 1)
            instructionObject = self.createInstructionObject(line)
            instructionList.append(instructionObject) # Add the validate instruction functions here.
        '''with open(inputFile, 'r') as f:
            lineNumber = 0
            for line in f:
                lineNumber += 1
               
                if(line[0:2] == "//"): # ! Handles a comment
                    continue
                self.validateInstruction(line, lineNumber)
                instructionObject = self.createInstructionObject(line)
                instructionList.append(instructionObject) # Add the validate instruction functions here.'''
    def parseFileStoreToMemory(self, inputFile):
        print("Started copying code into the memory")
        try:
            f = open(inputFile, 'r')
            #with open(inputFile, 'r') as f:
                #lineNumber = CODE_STORAGE_LOCATION_ONE - 1
                #for line in f:
                    #lineNumber += 1
                    #RAMObjectGlobal.writeAtLocation(lineNumber, line)
        except Exception as ef:
            print(ef)
        else:
             with open(inputFile, 'r') :
             #as f:
                lineNumber = CODE_STORAGE_LOCATION_ONE - 1
                for line in f:
                    lineNumber += 1
                    RAMObjectGlobal.writeAtLocation(lineNumber, line)

        finally:
            f.close()

        # RAMObjectGlobal.printMemoryStatus() # Printing the memory status
    def createInstructionObject(self,instructionString):
        opcode = instructionString.split()[0]
        print("Opcode : ", opcode)
        # if opcode.lower() == "add" or "ada":
        if opcode.lower() == "add" or opcode.lower() == "ada" or opcode.lower() == "add2":
            addObject = Add(instructionString) # Object once created by itself performs all the validation and execution
            instructionList.append(addObject)
        if opcode.lower() == "or" or opcode.lower() == "ora":
            addObject = OR(instructionString) # Object once created by itself performs all the validation and execution
            instructionList.append(addObject)
        if opcode.lower() == "and" or opcode.lower() == "anda":
            addObject = AND(instructionString) # Object once created by itself performs all the validation and execution
            instructionList.append(addObject) 
        if opcode.lower() == "not":
            addObject = NOT(instructionString) # Object once created by itself performs all the validation and execution
            instructionList.append(addObject)            
        if opcode.lower() == "mul" or opcode.lower() == "muli":
            addObject = MUL(instructionString) # Object once created by itself performs all the validation and execution
            instructionList.append(addObject)
        if opcode.lower() == "div" or opcode.lower() == "divi":
            addObject = DIV(instructionString) # Object once created by itself performs all the validation and execution
            instructionList.append(addObject)
        if opcode.lower() == "sub" or opcode.lower() == "suba" or opcode.lower() == "sub2":
            print( "SUB instruction identified" )
            subObject = Sub(instructionString)
            instructionList.append(subObject)
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
        if(opcode.lower() == "hlt"):
            print("HLT statement")
            hltObject = HLT(instructionString)
            instructionList.append(hltObject)
        if(opcode.lower() == "jz" or opcode.lower() == "jnz"):
            print("JZ or JNZ instruction")
            executionControlObject = executionControl(instructionString)
            instructionList.append(executionControlObject)
    
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
                print("Checking if the register", operand," is valid or not")
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
        # if inputString[0].lower() == "r":
        for reg in register_list:
            if reg == inputString.lower():
                return True
        print("ERROR : Register number out of range ,Line number :", lineNumber)
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
        # RAM.__init__(self)
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

class MUL(ALU): # All ADD ADA (Add to acc ) can create a single object 
    # this defines the type of operation
    def __init__(self, insString):
        ALU.__init__(self)
        # self.opcode = "0000"
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "mul":
            print("MUL class object created")
            self.opcode = "0111" # ! This needs to be removed since this is already hard coded
            self.numOperands = 2
            self.reg1 = insString.split()[1] # String 
            self.reg2 = insString.split()[2]
        elif opcode == "muli":
            print("MULI class object created")
            self.opcode = "1000"
            self.numOperands = 1
            self.reg1 = insString.split()[1]  # String 
            self.reg2 = "ONE"
        self.performOperation()
    @dispatch(object, object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    def multiplication(self, reg1, reg2):
        # reg1Val = getValueOfRegister(self.reg1) # now I will pass the integer value rather than the string (I can get the register in the last function that I call)
        # reg2Val = getValueOfRegister(self.reg2)
        # sum = reg1Val + reg2Val
        prod = reg1 * reg2
        RAMObjectGlobal.setAccumulator(prod)
        print("Executing MUL command")
        print("Product of ", reg1, " and ", reg2, "Was calculated to be :", prod)
        return prod
    @dispatch(object)
    def multiplication(self, reg1):
        RAMObjectGlobal.multiplyToAccumulator(reg1)
        prod = RAMObjectGlobal.getAccumulator()
        print("Executing MULI command")
        print("Product of ", reg1, " and Accumulator reg", "Was calculated to be :", prod)
        return prod
    def performOperation(self):
        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        if self.numOperands == 1:
            prod = self.multiplication(reg1Val)
        else:
            prod = self.multiplication(reg1Val, reg2Val)
        # if self.opcode == "0001": #ada command
            # RAMObjectGlobal.addToAccumulator(sum)
            # print("Value ", sum, " was added to the acc || Accumulator Status : ",RAMObjectGlobal.getAccumulator() )
        return prod    

class OR(ALU): # All ADD ADA (Add to acc ) can create a single object 
    # this defines the type of operation
    def __init__(self, insString):
        ALU.__init__(self)
        # self.opcode = "0000"
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "or":
            print("OR class object created")
            self.opcode = "10001" # ! This needs to be removed since this is already hard coded
            self.numOperands = 2
            self.reg1 = insString.split()[1] # String 
            self.reg2 = insString.split()[2]
        elif opcode == "ora":
            print("ORA class object created")
            self.opcode = "10011"
            self.numOperands = 1
            self.reg1 = insString.split()[1]  # String 
            self.reg2 = "ONE"
        self.performOperation()
    @dispatch(object, object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    def logicalor(self, reg1, reg2):
        # reg1Val = getValueOfRegister(self.reg1) # now I will pass the integer value rather than the string (I can get the register in the last function that I call)
        # reg2Val = getValueOfRegister(self.reg2)
        # sum = reg1Val + reg2Val
        orout = reg1 | reg2
        RAMObjectGlobal.setAccumulator(orout)
        print("Executing OR command")
        print("OR of ", reg1, " and ", reg2, "Was calculated to be :", orout)
        return orout
    @dispatch(object)
    def logicalor(self, reg1):
        RAMObjectGlobal.orToAccumulator(reg1)
        orout = RAMObjectGlobal.getAccumulator()
        print("Executing ORA command")
        print("OR of ", reg1, " and Accumulator reg", "Was calculated to be :", orout)
        return orout
    def performOperation(self):
        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        if self.numOperands == 1:
            orout = self.logicalor(reg1Val)
        else:
            orout = self.logicalor(reg1Val, reg2Val)
        # if self.opcode == "0001": #ada command
            # RAMObjectGlobal.addToAccumulator(sum)
            # print("Value ", sum, " was added to the acc || Accumulator Status : ",RAMObjectGlobal.getAccumulator() )
        return orout   

class AND(ALU): # All ADD ADA (Add to acc ) can create a single object 
    # this defines the type of operation
    def __init__(self, insString):
        ALU.__init__(self)
        # self.opcode = "0000"
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "and":
            print("AND class object created")
            self.opcode = "10010" # ! This needs to be removed since this is already hard coded
            self.numOperands = 2
            self.reg1 = insString.split()[1] # String 
            self.reg2 = insString.split()[2]
        elif opcode == "anda":
            print("ANDA class object created")
            self.opcode = "10100"
            self.numOperands = 1
            self.reg1 = insString.split()[1]  # String 
            self.reg2 = "ONE"
        self.performOperation()
    @dispatch(object, object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    def logicaland(self, reg1, reg2):
        # reg1Val = getValueOfRegister(self.reg1) # now I will pass the integer value rather than the string (I can get the register in the last function that I call)
        # reg2Val = getValueOfRegister(self.reg2)
        # sum = reg1Val + reg2Val
        andout = reg1 & reg2
        RAMObjectGlobal.setAccumulator(andout)
        print("Executing AND command")
        print("AND of ", reg1, " and ", reg2, "Was calculated to be :", andout)
        return andout
    @dispatch(object)
    def logicaland(self, reg1):
        RAMObjectGlobal.andToAccumulator(reg1)
        andout = RAMObjectGlobal.getAccumulator()
        print("Executing ANDA command")
        print("AND of ", reg1, " and Accumulator reg", "Was calculated to be :", andout)
        return andout
    def performOperation(self):
        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        if self.numOperands == 1:
            andout = self.logicaland(reg1Val)
        else:
            andout = self.logicaland(reg1Val, reg2Val)
        # if self.opcode == "0001": #ada command
            # RAMObjectGlobal.addToAccumulator(sum)
            # print("Value ", sum, " was added to the acc || Accumulator Status : ",RAMObjectGlobal.getAccumulator() )
        return andout      

class NOT(ALU): # All ADD ADA (Add to acc ) can create a single object 
    # this defines the type of operation
    def __init__(self, insString):
        ALU.__init__(self)
        # self.opcode = "0000"
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "not":
            print("NOT class object created")
            self.opcode = "10101" # ! This needs to be removed since this is already hard coded
            self.numOperands = 1
            self.reg1 = insString.split()[1] # String 
            #self.reg2 = "ONE"
        
        self.performOperation()
    
    @dispatch(object)
    def logicalnot(self, reg1):

        notout = ~reg1 
        RAMObjectGlobal.setAccumulator(notout)
        print("Executing NOT command")
        print("NOT of ", reg1,"Was calculated to be :", notout)
        return notout
    
    def performOperation(self):
        reg1Val = getValueOfRegister(self.reg1)
        
        notout = self.logicalnot(reg1Val)
        
        # if self.opcode == "0001": #ada command
            # RAMObjectGlobal.addToAccumulator(sum)
            # print("Value ", sum, " was added to the acc || Accumulator Status : ",RAMObjectGlobal.getAccumulator() )
        return notout      
      
class DIV(ALU): # All ADD ADA (Add to acc ) can create a single object 
    # this defines the type of operation
    def __init__(self, insString):
        ALU.__init__(self)
        # self.opcode = "0000"
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "div":
            print("DIV class object created")
            self.opcode = "1001" # ! This needs to be removed since this is already hard coded
            self.numOperands = 2
            self.reg1 = insString.split()[1] # String 
            self.reg2 = insString.split()[2]
        elif opcode == "divi":
            print("DIVI class object created")
            self.opcode = "1010"
            self.numOperands = 1
            self.reg1 = insString.split()[1]  # String 
            self.reg2 = "ONE"
        self.performOperation()
    @dispatch(object, object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    def division(self, reg1, reg2):
        try:
            quot = reg1 / reg2
        except Exception as ex:
            print ("Cannot execute the division function because of exception:", ex)
        else:
            RAMObjectGlobal.setAccumulator(quot)
            print("Executing DIV command")
            print("Product of ", reg1, " and ", reg2, "Was calculated to be :", quot)
            return quot
    @dispatch(object)
    def division(self, reg1):
        RAMObjectGlobal.divideToAccumulator(reg1)
        #quot = RAMObjectGlobal.getAccumulator()
        #print("Executing DIVI command")
        #print("Quotient of ", reg1, " and Accumulator reg", "Was calculated to be :", quot)
        #return quot
    def performOperation(self):
        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        if self.numOperands == 1:
            quot = self.division(reg1Val)
        else:
            quot = self.division(reg1Val, reg2Val)
        # if self.opcode == "0001": #ada command
            # RAMObjectGlobal.addToAccumulator(sum)
            # print("Value ", sum, " was added to the acc || Accumulator Status : ",RAMObjectGlobal.getAccumulator() )
        return quot
class HLT():
    def __init__(self, insString):
        self.opcode = insString.split()[0]
        self.performOperation()
    def performOperation(self):
        print ("Program Halted")
        exit(0)

class executionControl():
    def __init__(self, insString):
        # self.jumpedFromAddress = 0
        self.opcode = insString.split()[0]
        self.opcode = self.opcode.lower()
        self.reg1 = insString.split()[1]
        self.reg2 = insString.split()[2]
        self.reg1Val = getValueOfRegister(self.reg1)
        self.reg2val = getValueOfRegister(self.reg2)
        # print("Reg 1 val for jz : ", self.reg1Val())
        self.performOperation()
    def jumpTo(self, location):
        print("PC to be set to :", location)
        RAMObjectGlobal.setProgramCounterTo(location)
    def performOperation(self):
        
        if self.opcode.lower() == "jz":
            print("Execution of JZ instruction starts")
            if self.reg1Val == 0:
                print("reg value zero satisfied")
                locationToJumpTo = self.reg2val
                self.jumpTo(locationToJumpTo)
        if self.opcode.lower() == "jnz":
            print("Execution of JNZ instruction starts")
            if self.reg1Val != 0:
                print("reg value non zero satisfied")
                locationToJumpTo = self.reg2val
                self.jumpTo(locationToJumpTo)
        
    # def performOperation


'''
Ideo of IO:-
1. Output : output has to be printed using this. This should pront the operation that is happening.
'''


'''TO DO
    1. Implement doxygen 
    2. Github
    3. Classes structure visubalization ->  Can be done
    4. Profiling report ***
    5. Package implementation ***
    6. Different variations of methods
'''

# ! Instructions should also be stored in memory