#!/usr/bin/env python

import json
import sys
import os

filename = sys.argv[1]
arguments = sys.argv[2:]

with open(filename, 'r') as f:
  dumped = json.loads(f.read())
  for i in dumped[0]['variants']:
    os.system('bob build ' + " ".join(arguments) + ' ' + i)


