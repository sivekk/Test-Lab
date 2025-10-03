import os
import re
from LabSpec import *
from SpecDir import * 
from BuildType import *
from Labs import *

class LabsBuilder:

  path = ""
  labs = {} 
  labSpecs = {}

  def __init__(this, path):

    this.path     = path
    this.labs = Labs(this.path)  

  def __repr__(this):
    return "LabsBuilder (path: " + this.path + ")"

  def isTestFile(this, filename):

    javaTestClassFileName = re.compile(".*_t[0-9]+.java")
    pyTestClassFileName   = re.compile(".*_t[0-9]+.py")
    inputFileName         = re.compile(".*_in.txt$")
    eOutputFileName       = re.compile(".*_eout.txt$")
    javaRunnerFileName    = re.compile(".*_Runner.java")
    pyRunnerFileName      = re.compile(".*_Runner.py")

    return ((filename == "testFuncs.py")          or
            (filename == "testFuncs.java")        or
            javaTestClassFileName.match(filename) or
            pyTestClassFileName.match(filename)   or
            javaRunnerFileName.match(filename)    or
            pyRunnerFileName.match(filename)      or
            eOutputFileName.match(filename)       or
            inputFileName.match(filename)           )

  #def findEOutputFiles(this, path):


  #def copyExpectedOutputFiles(this, fromPath, toPath):

  def readLabSpec(this, labName):
      labSpecPath = os.path.join(this.path, labName + "_spec")
      labSpec = LabSpec(labSpecPath)
      return labSpec

  def createLabDir(this, labName, labSpec):

    # sort files by destination directory 

    solutionFiles     = {}
    solutionTestFiles = {}
    labFiles          = {}
    labTestFiles      = {}
    eOutputFileName   = re.compile(".*_eout.txt$")
    
    filteredFiles = SpecDir.filterFiles(labSpec.getFiles(), BuildType("SOLUTION"))
    for filename in filteredFiles:
      # Don't copy expected output files to solution.  The solution generates them.
      if eOutputFileName.match(filename):
        continue

      if this.isTestFile(filename):
        solutionTestFiles[filename] = filteredFiles[filename]
      else:
        solutionFiles[filename] = filteredFiles[filename]

    filteredFiles = SpecDir.filterFiles(labSpec.getFiles(), BuildType("TEMPLATE"))
    for filename in filteredFiles:
      if this.isTestFile(filename):
        labTestFiles[filename] = filteredFiles[filename]
      else:
        labFiles[filename] = filteredFiles[filename]

    # write files to destination directories

    solutionsDirName = labName + "_solutions"
    solutionsPath = os.path.join(this.path, solutionsDirName)
    solutionsDir = SpecDir(solutionsPath, "new")
    solutionsDir.writeFiles(solutionFiles)

    solutionTestsDir = SpecDir(os.path.join(solutionsPath, "tests"), "new")
    solutionTestsDir.writeFiles(solutionTestFiles)

    labDirPath = os.path.join(this.path, labName)
    labDir = SpecDir(labDirPath, "new")
    labDir.writeFiles(labFiles)

    labTestsDirPath = os.path.join(labDirPath, "tests")
    labTestsDir = SpecDir(labTestsDirPath, "new")
    labTestsDir.writeFiles(labTestFiles)

    this.copyGraphicsFiles(labName, labSpec)


  def copyGraphicsFiles(this, labName, labSpec):

    # get graphics file paths
    labSpecPath = labSpec.getPath()
    fromDirs = os.listdir(labSpecPath)
    graphicsFilePaths = []
    for fromDir in fromDirs:
      fromDirPath = os.path.join(labSpecPath, fromDir)
      if not os.path.isdir(fromDirPath):
        continue;
      fileNames = os.listdir(fromDirPath)
      for fileName in fileNames:
        fileExtension = fileName.split(".").pop()
        if (fileExtension == "png" or fileExtension == "jpg" or fileExtension == "GIF" or fileExtension == "gif"):
          graphicsFilePath = os.path.join(fromDirPath, fileName)
          graphicsFilePaths.append(graphicsFilePath) 

    lab = this.labs.getLab(labName)
    labSolutions = this.labs.getLab(labName+"_solutions")
    labDir = lab.getPath()
    labSolutionsDir = labSolutions.getPath()

    # copy files
    for fromPath in graphicsFilePaths:
      fileName = os.path.basename(fromPath)
      labPath = os.path.join(labDir, fileName)
      labSolutionsPath = os.path.join(labSolutionsDir, fileName)
      shutil.copy(fromPath, labPath)
      shutil.copy(fromPath, labSolutionsPath)



  def copyExpectedOutputs(this, labName, labSpec): 

    lab = this.labs.getLab(labName+"_solutions")
    if lab:
      expectedOutputs = lab.getExpectedOutputs()
      labSpec.setExpectedOutputs(expectedOutputs)


  def build(this, labNameRe):

    for labName in this.labs.getLabSpecNames():
      if labNameRe.match(labName):
        print("Building " + labName + "...")
        labSpec = this.readLabSpec(labName)
        this.createLabDir(labName, labSpec)

  def collectOutputs(this, labNameRe):
    for labName in this.labs.getLabSpecNames():
      if labNameRe.match(labName):
        print("Collecting outputs for " + labName + "...")
        labSpec = this.readLabSpec(labName)
        this.copyExpectedOutputs(labName, labSpec)

# end class LabBuilder
