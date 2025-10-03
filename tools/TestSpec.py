import os
import re
import importlib
import difflib
import termcolor
from SpecDir import * 

class TestSpec(SpecDir):

  def __init__(this, path, template):
    this.dirName    = os.path.basename(path)
    this.num = TestSpec.numFromDirName(this.dirName)
    super().__init__(path, template)

  @staticmethod
  def numFromDirName(dirName):
    
    # handle 0 <= num <= 9 
    num = dirName[1]

    # handle 10 <= num <= 99
    if (len(dirName) == 3):
      num = dirName[1] + dirName[2] 

    return num

  def getNum(this):
    return this.num

  def strFromTemplateStr(this, str): 
    ignoreRe = re.compile(".*&&&")
    if (ignoreRe.match(str)):
      str = str.replace("&&&", "")
    else:
      str = re.sub("tNum", this.num, str) 
    return str


  """
  def getInput(this):
    return this.readFile("in")
    
  def expectedOutput(this):
    output = []
    if (os.path.isfile(os.path.join(this.path, "out"))):
      output = this.readFile("out")
    return output

  def setExpectedOutput(this, lines):
    this.writeFile("out", lines)
    
  def printInput(this):
    inputStr = ""
    if (len(this.getInput()) > 0):
      inputStr += "\n"
      inputStr += "Input:\n"
      for line in this.getInput():
        inputStr += line + "\n"
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
    

  def run(this, pNum, pName, verbose=True):

    # run test
    print("Running problem %1s - %-15s: test %1s" % (pNum, pName, this.num), end="")
    g.startTest(this.getInput())
    importlib.invalidate_caches()
    module = importlib.import_module("labs.labenv." + this.pyFileName.split(".")[0])
    this.func = vars(module)["p" + pNum + "Test" + this.num]
    this.func()
    actualOutput = g.endTest()

    # generate output file if it doesn't exist
    if len(this.expectedOutput()) == 0:
      this.setExpectedOutput(actualOutput)
    
    # check result
    diffList = this.outputDiff(this.expectedOutput(), actualOutput)
    
    modifiedEOutput = this.expectedOutput()
    modifiedAOutput = actualOutput
    
    #if (diffList[0] == "- # OUTPUT CONTAINS:\n"):
    #  modifiedAOutput = this.outputForContainsMatch(diffList)
    #  modifiedEOutput.pop(0)  # throw away "- # OUTPUT CONTAINS:"

    if modifiedEOutput == modifiedAOutput:  # == compares the lists
      tResult = "Passed"
    else:
      tResult = "FAILED"

    
    # print result
    if tResult == "Passed":
      cTResult = termcolor.colored('Passed', 'green', attrs=['bold'])
      print("  " + cTResult)
    else:
      cTResult = termcolor.colored('FAILED', 'red', attrs=['bold'])
      print("  " + cTResult)
      if (verbose):
        print(this.getTestResultDetails(modifiedEOutput, modifiedAOutput))

    return(tResult)

  """

# end class Test
