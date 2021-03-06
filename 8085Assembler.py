
from multipledispatch import dispatch 
from abc import ABC, abstractmethod 
import matplotlib.pyplot as plt
RAM_LOCATION_ONE = 11   # Creates a memory adress space fixed for the ROM
MEMORY_SIZE = 1024
CODE_STORAGE_LOCATION_ONE = 511
CODE_STORAGE_LOCATION_END = 700
# This is a 16 bit processor
outputFile = open("OutputFile.txt", "w")
timeInstant = 0

register_list =['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'a']

instruction_list = {'add' : [2, "0000", "RR"],
                     'ada' : [1, "0001", "R"],
                     'ld' : [1, "0010", "R"],
                     'str' : [1, "0011", "R"],
                     'out' : [1, "0100", "?"],
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
exceptionList = []
exceptionLineNumberList = []
executionFileName = "execution.png"
inputFileName = "input_basic.OOPD.txt"


class Memory:
    
    """ The Memory base class for all the memory and storage operations """
    
    def __init__(self):
        self.timeInstant = 0
        self.exceptionList = []
        """ The Memory base class initializer."""
        print("Memory initialized")
        self.__Memory = [0]*MEMORY_SIZE
        self.__programCounter = CODE_STORAGE_LOCATION_ONE
        self.ROMContent = ["Group","Members","are","Gagandeep","Rajat","Sindhu","Soumya","DUMMY","ROM","DATA"] # This realizes he ROM notion
        # These memory locations can only be read. These cannot be written to.
        self.memoryBooting() # This data is written to the overall memory everytime device boots up.
        # ROM can have error messages that can be accesed later 
    def resetProgramCounter(self):
        self.__programCounter = CODE_STORAGE_LOCATION_ONE
    def memoryBooting(self):
        """! This boots up the memory or initializes the ROM content that is hard coded.
        """
        for i in range (0,RAM_LOCATION_ONE - 1):
            self.__Memory[i] = self.ROMContent[i] 
            '''For inplementing SQL database you just need to implement some queries'''
    def getDataAtLocation(self,loc):
        """! Getter for the memory.
        @param loc  Location that we want to read or get.
        @return Content stored at the memory location passed.
        """
        assert loc >= 0 and loc <=MEMORY_SIZE, "Memory accessed is out of address space"
        if(loc > MEMORY_SIZE or loc < 0):

            # Error logs can be created (IO class can be used)
            print("Wrong memory location: ", loc," accessed : Exiting")
            exit()
        
        if(loc + 1 > len(self.__Memory)):
            print("Random location accessed where no data was stored, exiting")
            exit()
        assert loc+1 <= len(self.__Memory), "Random location accessed where no data was stored, exiting"
        return self.__Memory[loc]
    def writeAtLocation(self,loc,data, copyingCode): # Can write any data, No constraint on writing specific data type
        """! Setter for the memory.
        @param loc  Location that we want to set.
        @param data  Value that we want to set the location to.
        """
        assert loc > 10, "Wrong memory location: "+ str(loc)+" writing tried (writing to ROM)"
        assert loc <= MEMORY_SIZE, "Wrong memory location: "+ str(loc)+" writing tried (Above total size of memory)"
        if ((loc > CODE_STORAGE_LOCATION_ONE) and (loc <= CODE_STORAGE_LOCATION_END) and (copyingCode == False)):
            print("Cannot write to locations used for storing input code")
            exit()

        self.__Memory[loc] = data
    def printMemoryStatus(self):
        """! Print the status of the memory. 
        """
        for i in range (0, MEMORY_SIZE):
            print("Loc ", i, ": ", self.__Memory[i])
    def setProgramCounterTo(self, val, executing):
        """! Setter for the program counter.
        @param val Value to be loaded into the program counter.
        """
        RAMObjectGlobal.timeInstant += 1
        print("PC value set to :", val,"(Line number: ",val - CODE_STORAGE_LOCATION_ONE ,")")
        if executing == True:
            plt.scatter(val, RAMObjectGlobal.timeInstant)
        self.__programCounter = val
    def getProgramCounter(self):
        """! Getter for the program counter.
        @return Program counter value.
        """ 
        return self.__programCounter

        # First 10 locations are ROM location  
        # We can store all the data in memory 
        # RAM has setters and getters both
        # ROM has getters only
        # Two functions
        # Read and writeAtLocation
        #! Read can be common to ROM and RAM . But only RAM should beb able to write at any location
class RAM(Memory):
    """ The RAM child class handling RAM related operations """
    def __init__(self):
        """ The RAM child class initializer."""
        Memory.__init__(self)
        self.executionFile = "DUMMY"
        self.geneExecutionFile = False
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

    def setRegisterToValue(self, regString, val):
        """! Combined setter for all the register in the RAM.
        @param val  Value to be set to the register specified.
        @param regString  Register name passed as string.
        """
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
        """! Combined getter for all the register in the RAM.
        @param regString  Register name passed as string.
        @return  Present value of the register.
        """
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
        """! Setter for the accumulator.
        @param value  Value to be set to the accumulator.
]        """
        self.__A = value
    def addToAccumulator(self,value): 
        print("Value stored in Accumulator: ", self.__A)
        self.__A += value
    def getAccumulator(self): # Accumulator Getter
        return self.__A
    def multiplyToAccumulator(self,value): 
        """! Multiplies the value to the accumulator.
        @param value  Value to be multiplied with the accumulator.
]        """
        print("Value stored in Accumulator: ", self.__A)
        self.__A *= value
    def orToAccumulator(self,value): 
        """! ORs the value to the accumulator.
        @param value  Value to be ORed with the accumulator.
]        """
        print("Value stored in Accumulator: ", self.__A)
        self.__A |= value
    def andToAccumulator(self,value): 
        """! ANDs the value to the accumulator.
        @param value  Value to be ANDed with the accumulator.
]        """
        print("Value stored in Accumulator: ", self.__A)
        self.__A &= value    

    def divideToAccumulator(self,value): 
        """! Divides accumulator by value.
        @param value  Value to be divide the accumulator with.
]        """
        print("Value stored in Accumulator: ", self.__A)      
        try:
            self.__A /= value
            self.__A = int(self.__A)
        except Exception as e:
            print("Cannot execute division operation because of exception ", e)
            exceptionList.append("Cannot execute division operation because of exception "+str(e))
        else:
            quot = RAMObjectGlobal.getAccumulator()
            print("Executing DIVI command")
            print("Quotient of Accumulator reg and ", value, "is calculated to be :", quot)
            return quot
    def setRegA(self, value):
        self.__A = value
    def getRegA(self):
        return self.__A
    
class ALU(ABC): # This is an abstract class 

    """ The ALU base class for all the arithmetic and logical operations """
    
    def __init__(self):
        """ The ALU base class initializer."""
        print("ALU Object created")
        @abstractmethod
        def performOperation(self): # This is an abstract method
            pass
class Add(ALU): # All ADD ADA (Add to acc ) can create a single object 
    # this defines the type of operation
    """ The Add class.
        The addition operations taking place are : 
        1) Adding contents of two registers
        2) Adding content of a register to the accumulator 
        3) Adding contents of two registers and storing it in another register
    """

    def __init__(self, insString):
        """! The Add class initializer.
            @param insString The instruction containing the op code.
        """
        ALU.__init__(self)
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
        elif opcode == "ada":
            print("ADA class object created")
            print("executing ADA")
            self.opcode = "0001"
            self.numOperands = 1
            self.reg1 = insString.split()[1]  # String 
            self.reg2 = "ZERO"
            self.reg3 = "ZERO"
        elif opcode == "add2":
            print("ADD class object created")
            print("executing ADD2")
            self.opcode = "1100" # ! This needs to be removed since this is already hard coded
            self.numOperands = 3
            self.reg1 = insString.split()[1]
            self.reg2 = insString.split()[2] # String 
            self.reg3 = insString.split()[3]
        self.performOperation()    
    @dispatch(object, object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    def addition(self, reg1, reg2):

        """! The addition of contents of two registers
        @param reg1  The content in Register 1.
        @param reg2  The content in Register 2.
        @return  The sum of the contents of the two registers.
        """
        sum = reg1 + reg2
        RAMObjectGlobal.setAccumulator(sum)
        print("Executing ADD command")
        print("Sum of ", reg1, " and ", reg2, "Was calculated to be :", sum)
        print("Accumulator value after ADD command ", RAMObjectGlobal.getAccumulator())
        return sum
    @dispatch(object)
    def addition(self, reg1):
        """! The addition of contents of a register to accumulator
        @param reg1  The content in Register 1
        @return  The sum of the contents of the register and the accumulator
        """
        RAMObjectGlobal.addToAccumulator(reg1)
        sum = RAMObjectGlobal.getAccumulator()
        print("Executing ADA command")
        print("Sum of ", reg1, " and Accumulator reg", "Was calculated to be :", sum)
        print("Accumulator value after ADA command ", RAMObjectGlobal.getAccumulator())
        return sum
    @dispatch(object,object,object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    def addition(self, reg1, reg2,reg3):

        """! The addition of contents of two registers and storing it in another register
        @param reg1  The sum is stored in Register 1
        @param reg2  The content in Register 2
        @param reg3  The content in Register 3
        @return  The sum of the contents of the two registers (reg2 and reg3)
        """
        sum = reg2 + reg3 
        RAMObjectGlobal.setRegisterToValue(self.reg1,sum)
        print("Executing ADD2 command")
        print("Sum of ", reg2, " and ", reg3, "Was calculated to be :", sum)
        RAMObjectGlobal.printRegisterStatus()
        return sum     
    def performOperation(self):
        """The calling of the addition method based on the number of operands in the instruction"""
        
        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        reg3Val = getValueOfRegister(self.reg3)

        if self.numOperands == 1:
            sum = self.addition(reg1Val)
        elif self.numOperands == 2:
            sum = self.addition(reg1Val, reg2Val)
        elif self.numOperands == 3:
            sum = self.addition(reg1Val,reg2Val, reg3Val)    
        return sum
class Sub(ALU):
    """ The Sub class.
        The subtraction operations taking place are : 
        1) Subtraction between contents of two registers
        2) Subtraction of content of a register from the accumulator 
        3) Subtraction between contents of two registers and storing it in another register

    """
    def __init__(self, insString):

        """! The Add class initializer.
        @param insString  The instruction containing the op code
        """
        ALU.__init__(self)
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "sub":
            print("SUB class object created")
            self.opcode = "0000" # ! This needs to be removed since this is already hard coded
            self.numOperands = 2
            self.reg1 = insString.split()[1] # String 
            self.reg2 = insString.split()[2]
            self.reg3 = "ZERO"
        elif opcode == "suba":
            print("SUB class object created")
            self.opcode = "1101"
            self.numOperands = 1
            self.reg1 = insString.split()[1]  # String 
            self.reg2 = "ZERO"
            self.reg3 = "ZERO"
        elif opcode == "sub2":
            print(" SUB class object created")
            self.opcode = "11111" # ! This needs to be removed since this is already hard coded
            self.numOperands = 3
            self.reg1 = insString.split()[1]
            self.reg2 = insString.split()[2] # String 
            self.reg3 = insString.split()[3]
        self.performOperation()    
    @dispatch(object, object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    def subtraction(self, reg1, reg2):

        """! The subtraction between contents of two registers
        @param reg1  The content in Register 1
        @param reg2  The content in Register 2
        @return  The differnce of the contents of the two registers
        """
        difference = reg2 - reg1
        RAMObjectGlobal.setAccumulator(difference)
        print("Executing SUB command")
        print("Difference of ", reg1, " and ", reg2, "Was calculated to be :", difference)
        return difference
    @dispatch(object)
    def subtraction(self, reg1):
        """! The subtraction of content of a register from the accumulator 
        @param reg1  The content in Register 1
        @return  The differnce of the contents of the register and the accumulator
        """
        newreg1 = reg1*(-1)
        RAMObjectGlobal.addToAccumulator(newreg1)
        difference = RAMObjectGlobal.getAccumulator()
        print("Executing SUBA command")
        print("Difference of ", reg1, " and Accumulator reg", "Was calculated to be :", difference)
        RAMObjectGlobal.printRegisterStatus()
        return difference
    @dispatch(object, object,object)                                               # ! Polymorphism -> SUB and SUBA can use this(All the binary operations)
    def subtraction(self, reg1, reg2,reg3):
        
        """! The subtraction between contents of two registers and storing the difference value in another register
        @param reg1  The difference is stored in reg1
        @param reg2  The content in Register 2
        @param reg3  The content in Register 3
        @return  The difference of the contents of the two registers(reg2 and reg3)
        """
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
        """The calling of the subtraction method based on the number of operands in the instruction"""

        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        reg3Val = getValueOfRegister(self.reg3)

        if self.numOperands == 1:
            difference = self.subtraction(reg1Val)
        elif self.numOperands == 2:
            difference = self.subtraction(reg1Val, reg2Val)
        elif self.numOperands == 3:
            difference = self.subtraction(reg1Val,reg2Val, reg3Val)    
        return difference
RAMObjectGlobal = RAM()

class InstructionDecoder:
    """InstructionDecoder class to take instructions given by user through and validate them and then copying it to the memory."""
    def __init__(self ):
        self.temp = 0
    def parseFileDecodeInstructions(self, inputFile, executionFileName):
        RAMObjectGlobal.executionFile = executionFileName
        """Function to decode instruction given in the file by the user"""
        self.parseFileStoreToMemory(inputFile)
        print("Parsing file and validating")
        while RAMObjectGlobal.getProgramCounter() < MEMORY_SIZE:
            line = RAMObjectGlobal.getDataAtLocation(RAMObjectGlobal.getProgramCounter())
            
            RAMObjectGlobal.setProgramCounterTo((RAMObjectGlobal.getProgramCounter() + 1), False)
            if(line[0:2] == "//"): # ! Handles a comment
                continue
            if(line.split()[0].lower() == "hlt"):
                break
            flag = self.validateInstruction(line, RAMObjectGlobal.getProgramCounter() - 1)
            
        RAMObjectGlobal.resetProgramCounter()
        
        while RAMObjectGlobal.getProgramCounter() < CODE_STORAGE_LOCATION_END:

            line = RAMObjectGlobal.getDataAtLocation(RAMObjectGlobal.getProgramCounter())
            RAMObjectGlobal.setProgramCounterTo((RAMObjectGlobal.getProgramCounter() + 1),True)
            if(line[0:2] == "//"): # ! Handles a comment
                continue
            if((RAMObjectGlobal.getProgramCounter() - CODE_STORAGE_LOCATION_ONE) in exceptionLineNumberList):
                print("skipped : ", line)
                continue
            #self.validateInstruction(line, RAMObjectGlobal.getProgramCounter() - 1)
            instructionObject = self.createInstructionObject(line)
            instructionList.append(instructionObject) # Add the validate instruction functions here.
    def truncateTo16BitDecimal(self, number):
        binary = bin(number)
        truncatedBinaryNumber = binary[-16:]
        decimalNumber16Bit = int(truncatedBinaryNumber, 2)
        return decimalNumber16Bit
        

    def parseFileStoreToMemory(self, inputFile):
        """ function to copy code into the memory"""
        print("Started copying code into the memory")
        try:
            f = open(inputFile, 'r')
        except Exception as ef:
            print(ef)
        else:
             with open(inputFile, 'r') :
                lineNumber = CODE_STORAGE_LOCATION_ONE - 1
                for line in f:
                    lineNumber += 1
                    RAMObjectGlobal.writeAtLocation(lineNumber, line, True)
        finally:
            f.close()

    def createInstructionObject(self,instructionString):
        """Function to extract the opcode for the instruction and then call the respective function for the execution"""
        opcode = instructionString.split()[0]
        print("Opcode : ", opcode)
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
            subObject = Sub(instructionString) # Object once created by itself performs all the validation and execution
            instructionList.append(subObject)
        # if opcode.lower() == "str":
        if opcode.lower() == "ld":
            print( "LD instruction decode stage")
            ldObject = LD(instructionString) # Object once created by itself performs all the validation and execution
            instructionList.append(ldObject)
        if opcode.lower() == "str":
            print( "STR instruction decode stage")
            strObject = STR(instructionString) # Object once created by itself performs all the validation and execution
            instructionList.append(strObject)
        if opcode.lower() == "out":
            print("OUT instruction encountered")
            outObject = OUT(instructionString) # Object once created by itself performs all the validation and execution
            instructionList.append(outObject)
        if opcode.lower() == "mov":
            print("MOV instruction encountered")
            movObject = MOV(instructionString) # Object once created by itself performs all the validation and execution
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
        """To validate the instruction given by the user with the standard format """
        insName = instructionString.split()[0]
        if insName.lower() not in instruction_list:
            print("The command mentioned does not exist ,line number:" ,lineNumber - CODE_STORAGE_LOCATION_ONE + 1)
            exceptionList.append("The command mentioned does not exist ,line number:" + str(lineNumber - CODE_STORAGE_LOCATION_ONE + 1))
            exceptionLineNumberList.append(lineNumber - CODE_STORAGE_LOCATION_ONE + 1)
            return False
            #exit()
        instruction = instruction_list[insName.lower()]
        numOperands = instruction[0]
        opcode = instruction[1]
        operandTypes = instruction[2]
        isInsLenCorr = self.isInstructionLengthCorrect(instructionString, numOperands + 1)
        if isInsLenCorr == False:
            print("More/Less operands were expected, Line number : ", lineNumber - CODE_STORAGE_LOCATION_ONE + 1)
            exceptionList.append("More/Less operands were expected, Line number : "+ str(lineNumber - CODE_STORAGE_LOCATION_ONE + 1))
            exceptionLineNumberList.append(lineNumber - CODE_STORAGE_LOCATION_ONE + 1)
            return False
            
        print ("operandTypes : ", operandTypes)
        for i in range (0,numOperands): # Assuming there are only 2 operands at max for any operation (This can be expanded later)
            operand = instructionString.split()[i+1]
            if operandTypes.lower()[i] == "r":
                print("Checking if the register", operand," is valid or not")
                isRegVal = self.isRegisterValid(operand, lineNumber)
                if isRegVal == False:
                    return False
            if operandTypes.lower()[i] == "#":
                print("Checking if the #val is valid or not")
                isImmVal = self.isImmediateValid(operand, lineNumber)
                if isImmVal == False:
                    return False
        return True
    def isImmediateValid(self,inputString, lineNumber): # Does not allow floating point values
        """To check any immediate value entered by the user"""
        if inputString[0].lower() == "#":
            splitElement = inputString[1:]
            print("Value is ", splitElement)
            if splitElement.isdigit() == True:
                return True
            exceptionList("Immediate value can only be numerical value ,Line number :"+ str(lineNumber - CODE_STORAGE_LOCATION_ONE + 1))
            print("ERROR : Immediate value can only be numerical value ,Line number :", lineNumber - CODE_STORAGE_LOCATION_ONE + 1)
            return False
        else:
            exceptionList("ERROR : Immediate value token was expected : "+str(lineNumber- CODE_STORAGE_LOCATION_ONE))
            print("ERROR : Immediate value token was expected : ", lineNumber-CODE_STORAGE_LOCATION_ONE)
            return False
    def isInstructionLengthCorrect(self,instructionString, insLength):
        """To check the length of the instruction"""
        lenOfInstruction = len(instructionString.split())
        if lenOfInstruction == insLength:
            return True
        else:
            print("Length found : ", lenOfInstruction)
            return False
    
    def isRegisterValid(self,inputString, lineNumber): # This would return false if register does not exist OR it is not even a register
        """TAo check whether the register  entered by the user is valid or not"""
        # if inputString[0].lower() != "r" :
        if inputString not in register_list:
            exceptionList.append("Register was expected as an argument,line number :"+ str(lineNumber - CODE_STORAGE_LOCATION_ONE + 1))
            exceptionLineNumberList.append(lineNumber - CODE_STORAGE_LOCATION_ONE + 1)
            print("Register was expected")
            return False
        for reg in register_list:
            if reg == inputString.lower():
                return True
        exceptionList.append("Register number out of range ,Line number :"+ str(lineNumber - CODE_STORAGE_LOCATION_ONE + 1))
        exceptionLineNumberList.append(lineNumber - CODE_STORAGE_LOCATION_ONE + 1)
        print("Register number out of range ,Line number :", lineNumber - CODE_STORAGE_LOCATION_ONE + 1)
        return False
        

class LD(Memory):
    """Child class of memory to handle the load operation"""
    def __init__(self, insString):
        Memory.__init__(self)
        self.opcode = insString.split()[0]
        self.opcode = self.opcode.lower()
        self.reg = insString.split()[1]
        self.performAction()
        print("Value of the accumulator is : ", RAMObjectGlobal.getAccumulator())
    def performAction(self):
        memoryLocation = getValueOfRegister(self.reg) # this is the memory location
        RAMObjectGlobal.setAccumulator(RAMObjectGlobal.getDataAtLocation(memoryLocation))
    

class STR(Memory):
    """Child class of memory fot handling the store operation"""
    
    def __init__(self, insString):
        Memory.__init__(self)
        self.opcode = insString.split()[0]
        self.opcode = self.opcode.lower()
        self.reg = insString.split()[1]
        self.performAction()
        print("Value of the accumulator while performing STORE is : ", RAMObjectGlobal.getAccumulator())
    def performAction(self):
        memoryLocation = getValueOfRegister(self.reg) # this is the memory location
        RAMObjectGlobal.writeAtLocation(memoryLocation, RAMObjectGlobal.getAccumulator(), False)
        print("Memory status : ")
        RAMObjectGlobal.printMemoryStatus()
instructionDecoderGlobal = InstructionDecoder()
class MOV(RAM):
    """ child class of RAM to handle MOV instruction """
    def __init__(self, insString):
        self.opcode = insString.split()[0]
        self.opcode = self.opcode.lower()
        self.reg1 = insString.split()[1]
        self.reg2 = insString.split()[2]

        self.performAction()
    def performAction(self):
        """Moving data provided by user to a register"""
        if self.reg2 in register_list:
            reg2Val = getValueOfRegister(self.reg2)
            reg2Val = instructionDecoderGlobal.truncateTo16BitDecimal(reg2Val)
            RAMObjectGlobal.setRegisterToValue(self.reg1, reg2Val)
        elif(self.reg2[0] == "#"):
            print("Assigning the imm value")
            immVal = int(self.reg2[1:])
            print(self.reg2[1:])
            immVal = instructionDecoderGlobal.truncateTo16BitDecimal(immVal)
            RAMObjectGlobal.setRegisterToValue(self.reg1, immVal)
            RAMObjectGlobal.printRegisterStatus()
        else:
            print("Move statement second argument should either be #(immediate value) or R type")
            exceptionList("Move statement second argument should either be #(immediate value) or R type")
            exit()
class IO(ABC):
    """Parent class to perform the IO operations"""
    def __init__(self):
        self.__outFile = outputFile
    def toTerminal(self, x):
        print(x)
    def toOutput(self, x):
        print(x)
        if(x == "NEXTLINE"):
            self.__outFile.write("\n")
        else:
            self.__outFile.write(x)
    def performAction():
        pass

class OUT(IO):
    """Child class of IO to perform the output operation"""
    def __init__(self, insString):
        IO.__init__(self)
        self.opcode = insString.split()[0]
        self.opcode = self.opcode.lower()
        self.reg = insString.split()[1]
        self.performAction()
    def __writeToOutFile(self, string):
        self.toOutput(string),
    def __display(self,string):
        print(string)
    def performAction(self):
        """Printing the data to the optput file"""
        if(self.reg[0] == '"'):
            self.__writeToOutFile(str(self.reg[1:-1]))
        else:
            regVal = getValueOfRegister(self.reg)
            self.__display(regVal)
            self.__writeToOutFile(str(regVal))
        RAMObjectGlobal.printRegisterStatus()
        
    
class IN(IO):
    """Class to perform the Input operation"""
    def __init__(self, insString):
        IO.__init__(self)
        self.opcode = insString.split()[0]
        self.opcode = self.opcode.lower()
        self.port = insString.split()[1]
        self.performAction()
    def readFromPort(self, portFileName):
        """To read data form the  ports"""
        portFile = open(portFileName+".txt", "r")
        readValue = portFile.read()
        RAMObjectGlobal.setRegA(instructionDecoderGlobal.truncateTo16BitDecimal(int(readValue)))
        print("Value read from the port : ", readValue)
        print("Value set to reg A : ", RAMObjectGlobal.getRegA())

    def performAction(self):
        self.readFromPort(self.port)

class MUL(ALU): 
    """ The MUL class.
        The multiplication operations taking place are : 
        1) Multiplication of contents of two registers
        2) Multiplication of content of a register with the accumulator 
        
    """
    def __init__(self, insString):
        ALU.__init__(self)
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "mul":
            print("MUL class object created")
            self.opcode = "0111"
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
    @dispatch(object, object)                                               
    def multiplication(self, reg1, reg2):
        """! The multiplication of contents of two registers
        @param reg1  The content in Register 1
        @param reg2  The content in Register 2
        @return  The product value of the contents of the two registers
        """
        prod = reg1 * reg2
        RAMObjectGlobal.setAccumulator(prod)
        print("Executing MUL command")
        print("Product of ", reg1, " and ", reg2, "Was calculated to be :", prod)
        return prod
    @dispatch(object)
    def multiplication(self, reg1):
        """! The multiplication between contents of two registers
        @param reg1  The content in Register 1
        @return  The product value of the register content and the accumulator
        """
        RAMObjectGlobal.multiplyToAccumulator(reg1)
        prod = RAMObjectGlobal.getAccumulator()
        print("Executing MULI command")
        print("Product of ", reg1, " and Accumulator reg", "Was calculated to be :", prod)
        return prod
    def performOperation(self):
        
        """The calling of the multiplication method based on the number of operands in the instruction"""
        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        if self.numOperands == 1:
            prod = self.multiplication(reg1Val)
        else:
            prod = self.multiplication(reg1Val, reg2Val)
        
        return prod    

class OR(ALU): 
    """ The OR class.
        The logical OR operations taking place are : 
        1) OR operation between of contents of two registers
        2) OR operation between content of a register with the accumulator 
        
    """
    def __init__(self, insString):
        ALU.__init__(self)
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "or":
            print("OR class object created")
            self.opcode = "10001" 
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
    @dispatch(object, object)                                               
    def logicalor(self, reg1, reg2):
        """! The logical OR of contents of two registers
        @param reg1  The content in Register 1
        @param reg2  The content in Register 2
        @return  The value after logical OR between contents of the two registers
        """

        orout = reg1 | reg2
        RAMObjectGlobal.setAccumulator(orout)
        print("Executing OR command")
        print("OR of ", reg1, " and ", reg2, "Was calculated to be :", orout)
        return orout
    @dispatch(object)
    def logicalor(self, reg1):
        """! The logical OR of contents of two registers
        @param reg1  The content in Register 1
        @return  The value after logical OR between content of the register and accumulator
        """
        RAMObjectGlobal.orToAccumulator(reg1)
        orout = RAMObjectGlobal.getAccumulator()
        print("Executing ORA command")
        print("OR of ", reg1, " and Accumulator reg", "Was calculated to be :", orout)
        return orout
    def performOperation(self):
        """The calling of the logicalor method based on the number of operands in the instruction"""
        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        if self.numOperands == 1:
            orout = self.logicalor(reg1Val)
        else:
            orout = self.logicalor(reg1Val, reg2Val)
        return orout   

class AND(ALU): 
    def __init__(self, insString):
        ALU.__init__(self)
        # self.opcode = "0000"
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "and":
            print("AND class object created")
            self.opcode = "10010" 
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
    @dispatch(object, object)                                               
    def logicaland(self, reg1, reg2):
        """! The logical AND of contents of two registers
        @param reg1  The content in Register 1
        @param reg2  The content in Register 2
        @return  The value after logical AND between contents of the two registers
        """
        
        andout = reg1 & reg2
        RAMObjectGlobal.setAccumulator(andout)
        print("Executing AND command")
        print("AND of ", reg1, " and ", reg2, "Was calculated to be :", andout)
        return andout
    @dispatch(object)
    def logicaland(self, reg1):
        """! The logical AND of contents of two registers
        @param reg1  The content in Register 1
        @return  The value after logical AND between content of the register and accumulator
        """
        RAMObjectGlobal.andToAccumulator(reg1)
        andout = RAMObjectGlobal.getAccumulator()
        print("Executing ANDA command")
        print("AND of ", reg1, " and Accumulator reg", "Was calculated to be :", andout)
        return andout
    def performOperation(self):
        """The calling of the logicaland method based on the number of operands in the instruction"""
        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        if self.numOperands == 1:
            andout = self.logicaland(reg1Val)
        else:
            andout = self.logicaland(reg1Val, reg2Val)
        return andout      

class NOT(ALU): 
    """ The NOT class.
        The logical NOT of a number gives in the 2's complement form 
    """
    def __init__(self, insString):
        ALU.__init__(self)
        # self.opcode = "0000"
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "not":
            print("NOT class object created")
            self.opcode = "10101"
            self.numOperands = 1
            self.reg1 = insString.split()[1] # String 
            #self.reg2 = "ONE"
        
        self.performOperation()
    
    @dispatch(object)
    def logicalnot(self, reg1):
        """! The logical NOT of contents of a register
        @param reg1  The content in Register 1
        @return  The 2's complement of the register content
        """
        notout = ~reg1 
        RAMObjectGlobal.setAccumulator(notout)
        print("Executing NOT command")
        print("NOT of ", reg1,"Was calculated to be :", notout)
        return notout
    
    def performOperation(self):
        """The calling of the logicalnot method """
        reg1Val = getValueOfRegister(self.reg1)
        notout = self.logicalnot(reg1Val)
        return notout      
      
class DIV(ALU): 
    """ The DIV class.
        The division operations taking place are : 
        1) Division of contents of two registers
        2) Division of content of a register with the accumulator 
        
    """ 
     
    def __init__(self, insString):
        ALU.__init__(self)
        opcode = insString.split()[0]
        opcode = opcode.lower()
        if opcode == "div":
            print("DIV class object created")
            self.opcode = "1001"
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
    @dispatch(object, object)                                               
    def division(self, reg1, reg2):
        """! The division of contents of two registers
        @param reg1  The content in Register 1
        @param reg2  The content in Register 2
        @return  The division value of the contents of the two registers
        """
        try:
            quot = reg1 / reg2
            quot = int(quot)
        except Exception as ex:
            print ("Cannot execute the division function because of exception:", ex)
            exceptionList.append("Cannot execute division operation because of exception :"+str(ex))
        else:
            RAMObjectGlobal.setAccumulator(quot)
            print("Executing DIV command")
            print("Product of ", reg1, " and ", reg2, "Was calculated to be :", quot)
            return quot
    @dispatch(object)
    def division(self, reg1):
        """! The division between contents of two registers
        @param reg1  The content in Register 1
        @return  The division value of the register content and the accumulator
        """
        
        RAMObjectGlobal.divideToAccumulator(reg1)
    def performOperation(self):
        """The calling of the division method based on the number of operands in the instruction"""
        reg1Val = getValueOfRegister(self.reg1)
        reg2Val = getValueOfRegister(self.reg2)
        if self.numOperands == 1:
            quot = self.division(reg1Val)
        else:
            quot = self.division(reg1Val, reg2Val)
        return quot
class HLT():
    """ The HLT class.
        The halt operations takes place, i.e., the execution of the program stops. 
        """
    def __init__(self, insString):
        self.opcode = insString.split()[0]
        self.performOperation()
    def performOperation(self):
        print ("Program Halted")
        plt.xlabel("Location of storage of instruction in memory")
        plt.ylabel("Time")
        
        plt.savefig(RAMObjectGlobal.executionFile)
        self.printExceptions()
        exit(0)
    def printExceptions(self):
        if(len(exceptionList) != 0):
            print("Exceptions that were handled and program was executed:- ")
            ecount = 0
            for ex in exceptionList:
                ecount += 1
                print("ERROR ", ecount , ": ", ex)

class executionControl():
    """ The Execution Control class.
        1) Uses the jump statements, JZ(Jump if Zero) and JNZ(Jump if not Zero)
        
        """
    def __init__(self, insString):
        self.opcode = insString.split()[0]
        self.opcode = self.opcode.lower()
        self.reg1 = insString.split()[1]
        self.reg2 = insString.split()[2]
        self.reg1Val = getValueOfRegister(self.reg1)
        self.reg2val = getValueOfRegister(self.reg2)
        self.performOperation()
    def jumpTo(self, location):
        """! Sets the program counter to the passed location value
        @param location The location of the register"""
        print("PC to be set to :", location)
        RAMObjectGlobal.setProgramCounterTo(location ,True)
    def performOperation(self):
        """The calling of the jumpTo method based on the opcode in the instruction
        1) If the opcode is JZ, then, jumpTo method is called when register value is 0
        2) If the opcode is JNZ, then, jumpTo method is called when register value is not 0"""
        if self.opcode.lower() == "jz":
            print("Execution of JZ instruction starts")
            if self.reg1Val ==0:
                print("reg value zero satisfied")
                locationToJumpTo = self.reg2val
                self.jumpTo(locationToJumpTo)
        if self.opcode.lower() == "jnz":
            print("Execution of JNZ instruction starts")
            if self.reg1Val != 0:
                print("reg value non zero satisfied")
                locationToJumpTo = self.reg2val
                self.jumpTo(locationToJumpTo + CODE_STORAGE_LOCATION_ONE - 1)
        

def getValueOfRegister(regString): 
    # We will be keeping track of the register vaues separately
    """!For the given register name, the value of the register is returned.
    @param regString Name of the Register
    @return registerValue Value of the register."""
    registerValue = RAMObjectGlobal.returnRegisterValue(regString)
    return registerValue
def main(inputFileName):
    try:
        instructionDecoderGlobal.parseFileDecodeInstructions(inputFileName, executionFileName)
    except Exception as eef:
        print(eef)
if __name__== "__main__":
    main(inputFileName)