#!/usr/bin/python
# -*- coding:utf-8 -*-
# Filename:push2branch.py
# python push2branch.py -b release/svw_cns3.0_r1 -m git@cnninvmgtlb01:manifest/manifest-svw-cns3.0-android.git -a

import os
import sys
import shutil
import re
import argparse
import requests

def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)

def write_file(file, dict):
    f = open(file).read()
    out = multiple_replace(f,dict)
    f1 = open(file,'w+')
    f1.write(out)
    f1.close()

def replace_version(f, branch):
    replace_dict = {".eng." : ".usr."}
    file = open(f).read()
    format = 'TARGET_VERSION:.*'
    rx=re.findall(format,file)
    old_version = rx[0].split(' ')[1]
    old_branch  = old_version.rstrip('.' + ".".join(old_version.split('.')[-3:]))
    new_branch = branch
    replace_dict[old_branch] = new_branch
    print ">> %s"%old_branch
    print ">>   %s"%new_branch
    out = multiple_replace(file, replace_dict)
    f1=open(f,'w+')
    f1.write(out)
    f1.close()

def git_push(path, branch):
    os.chdir(path)
    if os.system('git add .'):
        print ">> \033[91mgit add failed\033[0m"
        sys.exit(-1)
    os.system('git commit -m\"%REM% update version to adapt release branch\"')
    os.system('git checkout -b mybranch')
    os.system('git status')
    os.system('git push origin HEAD:%s'%branch)

def push_to_manifest(url, path, scm_url, commit, branch):
    if os.path.exists(path):
        print ">> \033[93m%s exists, deleting\033[0m"%path
        shutil.rmtree(path)
    if os.system('git clone %s %s'%(url, path)):
        print ">> \033[91mgit clone %s failed\033[0m"%url
        sys.exit(-1)
    os.chdir(path)
    if os.system('git remote add scm %s'%(scm_url)):
        print ">> \033[91mgit remote add %s failed\033[0m"%scm_url
        sys.exit(-1)
    os.system('git fetch scm')
    if os.system('git checkout -b mybranch %s'%(commit)):
        print ">> \033[91mgit checkout failed\033[0m"
        sys.exit(-1)
    if os.system('git push origin HEAD:%s'%(branch)):
        print ">> \033[91mgit push failed\033[0m"
        sys.exit(-1)

if __name__ == "__main__":
    cwd = sys.path[0]
    root_dir = os.path.dirname(cwd)
    manifest_dir = os.path.join(os.path.dirname(root_dir), 'cns_manifest')
    commit_file = os.path.join(root_dir, 'commit.txt')
    
    version_recipe = os.path.join(root_dir, 'recipes', 'system', 'target-version.yaml')
    android_recipe = os.path.join(root_dir, 'recipes', 'system', 'bsp', 'ext-renesas-h3-android.yaml')
    
    parser = argparse.ArgumentParser(description='Process Snapshot')
    parser.add_argument("-b", "--branch", type=str, required=True, help="Release branch name")
    parser.add_argument("-a", "--android", action='store_true', help="Judge if there is changes for android")
    parser.add_argument("-m", "--manifest", type=str, required=True, help="manifest git url")
    args = parser.parse_args()
    
    release_branch = ''
    if args.branch:
        release_branch = args.branch
    android_status = args.android
    manifest_url= args.manifest
    
    replace_version(version_recipe, release_branch)
    
    if android_status:
        print "\033[95m==========================Android Checking==========================\033[0m"
        f = open(android_recipe).read()
        format_temp = '(repo\sinit\s-u\s(([\s\S]*?)\s-b\s(.*)?))'
        rx_temp = re.findall(format_temp, f)
        ref_info = rx_temp[0][1]
        scm_url = rx_temp[0][2]
        commit = ref_info.split(" ")[-3]
        new_info = "%s -b %s -m manifest.xml"%(manifest_url, release_branch)
        rep_dict = {ref_info:new_info, "commit: %s"%commit : "branch: %s"%release_branch}
        for i in rep_dict:
            print ">>  %s"%i
            print ">>   %s"%rep_dict[i]
        write_file(android_recipe, rep_dict)
        push_to_manifest(manifest_url, manifest_dir, scm_url, commit, release_branch)
        print "\033[95m===========================Android Ending===========================\033[0m"

    git_push(root_dir, release_branch)
    if android_status:
        os.system('echo %s > %s'%(commit, commit_file))
