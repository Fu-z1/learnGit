#!/usr/bin/python
# -*- coding:utf-8 -*-
# Filename:build.py

import os
import sys
import subprocess as sp
import yaml
import re
import datetime
import time
import argparse

def get_calender_week():
    current_time = datetime.datetime.now().isocalendar()
    current_year = str(current_time[0])
    current_week = current_time[1]
    if current_year == '2018':
        real_week = str(current_week)
    elif current_year == '2019':
        real_week = str(current_week + 53)
    elif current_year == '2020': 
        real_week = str(current_week + 105)
    return real_week

def get_time(ISOTIMEFORMAT):
    current_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    return current_time

def get_old_info(file, info_list):
    dict = {}
    f = open(file).read()
    info = yaml.load(f)
    if info.has_key('environment'):
        for i in info['environment']:
            for j in info_list:
                if i == j:
                    key_name = i.split("_")[-1]
                    dict[key_name] = info['environment'][i]
    return dict

def get_new_info(file, info_list, *args):
    new_dict = {}
    old_dict = get_old_info(file, info_list)
    print old_dict
    cw = get_calender_week()
    if "MAP_MAJOR" in info_list:
        cw = str(int(old_dict['MAJOR']) +1).zfill(3)
    old_major = old_dict['MAJOR']
    old_delivery = old_dict['DELIVERY']
    old_buildref = old_dict['BUILDREF']
    if len(args) >= 1:
        new_major = str(args[0]).zfill(3)
    else:
        new_major = cw.zfill(3)
    if new_major == old_major:
        new_buildref = str(int(old_buildref) + 1)
    else:
        new_buildref = "1"
    new_dict['MAJOR'] = new_major
    new_dict['DELIVERY'] = old_delivery
    new_dict['BUILDREF'] = new_buildref
    return new_dict

def analyze_version(version_file):
    version_f = open(version_file).read()
    version_info = yaml.load(version_f)
    if version_info.has_key('environment'):
        TARGET_VERSION = version_info['environment']['TARGET_VERSION']
    return TARGET_VERSION

def replace_info(file, info_list, *args):
    dict1 = get_old_info(file, info_list)
    if len(args) >= 1:
        dict2 = get_new_info(file, info_list, args[0])
    else:
        dict2 = get_new_info(file, info_list)
    replace_dict = {"%s: \"%s\""%(info_list[0], dict1['MAJOR'])    : "%s: \"%s\""%(info_list[0], dict2['MAJOR']),
                    "%s: \"%s\""%(info_list[1], dict1['DELIVERY']) : "%s: \"%s\""%(info_list[1], dict2['DELIVERY']),
                    "%s: \"%s\""%(info_list[2], dict1['BUILDREF']) : "%s: \"%s\""%(info_list[2], dict2['BUILDREF'])}
    execute_replace(file, replace_dict)

def execute_replace(file, dict):
    for j in dict:
        print ">> %s"%j
        print ">>   %s"%dict[j]
    yaml_read = open(file).read()
    out = multiple_replace(yaml_read, dict)
    f=open(file,'w+')
    f.write(out)
    f.close()

def multiple_replace(text, adict):
    rx = re.compile(r'\b%s' % r'|\b'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)

def get_branch():
    cmd = ['git', 'branch']
    out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    while True:
        line = out.stdout.readline()
        if not line:
            break
        if (line.startswith('*')):
            info = ((line.strip()).split(' '))[-1]
            return info

def replace_version(file, form):
    replace_dict = {}
    old_version = analyze_version(file)
    old_info    = old_version.split('.')
    old_type    = old_info[-3]
    old_date    = old_info[-2]
    old_num     = old_info[-1]
    suffix_len = len('.'+'.'.join([old_type,old_date,old_num]))
    old_branch = old_version[:-suffix_len]

    new_date = get_time('%Y%m%d')
    new_branch = get_branch()
    new_num = '1'
    if form == "weekly":
        new_type = 'usr'
    else:
        new_type = 'eng'

    if (new_branch == old_branch):
        if new_date == old_date:
            new_num = str(int(old_num) + 1)
    new_version = '.'.join([new_branch, new_type, new_date, new_num])

    new_version_info = 'TARGET_VERSION: %s'%new_version
    old_version_info = 'TARGET_VERSION: %s'%old_version
    replace_dict[old_version_info] = new_version_info
    for j in replace_dict:
        print ">> %s"%j
        print ">>   %s"%replace_dict[j]
    yaml_read = open(file).read()
    out = multiple_replace(yaml_read, replace_dict)
    f1=open(file,'w+')
    f1.write(out)
    f1.close()
    return new_version

def git_push_version(dir, version, branch):
    os.chdir(dir)
    if os.system('git add recipes\/'):
        print ">> Git Add Fail!"
        sys.exit(-1)
    
    os.system('git status')
    if os.system('git commit -m\"%%REM%% update version to %s\"'%version):
        print ">> Git Commit Fail!"
        sys.exit(-1)

    if os.system('git push origin HEAD:%s'%branch):
        print ">> Git Push Fail!"
        sys.exit(-1)

