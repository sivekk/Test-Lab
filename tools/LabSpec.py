import os
import ProblemSpec
from SpecDir import * 

class LabSpec(SpecDir):

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
      if (LabSpec.isProblemDir(dirName)):
        dirNames.append(dirName)
    return dirNames
    
  def readProblems(this):
    #this.problems["Num"] = Problem(os.path.join(this.path, "ppNum_pName"), None)
    for pDirName in this.problemDirNames():
      #problem = Problem(os.path.join(this.path, pDirName), this.getProblem("Num"))
      problem = ProblemSpec.ProblemSpec(os.path.join(this.path, pDirName), None)
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

  def setExpectedOutputs(this, eOutputs):
    for name in eOutputs:
      (pNumStr, pName, testDirName, rest) = name.split("_")
      problemDirName = pNumStr + "_" + pName
      outFileName = "ppNum_pName_ttNum_eout.txt"
      eOutFilePath = os.path.join(this.path, problemDirName, "tests", testDirName, outFileName)
      fObj = open(eOutFilePath, "w")
      fObj.writelines(eOutputs[name])
      fObj.close()

# end class Problems
