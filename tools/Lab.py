import os
from Tests import * 
from Java import *
from Python import * 

class Lab:

    def __init__(this, path):

        this.path     = path
        this.labName  = os.path.basename(this.path)

        this.compiledPath  = os.path.join(this.path, "compiled")
        this.testsPath = os.path.join(this.path, "tests")

        this.tests = Tests(this.testsPath, this.compiledPath)

    def __repr__(this):
        return "Lab " + this.labName

    def getName(this):
        return this.labName

    def getExpectedOutputs(this):
        return this.tests.getExpectedOutputs()
    
    def getPath(this):
        return this.path

    def compileDir(this):
        Java.compileDir([this.path, this.testsPath], this.compiledPath)
        Python.compileDir([this.path, this.testsPath], this.compiledPath)

    def run(this, selection="x", verbose=True):
        this.compileDir()
        results =  this.tests.run(selection, verbose)
 
        return results
