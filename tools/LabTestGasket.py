"""
This file is used to test the problems in this lab. 
"""
import io

origprint = print
originput = input

def print(*args, **kwargs):
  if (g.MODE == "RUNNING TEST"):
    output = io.StringIO()
    g.print(*args, file=output, **kwargs)
    printStr = output.getvalue()
    output.close()
    g.outLines.append(printStr)
  else:
    g.print(*args, **kwargs)
  
def input(arg=""):
  if (g.MODE == "RUNNING TEST"):
    print(arg, end="")
    if len(g.inLines) > 0:
      return g.inLines.pop(0).strip()
    else:
      return None
  else:
   return g.input(arg)

class TestGasket:

  def __init__(this):
    this.input = originput
    this.print = origprint
    this.MODE = "NORMAL"
    this.inLines = []
    this.outLines = []

  def startTest(this, inLines):
    this.inLines = inLines.copy() 
    this.MODE    = "RUNNING TEST"

  def endTest(this):
    
    this.MODE     = "NORMAL"
    testOutput = "".join(this.outLines).splitlines(keepends=True)
    this.outLines = []
    
    return testOutput 
    

g = TestGasket()
  


