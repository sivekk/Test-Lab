#!/usr/bin/env python
import os
import sys
import re
import subprocess
import shutil 
import difflib
import pathlib
import datetime
import time

def getFilesDir(reStr):
    fileDirsRe = re.compile(reStr)
    dirlist = os.listdir()
    dirlist.sort()
    for name in dirlist:
        if not fileDirsRe.match(name):
            continue
        if os.path.isdir(name):
            return name    

def getFileNames(path):
    fileNames = []

    #if len(sys.argv) > 1:
    #    FILES_RE_STR = sys.argv[1]

    filesRe = re.compile(FILES_RE_STR)

    for fileName in os.listdir(path):
        if not filesRe.match(fileName):
            continue
        if os.path.isdir(os.path.join(path, fileName)):
            continue
        fileNames.append(fileName)

    return fileNames

def makeLogDir(path):
    if (not os.path.isdir(path) and not os.path.isfile(path)):
        os.mkdir(path)


def logFileChanges(fileName, srcDirPath, destDirPath):

    srcFilePath = os.path.join(srcDirPath, fileName)
    snapshotFilePath = os.path.join(destDirPath, fileName+".snapshot")
    changelogFilePath = os.path.join(destDirPath, fileName+".changelog")

    # create initial snapshot file
    if (not os.path.isfile(snapshotFilePath)):
        shutil.copyfile(srcFilePath, snapshotFilePath)

    # log file changes
    srcFile = open(srcFilePath)
    srcLines = srcFile.readlines()   
    srcFile.close()
    snapshotFile = open(snapshotFilePath)
    snapshotLines = snapshotFile.readlines()
    snapshotFile.close() 
    srcModTime = datetime.datetime.fromtimestamp(pathlib.Path(srcFilePath).stat().st_mtime).ctime()
    snapshotModTime = datetime.datetime.fromtimestamp(pathlib.Path(snapshotFilePath).stat().st_mtime).ctime()
    changes = list(difflib.context_diff(snapshotLines, srcLines, fromfile=snapshotFilePath, tofile=srcFilePath, fromfiledate=snapshotModTime, tofiledate=srcModTime, n=3, lineterm='\n'))
    if (len(changes) > 0):
        changes.insert(0, "# added or removed lines: " + str(numAddRmLines(changes)) + "\n")
        changes.insert(0, "# changed lines: " + str(numChangedLines(changes)) + "\n")
        changes.insert(0, "timestamp in seconds: " + str(int(time.time())) + "\n")
        changes.insert(0, "\n------------------------------------------------------------------\n\n")
        changelogFile = open(changelogFilePath, "a")    
        changelogFile.writelines(changes)
        changelogFile.close()

    # take new snapshot
    os.remove(snapshotFilePath)
    shutil.copyfile(srcFilePath, snapshotFilePath)

def numAddRmLines(lines):
    num = 0;
    for line in lines:
        if ADD_RM_LINE_RE.match(line):
            num = num + 1
    return num

def numChangedLines(lines):
    num = 0;
    for line in lines:
        if CHANGED_LINE_RE.match(line):
            num = num + 0.5 
    return int(num)


#### MAIN PROGRAM ###

# parameters
LOG_PATH = ".changelog"
LOGGER_LOG_PATH = os.path.join(LOG_PATH, 'LOGGER_LOG')
FILE_DIRS_RE_STR = "lab_"
FILES_RE_STR = ".+.py|.+.java"
LOGGING_INTERVAL_SECONDS = 60 
LOGGING_DURATION_MINUTES = 60 
LOGGING_ITERATIONS = (LOGGING_DURATION_MINUTES * 60) // LOGGING_INTERVAL_SECONDS
CHANGED_LINE_RE = re.compile("^! ") 
ADD_RM_LINE_RE = re.compile("^[+-] ") 



# only log if .changelog dir exists

logDirExists = os.path.isdir(LOG_PATH)

if (not logDirExists):
    sys.exit(0)

logDirModTime = int(pathlib.Path(LOG_PATH).stat().st_mtime)
curTime = int(time.time())
timeSinceMod = curTime - logDirModTime

if (timeSinceMod > LOGGING_INTERVAL_SECONDS):

    for iter in range(LOGGING_ITERATIONS):

        filesDir = getFilesDir(FILE_DIRS_RE_STR)
        fileNames = getFileNames(filesDir)

        # logger log
        loggerLog = [
            "iter: " + str(iter) + "\n",
            "log time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n",
            "LOG_PATH: " + LOG_PATH + "\n",
            "LOGGER_LOG_PATH: " + LOGGER_LOG_PATH + "\n",
            "FILE_DIRS_RE_STR: " + FILE_DIRS_RE_STR + "\n",
            "FILES_RE_STR: " + FILES_RE_STR + "\n",
            "LOGGING_INTERVAL_SECONDS: " + str(LOGGING_INTERVAL_SECONDS) + "\n",
            "LOGGING_DURATION_MINUTES: " + str(LOGGING_DURATION_MINUTES) + "\n",
            "LOGGING_ITERATIONS: " + str(LOGGING_ITERATIONS) + "\n",
            "curTime: " + str(curTime) + "\n",
            "timeSinceMod: " + str(timeSinceMod) + "\n",
            "filesDir: " + filesDir + "\n",
            "fileNames: " + ", ".join(fileNames) + "\n",
            "-------------------------------------------------------\n"
        ]
        llog = open(LOGGER_LOG_PATH, "a")
        llog.writelines(loggerLog)
        llog.close()

        for fileName in fileNames:
            logFileChanges(fileName, filesDir, LOG_PATH)
        time.sleep(LOGGING_INTERVAL_SECONDS)


