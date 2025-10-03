#!/usr/bin/env python
import sys
from Labs import * 
import os
import re
import subprocess
from Dir import *

# FIXME:  Changing this script so that it works as follows would help automate lab creation
# copy desired files to export build folder 
# rearrange files before archiving
#  - move everything in lab_<> to lab folder
#  - move files named top_<> in lab folder to the top folder
# archive files
# remove build folder contents

def export(lab):

    print("Exporting", lab)
    selectedLabDir = re.compile(lab+"$")
    labDir = re.compile("lab_.*")

    archiveFileName = lab + ".tgz"
    archiveFilePath = os.path.join("export", archiveFileName)

    if (os.path.isfile(archiveFilePath)):
        os.remove(archiveFilePath)

    archiveCmd = ["tar", "-zcf", archiveFilePath]
    dirList = os.listdir(".")
    skipList = [".git", "export", "APCS", "ITP", "README.md", "scores", "OldLabs"]
    for item in dirList:
        if item in skipList:
            continue
        if selectedLabDir.match(item) or not labDir.match(item):
            archiveCmd.append(item)

    subprocess.run(archiveCmd)


lab = "all"
exportPath = "export"
exportDir = Dir("export")

if len(sys.argv) > 1:
    lab = sys.argv[1]

if lab == "clean":
    exportDir.clean()
elif lab == "all":
    exportDir.clean()
    labNames = Labs(".").findLabNames()
    for lab in labNames:
        export(lab)
else:
    export(lab)