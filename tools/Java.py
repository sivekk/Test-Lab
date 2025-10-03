import re
import os
import subprocess
import shutil

class Java:

    @staticmethod
    def classNameFromFileName(fileName):
        return fileName.split(".").pop(0)

    @staticmethod
    def isJavaFile(path):
        filename = os.path.basename(path)
        jFileName = re.compile(".*\.java")
        return os.path.isfile(path) and jFileName.match(filename)

    @staticmethod
    def findJavaFileNames(path):

        fileNames = os.listdir(path)
        jFileNames = []
        for fileName in fileNames:
            filePath = os.path.join(path, fileName)
            if Java.isJavaFile(filePath): 
                jFileNames.append(fileName)

        return jFileNames

    @staticmethod
    def cleanCompileDir(path):
        if (os.path.isdir(path)):
            shutil.rmtree(path)
        os.mkdir(path)

    @staticmethod
    def compileDir(inPaths, outPath):

        Java.cleanCompileDir(outPath)

        cmdList = ["javac"]
        for path in inPaths:
            cmdList.append("-cp")
            cmdList.append(path)
        cmdList.append("-d")
        cmdList.append(outPath)
        for path in inPaths:
            names = Java.findJavaFileNames(path)
            for name in names:
                filePath = os.path.join(path, name)
                cmdList.append(filePath)

        if (len(names) > 0):
            #print(cmdList)
            subprocess.run(cmdList)

    @staticmethod
    def run(classPath, className, capture, inFileObj):

        # prepare to change working directory 
        classPath = os.path.abspath(classPath)
        dirpath   = os.path.dirname(classPath)
        cwd       = os.getcwd()

        result = None
        filePath = os.path.join(classPath, className + ".class")
        if os.path.isfile(filePath):

            # run in directory where java file is
            os.chdir(dirpath)
            #print("classPath:", classPath, ", className:", className)
            if capture:
                #result = subprocess.run(["java", "-cp", classPath, className], text=True, stdin=inFileObj, stdout=subprocess.PIPE)
                result = subprocess.run(["java", "-cp", classPath, className], text=True, stdin=inFileObj, capture_output=True)
            else:
                result = subprocess.run(["java", "-cp", classPath, className])

            # restore previous working directory
            os.chdir(cwd)

        return result
