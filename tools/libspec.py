import os
import shutil
import re
import importlib
from tools.LabTestGasket import *
from termcolor import colored
import difflib
import filecmp

class Directory:
  
  def __init__(this, path, template):
    this.path               = path
    this.dirName            = os.path.basename(this.path)
    if (template == "new"):
      this.template = None
      this.makeNewDir()
    else:
      this.template = template
    #this.copyTemplate()
    this.files              = {}
    this.pyHeaderFileName   = "header.py"
    this.javaHeaderFileName = "header.java"
    this.pyFooterFileName   = "footer.py"
    this.javaFooterFileName = "footer.java"
    this.pyFileName         = this.readPyFileName()
    this.readFileFragments()

  def makeNewDir(this):
    if os.path.exists(this.path):
      shutil.rmtree(this.path)
    os.mkdir(this.path)


  def readPyFileName(this):
    for name in os.listdir(this.path):
      if name.split(".")[-1] == "py":
        return name

  @staticmethod
  def printFiles(files):
    for filename in files:
      print("file:", filename)
      for line in files[filename]:
        print(line)
      print()
      
  def getFiles(this):
    return this.files
    
  def addHeaderToFileFragments(this, fragments):
    pyHeader   = this.pyHeaderFileName in os.listdir(this.path) 
    pyFooter   = this.pyFooterFileName in os.listdir(this.path) 
    javaHeader = this.javaHeaderFileName in os.listdir(this.path) 
    javaFooter = this.javaFooterFileName in os.listdir(this.path) 

    if pyHeader: 
      pyHeaderFilePath = os.path.join(this.path, this.pyHeaderFileName)
      pyHeaderFile = open(pyHeaderFilePath)
      pyHeaderLines = pyHeaderFile.readlines()
      pyHeaderFile.close()
    
    if pyFooter: 
      pyFooterFilePath = os.path.join(this.path, this.pyFooterFileName)
      pyFooterFile = open(pyFooterFilePath)
      pyFooterLines = pyFooterFile.readlines()
      pyFooterFile.close()
    
    if javaHeader:
      javaHeaderFilePath = os.path.join(this.path, this.javaHeaderFileName)
      javaHeaderFile = open(javaHeaderFilePath)
      javaHeaderLines = javaHeaderFile.readlines()
      javaHeaderFile.close()

    if javaFooter:
      javaFooterFilePath = os.path.join(this.path, this.javaFooterFileName)
      javaFooterFile = open(javaFooterFilePath)
      javaFooterLines = javaFooterFile.readlines()
      javaFooterFile.close()


      for name in fragments:
        if (name.split(".").pop() == "py"):
          fragments[name] = pyHeaderLines + fragments[name] + pyFooterLines 
        elif (name.split(".").pop() == "java"):
          fragments[name] = javaHeaderLines + fragments[name] + javaFooterLines 

    return fragments

  def mergeFileFragments(this, fragments):
    for filename in fragments:
      newFileName = this.strFromTemplateStr(filename)
      if (this.files.get(newFileName) == None):
        this.files[newFileName] = fragments[filename]
      else:
        this.files[newFileName] = this.files[newFileName] + fragments[filename]
      this.files[newFileName] = this.fileFromTemplateFile(this.files[newFileName])
      
  def getFileFragments(this):
    this.readFileFragments()
    return this.files

  def getSubDirFileFragments(this, subDirName):
    subDirPath = os.path.join(this.path, subDirName)
    if os.path.isdir(subDirPath):
      subDir = Directory(subDirPath, None)
      #fragments = subDir.getFileFragments()
      fragments = subDir.getFiles()
    else:
      fragments = {}
    return fragments

  def makeMDCodeSection(this, lines):
    newLines = []
    for line in lines:
      newLines.append("\t" + line)
    return newLines 

  def strFromFragmentStr(this, str):
    match = re.search("<<file:([^>]+)>>", str)
    if (match != None):
      relativePath = match.group(1)
      path = os.path.join(this.path, relativePath)
      if (not os.path.exists(path)):
        return str
      file = open(path)
      lines = file.readlines()
      file.close()
      filestr = "".join(this.makeMDCodeSection(lines))
      str = re.sub("<<file:[^>]+>>", filestr, str) 
    return str
      
  def readFileFragments(this):
    for filename in this.fileFragmentNames():
      newFileName = this.strFromTemplateStr(filename)
      this.files[newFileName] = this.fileFromFragmentFile( this.fileFromTemplateFile(this.readFile(filename)))


  def renameInFile(this):
    (rest, tName) = os.path.split(this.path)
    (rest, testsdir) = os.path.split(rest)
    (rest, pName) = os.path.split(rest)
    newfilename = pName+"_"+tName+"_in.txt"
    oldFilePath = os.path.join(this.path, "in")
    newFilePath = os.path.join(this.path, newfilename)
    os.rename(oldFilePath, newFilePath)
    return(newfilename)

  def fileFragmentNames(this):
    ffNames = []
    for filename in this.fileNames():

      # UPGRADE old lab specifications
      if (filename == "in"):
        filename = this.renameInFile()

      fileExtension = filename.split(".").pop()
      if (((fileExtension == "py")   or 
          (fileExtension == "java") or 
          (fileExtension == "txt")  or 
          (fileExtension == "md")     )         and
          (filename != this.pyHeaderFileName)   and 
          (filename != this.javaHeaderFileName) and 
          (filename != this.pyFooterFileName)   and 
          (filename != this.javaFooterFileName)    ):
        ffNames.append(filename)
    return ffNames
      
  def dirNames(this):
    dirNames = []
    for name in os.listdir(this.path):
      if (os.path.isdir(os.path.join(this.path, name))):
        dirNames.append(name)
    dirNames.sort()
    return dirNames

  def readFile(this, filename):
    fileObj = open(os.path.join(this.path, filename))
    return fileObj.readlines()

  def writeFile(this, filename, file, forceWrite = False):

    backupDir = os.path.join(this.path, ".backup")
    filePath  = os.path.join(this.path, filename)
    backupFilePath = os.path.join(backupDir, filename)
    
    # make .backup dir if it doesn't exist
    if not os.path.isdir(backupDir):
      os.mkdir(backupDir)

    # make backup file if it doesn't exist
    if not os.path.isfile(backupFilePath):
      backupFileObj = open(backupFilePath, "w")
      backupFileObj.writelines(file)
      backupFileObj.close()

    # if file doesn't exit, make file and backup file 
    if not os.path.isfile(filePath):
      fileObj = open(filePath, "w")
      fileObj.writelines(file)
      fileObj.close() 
      backupFileObj = open(backupFilePath, "w")
      backupFileObj.writelines(file)
      backupFileObj.close()

    # compare file and backup file
    fileObj = open(filePath)
    fileLines = fileObj.readlines()
    fileObj.close()
    backupFileObj = open(backupFilePath) 
    backupFileLines = backupFileObj.readlines()
    backupFileObj.close()
    filesMatch = filecmp.cmp(filePath, backupFilePath, shallow=False)

    # if no difference, write new file and new backup file
    if (filesMatch or forceWrite):
      fileObj = open(filePath, "w")
      fileObj.writelines(file)
      fileObj.close() 
    if (filesMatch and not forceWrite):
      backupFileObj = open(backupFilePath, "w")
      backupFileObj.writelines(file)
      backupFileObj.close()

  def writeFiles(this, dictionary, forceWrite = False):
    for filename in dictionary:
      this.writeFile(filename, dictionary[filename], forceWrite)
  
  def fileNames(this):
    fileNames = []
    for name in os.listdir(this.path):
      if (os.path.isfile(os.path.join(this.path, name))):
        fileNames.append(name)
    fileNames.sort()
    return fileNames 

  def fileFromFragmentFile(this, fragmentFile):
    file = []
    for line in fragmentFile:
      str = this.strFromFragmentStr(line) 
      file.append(str)
    return file
    
  def fileFromTemplateFile(this, templateFile):
    file = []
    for line in templateFile:
      str = this.strFromTemplateStr(line) 
      file.append(str)
    return file
  
  def strFromTemplateStr(this, name): 
    return name 

  def isPyFileName(this, filename):
    result = True
    parts = filename.split(".") 
    if len(parts) < 2:
      result = False 
    elif parts[1] != "py":
      result =  False 

    return result
    
  def copyTemplate(this):

    if (this.template == None):
      return
      
    # make directories
    for dirName in this.template.dirNames():
      dirName = this.strFromTemplateStr(dirName)
      if not (dirName in this.dirNames()): 
        os.mkdir(os.path.join(this.path, dirName))

    # copy files
    for templateFileName in this.template.fileNames():
      newFileName = this.strFromTemplateStr(templateFileName)
      pyFileName = this.readPyFileName()
      if (not this.isPyFileName(newFileName) or
          (pyFileName == None)               or
          (pyFileName == newFileName)          ):
        templateFile = this.template.readFile(templateFileName)
        newFile = this.fileFromTemplateFile(templateFile)
        this.writeFile(newFileName, newFile)

  @staticmethod
  def filterFile(file, buildType):
      newFile = []
      filtering = False
      for line in file:
        if buildType.filterStart(line):
          filtering = True
        if filtering == False:
          newFile.append(line)  
        if buildType.filterStop(line):
          filtering = False
      return newFile

  @staticmethod
  def filterFiles(files, buildType):
    newFiles = {}
    for filename in files:
      if filename == "header.py":
        continue;
      newFile = Directory.filterFile(files[filename], buildType)
      newFiles[filename] = newFile
    return newFiles
        
