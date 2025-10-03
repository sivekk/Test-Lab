from Test import *
import os
import re

class Tests:

    javaRunnerNamesRe = re.compile(".*_Runner\\.java")
    pyRunnerNamesRe   = re.compile(".*_Runner\\.py")
    javaTestNamesRe   = re.compile(".*_t[0-9]+\\.java$") 
    pyTestNamesRe     = re.compile(".*_t[0-9]+\\.py$") 
    eOutputNamesRe    = re.compile(".*_t[0-9]+_eout\\.txt$")

    def __init__(this, path, compiledPath):
        
        this.path = path
        this.compiledPath = compiledPath
        this.testFileNames = this.findTestFileNames()
        this.runnerFileNames = this.findRunnerFileNames()
        this.tests = this.readTests()
        this.runners = this.readRunners()

    def __repr__(this):
        return "Tests (path: " + this.path + ")"

    def isRunnerFile(this, path):
        name = os.path.basename(path)
        return (os.path.isfile(path)                  and
                (this.javaRunnerNamesRe.match(name) or 
                 this.pyRunnerNamesRe.match(name)     )    )

    def isTestFile(this, path):
        name = os.path.basename(path)
        return (os.path.isfile(path)                  and
                (this.javaTestNamesRe.match(name) or 
                 this.pyTestNamesRe.match(name)     )    )

    def findRunnerFileNames(this):
        runnerNames = []
        for name in os.listdir(this.path):
            filePath = os.path.join(this.path, name)
            if this.isRunnerFile(filePath): 
                runnerNames.append(name)
        runnerNames.sort()
        return runnerNames

    def findTestFileNames(this):
        testNames = []
        for name in os.listdir(this.path):
            filePath = os.path.join(this.path, name)
            if this.isTestFile(filePath): 
                testNames.append(name)
        testNames.sort()
        return testNames

    def isExpectedOutputFile(this, path):
        name = os.path.basename(path)
        return (os.path.isfile(path)           and
                 this.eOutputNamesRe.match(name)   )

    def getExpectedOutputs(this):
        expectedOutputs = {}
        for testName in this.testFileNames:
            test = this.tests[testName]
            eOutFileName = test.getEOutFileName()
            expectedOutputs[eOutFileName] = test.getExpectedOutput()
        return expectedOutputs 
             
    def readRunners(this):
        runners = {} 
        for name in this.runnerFileNames:
            runnerPath = os.path.join(this.path, name)
            runners[name] = Test(runnerPath, this.compiledPath)
        return runners

    def readTests(this):
        tests = {} 
        for name in this.testFileNames:
            testPath = os.path.join(this.path, name)
            tests[name] = Test(testPath, this.compiledPath)
        return tests

    def runSelectPrompt(this):

        this.pNames = {}

        prompt =  ""
        prompt += "Select item to run.\n"
        prompt += "  0 - All Tests\n"

        prevPNum = 0
        for name in this.testFileNames: 
            (baseName, extension) = name.split(".")
            (pNumStr, pName, testDirName) = baseName.split("_")
            pNum = pNumStr.strip("p")
            this.pNames[pNum] = pName
            tNum = testDirName.strip("t")
            if (pNum != prevPNum):
                prompt += "  " +  pNum + " - Problem" + pNum + " : " + pName + "\n"
            prompt += '    ' + pNum + '.' + tNum + ' - ' + 'Test' + tNum + "\n"
            prevPNum = pNum

        return prompt

    def selectTestFileNames(this, pNumSel, tNumSel):
        names = []

        if tNumSel == None:
            pName = this.pNames[pNumSel]
            name = "p"+pNumSel+"_"+pName+"_Runner.py"
            if name in this.runnerFileNames:
                names.append(name)
            else:
                name = "p"+pNumSel+"_"+pName+"_Runner.java"
                names.append(name)
        else:
            for name in this.testFileNames:
                basename = name.split(".").pop(0)
                (pstr, labName, tstr) = basename.split("_")
                pNum = pstr.strip("p")
                tNum = tstr.strip("t")
                if (pNum == pNumSel) and (tNum == tNumSel):
                    names.append(name)
        return names


    def allTestsPassingPrompt(this):
        print()
        print("---- ATTENTION ----")
        print()
        print("Now that all of your tests are passing, to turn in your lab you must save it to GitHub with the following actions:")
        print("  1. Click on the Source Control tool.")
        print("  2. Enter a message in the box at the top.")
        print("  3. Click the Commit button.")
        print("  4. Click the Sync button.")

    def allTestsPassing(this, results, selection):
        allPassing = True
        if selection != "0":
            allPassing = False
        for result in results:
            if result != "Passed":
                allPassing = False 
        return allPassing

    def run(this, selection="", verbose=True):

        results = []


        if (selection == "x"):
            print(this.runSelectPrompt())
            selection = input()

        if (selection == "0"):
            testNames = this.testFileNames
        else:
            selectionParts = selection.split(".")
            pNum = selectionParts.pop(0) 
            tNum = None

            # problem was selected instead of test
            if len(selectionParts) < 1:
                runnerName = this.selectTestFileNames(pNum, tNum).pop(0)
                result = this.runners[runnerName].run(False, False)
                results.append(result)
                return results 

            tNum = selectionParts.pop(0)
            testNames = this.selectTestFileNames(pNum, tNum)

        for testName in testNames:
            result = this.tests[testName].run(True, verbose)
            results.append(result)

        if this.allTestsPassing(results, selection):
            if (verbose):
                this.allTestsPassingPrompt()

        return results


