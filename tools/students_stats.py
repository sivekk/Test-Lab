#!/usr/bin/env python
import re
import os 

def readLog(logfilename):

    iterRe    = re.compile("iter: ")
    logTimeRe = re.compile("^log time:"); 

    logtimes = {}
    file = open(logfilename)
    lines = file.readlines()

    for line in lines:
        # skip first snapshots because time from previous edit is unknown
        line = line.strip()
        if iterRe.match(line):
            (s1, iter) = line.split(" ")
        elif iter != "0" and logTimeRe.match(line):
            (s1, s2, date, time)= line.split(" ")    
            logtimes[date + " " + time] = iter
    file.close()

    return logtimes


def readChangeLog(filename):

    startRe        = re.compile("^timestamp")
    changedLinesRe = re.compile("^# changed lines:") 
    addOrRmLinesRe = re.compile("^# added or removed lines:") 
    timeRe         = re.compile("^--- [a-zA-Z]") 
    removedLineRe  = re.compile("^- ")

    months = {
        "Jan":"01",
        "Feb":"02",
        "Mar":"03",
        "Apr":"04",
        "May":"05",
        "Jun":"06",
        "Jul":"07",
        "Aug":"08",
        "Sep":"09",
        "Oct":"10",
        "Nov":"11",
        "Dec":"12",
        }

    file = open(filename)
    lines = file.readlines()
    snapshots = {}
    snapshot = {}
    for line in lines:
        if startRe.match(line):
            #if "numAddedLines" in snapshot: 
            #    numAddedLines = snapshot["numAddedLines"]
            #    if not numAddedLines in snapshots:
            #        snapshots[numAddedLines] = []
            #    snapshots[numAddedLines].append(snapshot)
            #snapshot = {"filename":filename, "lines":[]}
            if "numAddDelLines" in snapshot: 
                numAddDelLines = snapshot["numAddDelLines"]
                if not numAddDelLines in snapshots:
                    snapshots[numAddDelLines] = []
                snapshots[numAddDelLines].append(snapshot)
            snapshot = {"filename":filename, "lines":[]}
        elif changedLinesRe.match(line):
            snapshot["numChangedLines"] = int(line.split(" ").pop())
        elif addOrRmLinesRe.match(line):
            snapshot["numAddDelLines"] = int(line.split(" ").pop())
        elif timeRe.match(line):
            (s1, s2, weekday, month, day, time, year) = line.split()
            month = months[month] 
            if (int(day) < 10):
                day = "0"+day
            date = year+"-"+month+"-"+day
            #snapshots[date + " " + time] = snapshot
#        elif removedLineRe.match(line):
#            snapshot["numAddedLines"] = snapshot["numAddedLines"] - 1

        if "lines" in snapshot:
            snapshot["lines"].append(line)
    file.close()

    return snapshots

def readChangeLogs(dirName):

    fileSnapshots = {} 
    changeLogRe = re.compile(".*\.changelog$")
    filenames = os.listdir(dirName)
    for filename in filenames:
        if changeLogRe.match(filename):
            fileSnapshots[filename] = readChangeLog(filename)
    return fileSnapshots

def printSortedChangeLogs(changelogs):
    for filename in changelogs:
        changelog = changelogs[filename]
        keys = list(changelog.keys())
        keys.sort()
        keys.reverse()
        #for numAddedLines in keys:
        #    snapshots = changelog[numAddedLines]
        #    print("filename:", filename, "numAddedLines:", numAddedLines)
        for numAddDelLines in keys:
            snapshots = changelog[numAddDelLines]
            print("filename:", filename, "numAddDelLines:", numAddDelLines)
            for snapshot in snapshots:
                lines = snapshot["lines"]
                print("".join(lines))



#readLog("LOGGER_LOG")
changelogs = readChangeLogs(".")
printSortedChangeLogs(changelogs)