# end class Directory

class Test(Directory):

  def __init__(this, path, template):
    this.dirName    = os.path.basename(path)
    this.num = Test.numFromDirName(this.dirName)
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
    str = re.sub("tNum", this.num, str) 
    return str

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
      cTResult = colored('Passed', 'green', attrs=['bold'])
      print("  " + cTResult)
    else:
      cTResult = colored('FAILED', 'red', attrs=['bold'])
      print("  " + cTResult)
      if (verbose):
        print(this.getTestResultDetails(modifiedEOutput, modifiedAOutput))

    return(tResult)

# end class Test

class Problem(Directory):

  def __init__(this, path, template):
    
    this.dirName    = os.path.basename(path)
    this.num        = Problem.numFromDirName(this.dirName)
    this.name       = Problem.nameFromDirName(this.dirName)
    
    super().__init__(path, template)
    
    this.testsPath = os.path.join(this.path, "tests")
    
    this.tests     = Tests(this.testsPath, this.testsTemplate()) 
    this.mergeChildrenFileFragments()

  def removeSolution(this, buildType):
    files = {}
    filename = this.readPyFileName()
    fileObj = open(os.path.join(this.path, filename))
    files[filename] = fileObj.readlines()
    filteredFiles = Directory.filterFiles(files, buildType)
    this.writeFiles(filteredFiles, forceWrite = True)
    
  def strFromTemplateStr(this, str): 
    str = re.sub("pNum", this.num, str) 
    str = re.sub("pName", this.name, str) 
    return str
  
  def mergeChildrenFileFragments(this):
    this.mergeFileFragments(this.getSubDirFileFragments("headers"))
    #this.mergeFileFragments(this.tests.getFileFragments())
    this.mergeFileFragments(this.tests.getFiles())
    this.mergeFileFragments(this.getSubDirFileFragments("footers"))
    #this.files = this.addHeaderToFileFragments(this.files)
    
  def testsTemplate(this):
    if this.template == None:
      return None
    else:
      return this.template.getTests()

  @staticmethod
  def nameFromDirName(dirName):
    return dirName.split("_").pop()
    
  @staticmethod
  def numFromDirName(dirName):

    pNumStr = dirName.split("_").pop(0)
    num = pNumStr[1:len(pNumStr)] 
  
    return num 
    
  def getName(this):
    return this.name

  def getNum(this):
    return this.num
    
  def getTests(this):
    return this.tests

  def run(this, tNum):
    tResult = None
    if tNum == None:
      print()
      print('PROBLEM', this.num, ":", this.name) 
      print()
      importlib.invalidate_caches()
      module = importlib.import_module("labs." + this.pyFileName.split(".")[0])
      this.func = vars(module)[this.dirName]
      this.func()
    else:
      tResult = this.tests.getTest(tNum).run(this.num, this.name)
      
    return tResult


  def runTests(this, verbose):
    tResult = this.tests.run(this.num, this.name, verbose)
    return tResult
    
