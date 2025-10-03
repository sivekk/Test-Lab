#!/usr/bin/env python
import subprocess
import os

if os.name == "posix":
    # this doesn't work on Windows machines
    subprocess.Popen(["tools/logChanges.py"])
else:
    # this enables python debugging which is not desired
    subprocess.Popen(["tools/logChanges.py"])

