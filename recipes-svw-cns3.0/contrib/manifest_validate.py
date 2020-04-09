#!/usr/bin/python 
# -*- coding:utf-8 -*-
# Filename:manifest_validate.py

import os
import sys
import subprocess as sp
import argparse


def validate(uc_path, vh_path, ri_path):
    e = 0
    cmd = ["./mib3-validate", "validate", "--updatecontainer", uc_path, "--variants-helper", vh_path, "--release-info", ri_path, "--moduleDepth"]
    out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    info= out.stdout.readlines()
    error_msg = ["ERROR: validating module name", 
                 "ERROR: module - name longer than 31 characters:"]
    for line in info:
        print line.strip()
        if error_msg[0] in line or error_msg[1] in line:
            e = 1
    return e

def git_clone(url, branch, path):
    if os.path.exists(path):
        print ">> \033[93m%s exists\033[0m"%path
    else:
        if os.system('git clone %s -b %s %s'%(url, branch, path)):
            print ">> \033[91mgit clone %s failed\033[0m"%url
        else:
            print ">> \033[93mclone %s\n\033[0m"%url

if __name__ == "__main__":
    cwd = sys.path[0]
    root_dir = os.path.dirname(cwd)
    parent_dir = os.path.dirname(root_dir)

    parser = argparse.ArgumentParser(description='Validate Manifest')
    parser.add_argument('path', type=str, help="Path need to be checked")
    args = parser.parse_args()
    
    updatecontainer_path = args.path
    
    varianthelper_path = os.path.join(root_dir, "plugins", "variants-helper.py")
    releaseinfo_path = os.path.join(cwd, "variants-helper", "release_info.json")
    
    if not os.path.exists(varianthelper_path):
        print "\033[91mvariants-helper.py doesn't exists!\033[0m"
        sys.exit(-1)
    
    if not os.path.exists(releaseinfo_path):
        print "\033[91mrelease_info.json doesn't exists!\033[0m"
        sys.exit(-1)
    
    validate_tool_path = os.path.join(parent_dir, "validate_tool")
    validate_tool_url = "git@cnninvmplrn01:mib3-integration/mib3.manifest.validate.git"
    git_clone(validate_tool_url, "4.1.0", validate_tool_path)
    
    os.chdir(validate_tool_path)
    print os.getcwd()
    result = validate(updatecontainer_path, varianthelper_path, releaseinfo_path)
    if result == 1 :
        print "\033[91mManifest validate failed!\033[0m"
        sys.exit(-1)
    else:
        print "\033[92mManifest validate succeeded!\033[0m"
