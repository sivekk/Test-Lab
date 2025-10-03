import os
import re
import sys
from Lab import *

class Labs:


    def __init__(this, path):

        this.path = path
        this.labNames = this.findLabNames()
        this.labSpecNames = this.findLabSpecNames()
        this.labs = {} 

    def __repr__(this):
        return "Labs (path: " + this.path + + " " + this.labs + ")"

    def getLabNames(this):
        return this.labNames

    def getLabSpecNames(this):
        return this.labSpecNames

    def getLab(this, labName):
        if not labName in this.labNames:
            return None
        if not labName in this.labs:
            this.labs[labName] = this.readLab(labName)
        return this.labs[labName]

    def findLabNames(this):
        labSpecDirName = re.compile("(lab_.+)_spec$")
        labDirName = re.compile("(lab_.+)")
        names = os.listdir(this.path)
        labNames = []
        for name in names:

            # skip spec directories
            match = labSpecDirName.match(name)
            if match:
                continue
            match = labDirName.match(name)

            # skip non-lab directories
            if not match:
                continue

            labName = match.group(1)
            labNames.append(labName)
        labNames.sort()
        return labNames 

    def findLabSpecNames(this):
        labSpecDirName = re.compile("(lab_.+)_spec$")
        names = os.listdir(this.path)
        labSpecNames = []
        for name in names:
            # skip non-spec directories
            match = labSpecDirName.match(name)
            if not match:
                continue

            labName = match.group(1)
            labSpecNames.append(labName)
        labSpecNames.sort()
        return labSpecNames 

    """
    def findLabNames(this, selection="all"):

        selectionRe = re.compile(".*" + selection)
        labDirName = re.compile("(lab_.+)")
        labSpecDirName = re.compile("(lab_.+)_spec$")
        names = os.listdir(this.path)
        names.sort()
        labNames = []
        for name in names:
            match = labDirName.match(name)

            if (not os.path.isdir(name)    or 
                not match                  or 
                labSpecDirName.match(name)   ): 
                continue

            labName = match.group(1)
            if (selection != "all" and not selectionRe.match(labName)):
                continue
            labNames.append(labName)
        return labNames 
    """
    
    def readLab(this, labName):
        labPath = os.path.join(this.path, labName)
        this.labs[labName] = Lab(labPath)
        return this.labs[labName] 

    def run(this, labNameRe, selection="x", verbose=True):
        results = {} 
        found = False
        for labName in this.labNames:
            if labNameRe.match(labName):
                print("\nRunning " + labName + "...\n")
                found = True
                labResults = this.getLab(labName).run(selection, verbose)
                numPassed = 0
                for labResult in labResults:
                    if labResult == "Passed":
                        numPassed = numPassed + 1 
                results[labName] = [numPassed, labResults]
        if found == False:
            sys.exit("Failed to find lab matching selection.")
        return results
