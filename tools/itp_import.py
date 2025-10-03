#!/usr/bin/env python
import sys
import os
import re
from Dir import *

def renameInFile(path):
    dirname  = os.path.dirname(path)
    newfilename = "ppNum_pName_ttNum_in.txt"
    newFilePath = os.path.join(dirname, newfilename)
    os.rename(path, newFilePath)
    return(newfilename)

def renameTestFuncsFile(path):
    dirname  = os.path.dirname(path)
    newfilename = "ppNum_pName_ttNum.py"
    newFilePath = os.path.join(dirname, newfilename)
    os.rename(path, newFilePath)
    return(newfilename)

def modifyTestFuncsFile(path):
    modlines = []
    fobj = open(path)
    defLine = re.compile("def.*")
    afterDefLine = False
    for line in fobj.readlines():

        # get rid of function definition lines
        if (defLine.match(line)):
            afterDefLine = True
            continue

        modline = line

        if afterDefLine:
            modline = modline.replace("  ", "", 1)
            #modline = modline.strip()

        # get rid of "labs." 
        modline = modline.replace("labs.", "")

        #modline = modline + "\n"
        modlines.append(modline)
        fobj.close()

    fobj = open(path, "w")
    fobj.writelines(modlines)
    fobj.close()

    return modlines

def modifySolutionFile(path):
    modlines = []
    fobj = open(path)
    labsRe = re.compile(".*labs\.[a-zA-Z]+")
    gasketRe = re.compile(".*LabTestGasket")
    for line in fobj.readlines():

        modline = line

        # get rid of old gasket import
        if gasketRe.match(modline):
            continue 

        # get rid of "labs." 
        if labsRe.match(line):
            modline = modline.replace("labs.", "")

        modlines.append(modline)

    fobj.close()

    fobj = open(path, "w")
    fobj.writelines(modlines)
    fobj.close()

    return modlines

def copySolutionCode(labPath, outPath):
    # extract lab info
    labName = os.path.basename(labPath)
    labDirPath = os.path.dirname(labPath)

    inPath = os.path.join(labDirPath, "solution", labName+"-Solution", "labs", "labenv", "lab_specification")
    inDir = Dir(inPath)
    problemDirRe = re.compile(".*p[0-9]+_[^/]+$")
    typicalSolutionFileRe = re.compile("p[0-9]+_.*\.py")
    solutionFileRe = re.compile(".*\.py")
    solutionPaths = inDir.findFile(solutionFileRe)

    # add any other top level files
    topFileNames = inDir.filenames()
    for name in topFileNames:
        if solutionFileRe.match(name):
            continue
        topFilePath = os.path.join(inPath, name)
        solutionPaths.append(topFilePath)

    backupRe = re.compile(".*\.backup")
    for solutionPath in solutionPaths:

        solutionDirPath = os.path.dirname(solutionPath)

        # skip backup files
        if backupRe.match(solutionPath):
            continue; 

        # skip directories that aren't solution directories
        if not problemDirRe.match(solutionDirPath) and os.path.basename(solutionDirPath) != "lab_specification":
            continue;


        solutionFileName = os.path.basename(solutionPath)
        if os.path.basename(solutionDirPath) != "lab_specification":
            dstDirPath = os.path.join(outPath, os.path.basename(solutionDirPath))
        else:
            dstDirPath = os.path.join(outPath)

        # remove old template file
        templateFilePath = os.path.join(dstDirPath, solutionFileName)
        if os.path.isfile(templateFilePath):
            os.remove(templateFilePath)


        if typicalSolutionFileRe.match(solutionFileName):
            dstFileName = "ppNum_pName.py"
        else:
            dstFileName = solutionFileName
        dstPath = os.path.join(dstDirPath, dstFileName)
        print("solutionPath:", solutionPath)
        print("dstPath:", dstPath)
        shutil.copyfile(solutionPath, dstPath)
        modifySolutionFile(dstPath)


def createRunnerFiles(outPath, subdirNames):
    pyFileRe = re.compile(".*\.py$")
    pNum_pName_FileRe = re.compile("p[0-9]+_")
    for subdirName in subdirNames:
        subDirPath = os.path.join(outPath, subdirName)
        dirlist = os.listdir(subDirPath)
        pyFileName = "" 
        for filename in dirlist:
            if pyFileRe.match(filename):
                pyFileName = filename.split(".")[0]

        if not pNum_pName_FileRe.match(pyFileName):
            lines = ["import "+pyFileName+"\n",
                    "\n",
                    pyFileName+".ppNum_pName()\n",
                    "\n"                          ]
        else: 
            lines = ["import ppNum_pName\n",
                    "\n",
                    "ppNum_pName.ppNum_pName()\n",
                    "\n"                          ]
        filepath = os.path.join(outPath, subdirName, "tests", "ppNum_pName_Runner.py")
        fobj = open(filepath, "w")
        fobj.writelines(lines)
        fobj.close()

def modifyInstructions(outPath, subdirNames):
    for subdirName in subdirNames:
        (pNum, pName) = subdirName.split("_")
        filepath = os.path.join(outPath, subdirName, "instructions.md")
        fobj = open(filepath)
        lines = fobj.readlines()
        fobj.close()
        writelines = []
        inFileRe = re.compile(".*\/in>>")
        outFileRe = re.compile(".*\/out>>")
        for line in lines:
            if inFileRe.match(line):
                line = line.replace("in>>", "&&&ppNum_pName_ttNum_in.txt>>")
            if outFileRe.match(line):
                strs = line.split("/")
                strs.pop()
                tNum = strs.pop()
                line = line.replace("out>>", pNum+"_"+pName+"_"+tNum+"_eout.txt>>")
            writelines.append(line)
        fobj = open(filepath, "w")
        fobj.writelines(writelines)
        fobj.close()



# get command line arguments
if len(sys.argv) < 3:
    sys.exit("usage:  itp_import.py <input path> <output path>")

# get labName info
labPath = sys.argv[1].strip("/")

# get input dir
inPath = os.path.join(labPath, "labs", "labenv", "lab_specification")
inDir  = Dir(inPath)

# make output dir
outPath  = sys.argv[2] + "_spec"
outDir = Dir(outPath)
outDir.clean() 

# copy input subdirs to output dir
subdirNames = inDir.subdirNames()
for name in subdirNames:
    inSubdirPath  = os.path.join(inPath, name)
    outSubdirPath = os.path.join(outPath, name)
    # remove these directories
    if name == "ppNum_pName":
        rmDir = Dir(inSubdirPath)
        rmDir.remove()
    else:
        shutil.copytree(inSubdirPath, outSubdirPath)
subdirNames = inDir.subdirNames()

# rename files named "in"
inRe = re.compile("in$")
for path in outDir.findFile(inRe):
    renameInFile(path)

# remove files named "out"
outRe = re.compile("out$")
for path in outDir.findFile(outRe):
    os.remove(path)

# modify and rename files named "testFuncs.py"
testFuncsRe = re.compile("testFuncs.py$")
for path in outDir.findFile(testFuncsRe):
    modifyTestFuncsFile(path)
    renameTestFuncsFile(path)

# create runner files
createRunnerFiles(outPath, subdirNames)

# copy solution code 
copySolutionCode(labPath, outPath)

# modify instrutions.md
modifyInstructions(outPath, subdirNames)

"""
# copy input files to output dir
filenames = inDir.filenames()
for name in filenames:
    inFilePath  = os.path.join(inPath, name)
    outFilePath = os.path.join(outPath, name)
    shutil.copy(inFilePath, outFilePath)
    modifySolutionFile(outFilePath)
filenames = inDir.filenames()
"""