# end class Problem 

class Tests(Directory):

  def __init__(this, path, template):
    
    super().__init__(path, template)
    
    this.tests = {}  
    this.readTests()
    this.mergeChildrenFileFragments()
    

  def mergeChildrenFileFragments(this):
    this.mergeFileFragments(this.getSubDirFileFragments("headers"))
    for testDirName in this.tests:
      #fragments = this.tests[testDirName].getFileFragments()
      fragments = this.tests[testDirName].getFiles()
      this.mergeFileFragments(fragments)
    this.mergeFileFragments(this.getSubDirFileFragments("footers"))
    #this.files = this.addHeaderToFileFragments(this.files)
    
  @staticmethod
  def isTestDir(dirName):
    result = True
    if (dirName[0] != "t"):
      result = False
    if (len(dirName) != 1 and len(dirName) !=2):
      result = False
    return result
    
  def testDirNames(this):
    dirs = []
    for dirName in this.dirNames():
      if (Tests.isTestDir(dirName)):
        dirs.append(dirName)
    return dirs
    
  def testTemplate(this, dirName):
    if this.template == None:
      return None
    else:
      return this.template.getTest(Test.numFromDirName(dirName))
      
  def readTests(this):
    testDirs = this.testDirNames()
    for testDir in testDirs:
      test = Test(os.path.join(this.path, testDir), this.testTemplate(testDir))
      this.tests[test.getNum()] = test 
      
  def getNums(this):
    return this.tests.keys()

  def testsList(this):
    testsList = []
    for num in this.tests.keys():
      testsList.append(this.getTest(num))
    return testsList
      
  def getTest(this, num):
    return this.tests.get(num)

    
  def run(this, pNum, pName, verbose):
    combinedResult = "Passed"
    for test in this.testsList():
      tResult = test.run(pNum, pName, verbose)
      if (tResult == "FAILED"):
        combinedResult = "FAILED"
    return tResult    
    
