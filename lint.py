#!/usr/bin/env python
# -*- coding: utf-8; mode: Python; py-indent-offset: 4 -*-

import os
import sys


include = ["base_project"]
exclude = []

incstr = " ".join(include)
excstr = ",".join(exclude)


print("Checking PEP8 ...")
if os.system("pycodestyle --show-source --show-pep8 --max-line-length=79 --filename=*py " +
             "--exclude=" + excstr + " " + incstr) != 0:
    sys.exit(1)

print("Running lint ...")
if os.system("pylint --rcfile=pylintrc --ignore=" +
             excstr + " " + incstr) != 0:
    sys.exit(1)

sys.exit(0)
