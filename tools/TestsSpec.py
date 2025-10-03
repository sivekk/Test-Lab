import os
from TestSpec import *
from SpecDir import * 

class TestsSpec(SpecDir):

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
      if (TestsSpec.isTestDir(dirName)):
        dirs.append(dirName)
    return dirs
    
  def testTemplate(this, dirName):
    if this.template == None:
      return None
    else:
      return this.template.getTest(TestSpec.numFromDirName(dirName))
      
  def readTests(this):
    testDirs = this.testDirNames()
    for testDir in testDirs:
      test = TestSpec(os.path.join(this.path, testDir), this.testTemplate(testDir))
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