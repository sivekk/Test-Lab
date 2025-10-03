import re
import os
import subprocess
import shutil
import sys

class Python:

    @staticmethod
    def classNameFromFileName(fileName):
        return fileName.split(".").pop(0)

    @staticmethod
    def isPythonFile(path):
        filename = os.path.basename(path)
        jFileName = re.compile(".*\.py")
        return os.path.isfile(path) and jFileName.match(filename)

    @staticmethod
    def findPythonFileNames(path):

        fileNames = os.listdir(path)
        pyFileNames = []
        for fileName in fileNames:
            filePath = os.path.join(path, fileName)
            if Python.isPythonFile(filePath): 
                pyFileNames.append(fileName)

        return pyFileNames

    @staticmethod
    def compileDir(inPaths, outPath):

        eoutRe = re.compile(".*eout\.txt$")
        if (not os.path.isdir(outPath)):
            os.mkdir(outPath)
        for path in inPaths:
            #names = Python.findPythonFileNames(path)
            names = os.listdir(path)
            for name in names:
                # skip expected output files
                if eoutRe.match(name):
                    continue; 
                filePath = os.path.join(path, name)
                if os.path.isfile(filePath):
                    shutil.copy(filePath, outPath)


    @staticmethod
    def run(path, capture, inFileObj):

        # prepare to change working directory 
        path    = os.path.abspath(path)
        dirpath = os.path.dirname(path)
        cwd     = os.getcwd()

        result = None
        if Python.isPythonFile(path):

            # run in directory where python file is
            os.chdir(dirpath)
            if capture:
                result = subprocess.run(["python", path], text=True, stdin=inFileObj, stdout=subprocess.PIPE)
            else:
                result = subprocess.run(["python", path])

            # restore previous working directory
            os.chdir(cwd)

        return result

