#!/usr/bin/env python
from LabsBuilder import * 
import sys
import re

lab = ".*"

if len(sys.argv) > 1:
    lab = sys.argv[1]

labRe = re.compile(lab)

# build
LabsBuilder(".").collectOutputs(labRe)
print()