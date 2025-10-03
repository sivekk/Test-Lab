import os
import re
import difflib
from Java import *
from Python import *
import termcolor

class Test:

    def __init__(this, path, compiledPath):

        this.path     = path
        this.fileName = os.path.basename(this.path)
        this.compiledPath = compiledPath 

        baseFileName = this.fileName.split(".").pop(0)  # remove extension
        (this.pNum, this.pName, this.tNum) = baseFileName.split("_")
        this.pNum = this.pNum.strip("p")
        this.tNum = this.tNum.strip("t")

        dirName = os.path.dirname(this.path)
        this.inFilePath = os.path.join(dirName, baseFileName + "_in.txt")

        this.outFilePath = os.path.join(dirName, baseFileName + "_out.txt")
        this.eOutFilePath = os.path.join(dirName, baseFileName + "_eout.txt")

    def __repr__(this):
        return "Problem " + this.pNum + " - " + this.pName + " : Test " + this.tNum 

    def getInputFile(this):
        fObj = None
        if os.path.isfile(this.inFilePath):
            fObj = open(this.inFilePath)
        return fObj 

    def getInput(this):
        lines = []
        fObj = this.getInputFile()
        if fObj:
            lines = fObj.readlines()
        return lines

    def getEOutFileName(this):
        return os.path.basename(this.eOutFilePath)

    def getExpectedOutput(this):
        #output = []
        output = None 
        if (os.path.isfile(this.eOutFilePath)):
            fObj = open(this.eOutFilePath)
            output = fObj.readlines()
        return output

    def setExpectedOutput(this, lines):
        fObj = open(this.eOutFilePath, "w")
        fObj.writelines(lines)
        fObj.close()

    def printInput(this):
        inputStr = ""
        if (len(this.getInput()) > 0):
            inputStr += "\n"
            inputStr += "Input:\n"
            for line in this.getInput():
                inputStr += line
        return inputStr
    
    def printExpectedOutput(this, expectedOutput):
        outputStr = ""
        outputStr += "Expected Output:\n"
        for line in expectedOutput:
            outputStr += line
        return outputStr
    
    def printActualOutput(this, actualOutput):
        outputStr = ""
        outputStr += "Actual Output:\n"
        for line in actualOutput:
            outputStr += line
        return outputStr

    def outputDiff(this, expectedOutput, actualOutput):
        return list(difflib.Differ().compare(expectedOutput, actualOutput))
    
    def printOutputDiff(this, expectedOutput, actualOutput):
        outputStr = ""
        outputStr += "Difference:\n"
        tDiff = this.outputDiff(expectedOutput, actualOutput) 
        for line in tDiff:
            outputStr += line
        return outputStr

    def outputDiff(this, expectedOutput, actualOutput):
        return list(difflib.Differ().compare(expectedOutput, actualOutput))
    
    def printOutputDiff(this, expectedOutput, actualOutput):
        outputStr = ""
        outputStr += "Difference:\n"
        tDiff = this.outputDiff(expectedOutput, actualOutput) 
        for line in tDiff:
            outputStr += line
        return outputStr
  
    def getTestResultDetails(this, expectedOutput, actualOutput):

        resultDetails = ""
        
        resultDetails += this.printInput()
        resultDetails += "\n"
        resultDetails += this.printExpectedOutput(expectedOutput)
        resultDetails += "\n"
        resultDetails += this.printActualOutput(actualOutput)    
        resultDetails += "\n"
        resultDetails += this.printOutputDiff(expectedOutput, actualOutput)
        resultDetails += "\n"

        return resultDetails

    def outputForContainsMatch(this, diffList):

        diffList.pop(0)  # get rid of "- # OUTPUT CONTAINS:"
        output = []

        for i in range(len(diffList)):
            line = diffList[i]

        ## this is broken
        # keep lines that dont start with + or -
        matchPlus  = re.search("\+ ", line)
        matchMinus = re.search("\- ", line)
        if ((matchPlus == None) and (matchMinus == None)):
            # remove initial 2 spaces
            line = line[2:]
            output.append(line)

        return output
    
    def run(this, capture=False, verbose=True):

        if verbose:
            print(this, end="")

        inFileObj = this.getInputFile()

        if (Java.isJavaFile(this.path)):
            className = Java.classNameFromFileName(this.fileName)
            result = Java.run(this.compiledPath, className, capture, inFileObj)
        elif (Python.isPythonFile(this.path)):
            filePath = os.path.join(this.compiledPath, this.fileName)
            result = Python.run(filePath, capture, inFileObj)

        if not capture:
            return

        actualOutput = [] 
        if result == None:
            actualOutput = ["ERROR:  test failed to build or run"]
        elif result.stderr:
            actualOutput.extend(result.stderr.splitlines(keepends=True))
        elif result.stdout:
            actualOutput.extend(result.stdout.splitlines(keepends=True))

        # generate output file if it doesn't exist
        #if len(this.getExpectedOutput()) == 0:
        if this.getExpectedOutput() == None:
            this.setExpectedOutput(actualOutput)
        
        # check result
        diffList = this.outputDiff(this.getExpectedOutput(), actualOutput)

        modifiedEOutput = this.getExpectedOutput()
        modifiedAOutput = actualOutput

        #if (diffList[0] == "- # OUTPUT CONTAINS:\n"):
        #  modifiedAOutput = this.outputForContainsMatch(diffList)
        #  modifiedEOutput.pop(0)  # throw away "- # OUTPUT CONTAINS:"
        
        if modifiedEOutput == modifiedAOutput:  # == compares the lists
            tResult = "Passed"
        else:
            tResult = "FAILED"

        # print result
        if verbose:
            if tResult == "Passed":
                cTResult = termcolor.colored('Passed', 'green', attrs=['bold'])
                print("  " + cTResult)

                # adding this for testing
                #print(this.getTestResultDetails(modifiedEOutput, modifiedAOutput))

            else:
                cTResult = termcolor.colored('FAILED', 'red', attrs=['bold'])
                print("  " + cTResult)
                if (verbose):
                    print(this.getTestResultDetails(modifiedEOutput, modifiedAOutput))

        return(tResult)