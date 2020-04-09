#!/usr/bin/env python3
#
# author: Christoph Schwalbe
#
# Description: This program check an Override file for the include Keyword and warns if sth file is missing
#
import ruamel.yaml
import ruamel.yaml.util
from os import path
from os.path import isfile
from os.path import basename
import sys
import os
import logging
#
# simple usage: check_override /path/to/file/and/fileName.yaml
# basedir: recipes
#

class OverrideNotFoundError(Exception):
   """Override File was not Found"""
   def __init__(self, text):
      self.text = text
   def __str__(self):
      return repr(self.text)

log = logging.getLogger(__name__)

def open_yaml(filepart):
   filepath_base = './'
   myyaml = ruamel.yaml.YAML(typ='rt')
   myyaml.preserve_quotes = True
   myyaml.default_flow_style = False
   myyaml.indent(mapping=3, sequence=4, offset=2)
   myyaml.allow_duplicate_keys = True

   filepath = path.relpath(filepath_base + filepart)
   with open(filepath, "r") as f:
      myfile = myyaml.load(f)
   return myfile

def write_yaml(filepart, new_file):
   filepath_base = '../'
   filepath = filepath_base + filepart
   myyaml = ruamel.yaml.YAML(typ='rt')
   myyaml.preserve_quotes = True
   myyaml.default_flow_style = False
   myyaml.indent(mapping=3, sequence=4, offset=2)
   myyaml.allow_duplicate_keys = True
   #write to file
   with open(filepath, "w") as f:
      myyaml.dump(new_file, f)



def check_override_file(checkIfFileExists):
   fileName = checkIfFileExists
   if not os.path.isfile(fileName):
      raise OverrideNotFoundError("Override file: '{}' does not exist!".format(fileName))
   else:
     overrideFile = open_yaml(fileName)
     for i in overrideFile:
      if 'include' in i:
         #print(overrideFile['include'])
         for p in overrideFile['include']:
            current = './' + p + '.yaml'
            override = os.path.dirname(current)
            #print(current)
            #print(os.path.exists(current))
            if not os.path.exists(current):
              log.error("Override file: '{}' does not exist!".format(current))

if len(sys.argv) == 1:
    print("please give the filepath + filename as Parameter.")
else:
    check_override_file(str(sys.argv[1]))
