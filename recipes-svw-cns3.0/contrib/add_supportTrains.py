#!/usr/bin/python
# -*- coding:utf-8 -*-
# Filename:add_supportTrains.py

import os
import datetime
import sys
import re
import argparse

def get_calender_week():
    current_time = datetime.datetime.now().isocalendar()
    current_year = str(current_time[0])
    current_week = current_time[1]
    if current_year == '2018':
        real_week = str(current_week).zfill(3)
    elif current_year == '2019':
        real_week = str(current_week + 53).zfill(3)
    elif current_year == '2020':
        real_week = str(current_week + 105).zfill(3)
    return real_week

def analyze_variant(file, platform, *args):
    if len(args) >= 1:
        current_week = '\\"*_?%s*\\"'%(str(args[0]).zfill(3))
    else:
        current_week = '\\"*_?%s*\\"'%get_calender_week()
    f = open(file).read()
    format = 'if\s\[\[\s\"\$\{PLATFORM\}\"\s\s==\s\"%s\"\s\]\]\;\sthen\s*SUPPORTED_TRAINS_STRING=\"\[\S*?\]\"'%platform
    rx = re.findall(format, f)
    if rx:
        platform_info = rx[0].split('SUPPORTED_TRAINS_STRING=')[0]
        info = rx[0].split('SUPPORTED_TRAINS_STRING=')[1]
        print info
        info_list = info[2:-2].split(',')
        if current_week in info_list:
            print ">> \033[92m%s is already involved\033[0m"%current_week
        else:
            print ">> \033[91m%s is not involved\033[0m"%current_week
            info_list.append(current_week)
            new_info = '"[' + ",".join(info_list) + ']"'
            print ">> \033[92mnew info is %s\033[0m"%new_info
            origin = open(file).read()
            new_message = platform_info + 'SUPPORTED_TRAINS_STRING=' + new_info
            out = origin.replace(rx[0], new_message)
            f1=open(file,'w+')
            f1.write(out)
            f1.close()

if __name__ == "__main__":
    cwd = sys.path[0]
    root_dir = os.path.dirname(cwd)
    
    parser = argparse.ArgumentParser(description='Add SupportTrains Number')
    parser.add_argument("-p", "--platform", required=True, type=str, choices=['MQB', '37W'],
                         help="Build Platform")
    parser.add_argument("-y", "--yaml", required=True, type=str, help="The yaml file to be edit")
    parser.add_argument("-v", "--version", type=str, help="Force a version number manually")

    args = parser.parse_args()
    platform_name = args.platform
    variant_yaml = os.path.join(root_dir, 'recipes', args.yaml)
    force_version = ""
    if args.version:
        force_version = args.version
        analyze_variant(variant_yaml, platform_name, force_version)
    else:
        analyze_variant(variant_yaml, platform_name)

