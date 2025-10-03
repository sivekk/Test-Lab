import os
import re
import importlib
import TestsSpec
from SpecDir import * 

class ProblemSpec(SpecDir):

  def __init__(this, path, template):
    
    this.dirName    = os.path.basename(path)
    this.num        = ProblemSpec.numFromDirName(this.dirName)
    this.name       = ProblemSpec.nameFromDirName(this.dirName)
    
    super().__init__(path, template)
    
    this.testsPath = os.path.join(this.path, "tests")
    
    this.tests     = TestsSpec.TestsSpec(this.testsPath, this.testsTemplate()) 
    this.mergeChildrenFileFragments()

  def removeSolution(this, buildType):
    files = {}
    filename = this.readPyFileName()
    fileObj = open(os.path.join(this.path, filename))
    files[filename] = fileObj.readlines()
    filteredFiles = SpecDir.filterFiles(files, buildType)
    this.writeFiles(filteredFiles, forceWrite = True)
    
  def strFromTemplateStr(this, str): 
    #pNumRe = re.compile(".*pNum")
    #if (pNumRe.match(str)):
    #  print("str:", str)
    ignoreRe = re.compile(".*&&&")
    if (ignoreRe.match(str)):
      str = str.replace("&&&", "")
    else:
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
