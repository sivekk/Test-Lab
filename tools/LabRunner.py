from tools.LabTestGasket import *
import os
import re
import subprocess

class LabRunner:
  
  def __init__(this, path):
    #this.problemsPath  = os.path.join(path, "specification")
    #this.problems      = tools.libspec.Problems(this.problemsPath) 

    this.path = path
    this.labNames = this.findLabNames()


    #testsPath = os.path.join(this.path, "tests")
    #this.tests = tools.libtests.Tests(testsPath)








  def runSelectPrompt(this):

    prompt =  ""
    prompt += "Select item to run.\n"
    prompt += "  0 - All Tests\n"
    for pNum in this.problems.getNums():
      problem = this.problems.getProblem(pNum)
      pName   = problem.getName()
      prompt += "  " +  pNum + " - Problem" + pNum + " : " + pName + "\n"
      tNums = problem.getTests().getNums()
      for tNum in tNums: 
        prompt += '    ' + pNum + '.' + tNum + ' - ' + 'Test' + tNum + "\n"

    return prompt

  def allTestsPassingPrompt(this):
    print()
    print("---- ATTENTION ----")
    print()
    print("Now that all of your tests are passing, you must do the following to complete your lab:")
    print("  1. Run the tests in the Replit Test tool.")
    print("  2. Look at the results in the Console and make sure all the tests passed.")
    print("  3. Click the Submit button to submit your lab.")

  def run(this, selection = ""):
    """
    This function is executed when the lab is run.
    """

    for labName in this.labNames:
      this.compile(labName)
      classPath = os.path.join(this.path, labName, "compiled")
      javaRunSelectorPath = os.path.join(classPath, "RunSelector.class")
      if os.path.isfile(javaRunSelectorPath):
        print("Running run selector for " + labName + "...")
        subprocess.Popen(["java", "-cp", classPath, "RunSelector", "arg1"])
  
    return

    testResult = "FAILED"
    
    if (selection == ""):
      selection = input(this.runSelectPrompt())

    if (selection == "0"):
      testResult = this.problems.runAllTests()
      if (testResult == "Passed"):
        this.allTestsPassingPrompt()
    else:
      selectionParts = selection.split(".")
      pNum = selectionParts.pop(0) 
      tNum = None
      if len(selectionParts) > 0:
        tNum = selectionParts.pop(0)
      # get problem to run
      testResult = this.problems.getProblem(pNum).run(tNum)

    return testResult

# end class LabRunner
