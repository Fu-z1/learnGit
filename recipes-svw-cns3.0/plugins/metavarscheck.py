# Bob build tool
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import binascii
from os.path import join
import json
import os
import re
import shutil
import subprocess
import tempfile
import sys
import time

from bob.input import GitScm, UrlScm

RETRY_COUNT = 3
RETRY_TIMEOUT = 2 # seconds

RED = '\x1b[31;1m'
YELLOW = '\x1b[33;1m'
GREEN = '\x1b[32;1m'
BLUE = '\x1b[34;1m'
END = '\x1b[0m'

def red(text):
  return RED + text + END

def yellow(text):
  return YELLOW + text + END

def green(text):
  return GREEN + text + END

def blue(text):
  return BLUE + text + END

# scan package recursivelely with its dependencies and build a list of checkout dirs
def getPackageVariants(package, variants):
  if package.getPackageStep().isValid():
    variantID = package.getPackageStep().getVariantId()
    if package.getName() not in variants:
      variants[package.getName()] = {variantID : package}
    else:
      va = variants[package.getName()]
      if variantID not in va:
        va[variantID] = package
  for d in package.getDirectDepSteps():
    getPackageVariants(d.getPackage(), variants)

def readList(filename):

  result = []

  if not os.path.isfile(filename):
    print('file ' + red(filename) + ' does not exist!')
    return result

  with open(filename, 'r') as f:
    for line in f:
      if not line.startswith('#'):
        l = line.rstrip()
        result.append(l)
  return result

def callOutput(array, workDirectory = "."):
  for attempts in range(RETRY_COUNT):
    try:
      output = subprocess.check_output(array, cwd = workDirectory)
      output_decoded = output.decode('UTF-8')
      output_stripped = output_decoded.rstrip()
      return output_stripped
    except OSError as ex:
      # raised when e.g. file does not exist
      print('OSError: ' + str(ex.strerror))
    except subprocess.CalledProcessError as ex:
      # raised on non-zero return value
      if attempts < RETRY_COUNT - 1:
        time.sleep(RETRY_TIMEOUT)
        continue
      else:
        print('call failed with return code ' + str(ex.returncode))
    break;

def isRelease(name):
  return name.startswith('release/')

def doMetaCheck(package, filemodulesname):

    prog = "git rev-parse --abbrev-ref HEAD"
    output = callOutput(prog.split(" "))
    if output:
      isReleaseBranch = isRelease(output)
    else:
      # call failed, assume we are not on release branch
      isReleaseBranch = False

    # map of package names to map of variantIDs to package
    variants = {}
    getPackageVariants(package, variants)

    metaVars = {}

    # read module list that we want to check
    modulelist = readList(filemodulesname)

    for package_name in variants:
      for variantid in variants[package_name]:
        cur_package = variants[package_name][variantid]
        metaenv = cur_package.getMetaEnv()
        package_name = cur_package.getName()
        if len(metaenv) > 0:
          metaVars[package_name] = metaenv
          # check source tag and module version
          # only for release branch
          if isReleaseBranch:
            if 'tsd-swupdate-' in package_name or 'tsd-pwc-mib3-updater' in package_name:
              module_version = metaenv['MODULE_VERSION']
              tag = ""
              same_version = False
              for scm in cur_package.getCheckoutStep().getScmList():
                if isinstance(scm, GitScm):
                  props = scm.getProperties()[0]
                  tag = props['tag']
                  if tag == module_version:
                    same_version = True
              if not same_version:
                print(red('ERROR: source tag (' + str(tag) + ') and module version (' + module_version + ') differ for ' + package_name))

    modules = {}
    for name in metaVars:
      _metaVars = metaVars[name]
      # filter zr3-variant
      if 'PACKAGE_VERSION' in _metaVars.keys():
        modules[name] = [_metaVars['PACKAGE_VERSION'], _metaVars['MODULE_VERSION']]

    # print versions according to order in module list
    keyset = modules.keys()
    usedkeys = []
    for i in modulelist:
      found = False
      for j in keyset:
         if j.startswith(i):
           found = True
           usedkeys.append(j)
      if not found:
         print(red('module from module list not found: ' + i))
    for i in usedkeys:
       print(i + ' ' + modules[i][0] + ' ' + modules[i][1])
       modules.pop(i)
    # print versions from modules not included in module list
    for i in modules.keys():
       print(red('module defines meta version, but is not in module list: ' + i))

def metaCheck(package, argv, extra):
    parser = argparse.ArgumentParser(prog='bob project metacheck', description='meta vars check')
    parser.add_argument('--modulenames', required=True, help='file containing list of module names')
    args = parser.parse_args(argv)
    filemodulesname = args.modulenames
    doMetaCheck(package, filemodulesname)

manifest = {
   'apiVersion' : '0.10',
   'projectGenerators' : {
      'metacheck' : metaCheck,
   }
}