def git_tag(dir, tag):
    os.chdir(dir)
    if os.system('git add recipes\/'):
        print ">> Git Add Fail!"
        sys.exit(-1)
    os.system('git status')
    if os.system('git commit -m\"%%REM%% snapshot for %s\"'%tag):
        print ">> Git Commit Fail!"
        sys.exit(-1)
    
    if os.system('git tag %s'%tag):
        print ">> Git Tag Fail!"
        sys.exit(-1)
    if os.system('git push origin %s'%tag):
        print ">> Git Push Tag Fail!"
        sys.exit(-1)
    if os.system('git checkout %s'%tag):
        print ">> Checkout %s failed!"%tag
    else:
        print ">> Checkout %s succeed!"%tag

if __name__ == "__main__":
    path_dict = {'daily':'daily_build',
                 'weekly':'weekly_release',
                 'customer':'customer_release',
                 'temp':'temp_release'}
    platform_path_dict = {'MQB' : 'cns-c-sample', '37W' : '37w-b0-sample'}

    parser = argparse.ArgumentParser(description='Process SW building')
    parser.add_argument('package', nargs='+', help="Sub-package that is the root of the project")
    parser.add_argument("-f", "--form", required=True, type=str, choices=['daily', 'weekly', 'customer', 'temp'],
                         help="Build Form")
    parser.add_argument('-D', default=[], action='append', dest="defines",
                        help="Override default environment variable")
    parser.add_argument("-s", "--suffix", type=str, help="Add tag suffix if needed")
    parser.add_argument("-t", "--tag", action="store_true", help="Judge if push tag to remote")
    parser.add_argument("-v", "--version", type=str, help="Force a version number manually")
    parser.add_argument("-y", "--yaml", required=True, default=[], action='append', help="Choose which yaml to be changed")
    parser.add_argument("-p", "--platform", required=True, type=str, choices=['MQB', '37W'],
                         help="Build Platform")
    args = parser.parse_args()
    
    force_version = ""
    if args.version:
        force_version = args.version
    
    yaml_list = args.yaml
    print yaml_list
    
    build_form = args.form
    if isinstance(args.package, list):
        packages = ' '.join(args.package)
    else:
        packages = args.package
    defines = ""
    if args.defines:
        defines = " ".join(['-D'+x for x in args.defines])
    tag_suffix = args.suffix
    push_tag = args.tag
    platform = args.platform 
    cwd = sys.path[0]
    root_dir = os.path.dirname(cwd)
    current_branch = get_branch()
    buildref_yaml = os.path.join(root_dir, 'recipes', 'zr3.yaml')
    version_yaml = os.path.join(root_dir, 'recipes', 'system', 'target-version.yaml')
    os.chdir(root_dir)
    
    new_version = replace_version(version_yaml, build_form)

    if "zr3-variant.yaml" in yaml_list:
        INFO_LIST = ["MAJOR", "DELIVERY", "BUILDREF"]
    elif "zr3-navimap.yaml" in yaml_list:
        INFO_LIST = ["MAP_MAJOR", "MAP_DELIVERY", "MAP_BUILDREF"]
    
    if not build_form == 'daily':
        if force_version:
            new_info_dict = get_new_info(buildref_yaml, INFO_LIST, force_version)
            for yaml_file in yaml_list:
                print yaml_file
                variant_yaml = os.path.join(root_dir, 'recipes', yaml_file)
                os.system("python contrib/add_supportTrains.py -p %s -y %s -v %s"%(platform, yaml_file, force_version))
            replace_info(buildref_yaml, INFO_LIST, force_version)
        else:
            new_info_dict = get_new_info(buildref_yaml, INFO_LIST)
            for yaml_file in yaml_list:
                print yaml_file
                variant_yaml = os.path.join(root_dir, 'recipes', yaml_file)
                os.system("python contrib/add_supportTrains.py -p %s -y %s -v %s"%(platform, yaml_file, new_info_dict['MAJOR']))
            replace_info(buildref_yaml, INFO_LIST)
    
        if tag_suffix:
            tag_number = new_info_dict['MAJOR'].zfill(3) + new_info_dict['DELIVERY'] + '-rc' + new_info_dict['BUILDREF'] + '-' + tag_suffix
        else:
            tag_number = new_info_dict['MAJOR'].zfill(3) + new_info_dict['DELIVERY'] + '-rc' + new_info_dict['BUILDREF']
        print ">> NEW    TAG: %s"%tag_number

    git_push_version(root_dir, new_version, current_branch)
    os.system('python contrib\/gitlog.py -f %s %s %s'%(build_form, defines, packages))
    os.system('python contrib\/create_snapshot.py %s %s'%(defines, packages))

    if push_tag:
        git_tag(root_dir, tag_number)

    os.system('echo \"%s\" > version.txt'%new_version)

    remote_path = os.path.join('/var', 'www', platform_path_dict[platform], 'linux', path_dict[build_form])
    if (build_form == "weekly"):
        real_dir_name = (".".join(new_version.split(".")[-2:])) + "_" + tag_number
    elif (build_form == "temp"):
        real_dir_name = new_version.replace("/", "-")
    else:
        real_dir_name = ".".join(new_version.split(".")[-2:])
    remote_dir = os.path.join(remote_path, real_dir_name)
    os.system('echo \"%s\" > dir.txt'%remote_dir)