# end class Tests

class Problems(Directory):

  def __init__(this, path):
    super().__init__(path, None)
    this.problems = {}
    this.readProblems()
    this.mergeChildrenFileFragments()

  def removeSolutions(this, buildType):
    for problemName in this.problems:
      this.problems[problemName].removeSolution(buildType)
    
  def mergeChildrenFileFragments(this):
    this.mergeFileFragments(this.getSubDirFileFragments("headers"))
    for problemName in this.problems:
      #fragments = this.problems[problemName].getFileFragments()
      fragments = this.problems[problemName].getFiles()
      this.mergeFileFragments(fragments)
    this.mergeFileFragments(this.getSubDirFileFragments("footers"))
    #this.files = this.addHeaderToFileFragments(this.files)

  @staticmethod
  def isProblemDir(name):
    result = True
    #if (name == "ppNum_pName"):
    #  result = False
    if (len(name.split("_")) != 2):
      result = False
    if (name[0] != "p"):
      result = False
    return result

    
  def problemDirNames(this):
    dirNames = []
    for dirName in this.dirNames():
      if (Problems.isProblemDir(dirName)):
        dirNames.append(dirName)
    return dirNames
    
  def readProblems(this):
    #this.problems["Num"] = Problem(os.path.join(this.path, "ppNum_pName"), None)
    for pDirName in this.problemDirNames():
      #problem = Problem(os.path.join(this.path, pDirName), this.getProblem("Num"))
      problem = Problem(os.path.join(this.path, pDirName), None)
      this.problems[problem.getNum()] = problem 
    #this.problems.pop("Num")
    
  def getNums(this):
    return this.problems.keys()

  def problemsList(this):
    problems = []
    for num in this.problems.keys():
      problems.append(this.getProblem(num))
    return problems
      
  def getProblem(this, num):
    return this.problems.get(num)
    
  def runAllTests(this):
    print("Running tests...")
    result = "Passed" 
    verbose = True
    for problem in this.problemsList():
      tResult = problem.runTests(verbose)
      if tResult == "FAILED":
        result = "FAILED" 
        verbose = False
    return result
# end class Problems

class BuildType:

  def __init__(this, type):
    this.type = type 

  def getType(this):
    return this.type
    
  def filterStart(this, line):
    if this.type == "SOLUTION":
      if line.strip() == "# TEMPLATE ONLY - START:":
        return True
    else:
      if line.strip() == "# SOLUTION ONLY - START:":
        return True
    return False

  def filterStop(this, line):
    if this.type == "SOLUTION":
      if line.strip() == "# TEMPLATE ONLY - END:":
        return True
    else:
      if line.strip() == "# SOLUTION ONLY - END:":
        return True
    return False

# end class BuildType