#!/usr/bin/env python
from Labs import *
from LabsBuilder import *
import sys
import re

lab = ".*"
selection = "0"

if len(sys.argv) > 1:
    lab = sys.argv[1]
if len(sys.argv) > 2:
    selection = sys.argv[2]

labRe = re.compile(lab)

# build
LabsBuilder(".").build(labRe)
print()

# run
Labs(".").run(labRe, selection)
