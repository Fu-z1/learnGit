#!/usr/bin/env python3
#
# author: Christoph Schwalbe
#
# Description: simple program to add in recipes the powercontroller version depending on powercontroller module git TAG
#
import ruamel.yaml
import ruamel.yaml.util
#from ruamel.yaml import YAML
#import yaml
from os import path
#
# simple usage for update powercontroller
# sudo pip uninstall ruamel.yaml
# sudo pip install ruamel.yaml==0.15.35
# and run in contrib folder! even if relpath is used
# run with: python3 update_package.py
#


def open_yaml(filepart):
   filepath_base = '../'
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



def check_package():
   file1 = open_yaml('recipes/system/tsd-pwc-mib3-image.yaml')   # tag
   file2 = open_yaml('recipes/zr3-variant.yaml')                 # PWC_VERSION
   file3 = open_yaml('recipes/system/tsd-pwc-mib3-updater.yaml') # MODULE_VERSION PACKAGE_VERSION
   module_tag = ''
   pwc_version = ''
   module_version = ''
   package_version = ''

   # tag in module, if changed, change it also in file2 and file3
   for i in file1:
      if 'checkoutSCM' in i:
         #print(file1['checkoutSCM'])
         if 'tag' in file1['checkoutSCM']:
            print('tag: {}'.format(file1['checkoutSCM']['tag']))
            module_tag = file1['checkoutSCM']['tag']

   if module_tag != '':

    for i in file2:
      if 'environment' in i:
         #print(file2['environment'])
         if 'PWC_VERSION' in file2['environment']:
            print('pwc_version: {}'.format(file2['environment']['PWC_VERSION']))
            pwc_version = file2['environment']['PWC_VERSION']

    for i in file3:
      if 'metaEnvironment' in i:
         #print(file3['metaEnvironment'])
         if 'MODULE_VERSION' in file3['metaEnvironment'] and 'PACKAGE_VERSION' in file3['metaEnvironment']:
            print('package_version: {}'.format(file3['metaEnvironment']['PACKAGE_VERSION']))
            print('module_version: {}'.format(file3['metaEnvironment']['MODULE_VERSION']))
            module_version = file3['metaEnvironment']['PACKAGE_VERSION']
            package_version = file3['metaEnvironment']['MODULE_VERSION']

    collect_numbers = [module_tag, pwc_version, module_version, package_version]
    check = all(tag_number == module_tag for tag_number in collect_numbers)
    if check == False:
      file2['environment']['PWC_VERSION'] = module_tag
      file3['metaEnvironment']['PACKAGE_VERSION'] = module_tag
      file3['metaEnvironment']['MODULE_VERSION'] = module_tag
      print("writting to files")
      write_yaml('recipes/zr3-variant.yaml', file2)
      write_yaml('recipes/system/tsd-pwc-mib3-updater.yaml', file3)

check_package()
