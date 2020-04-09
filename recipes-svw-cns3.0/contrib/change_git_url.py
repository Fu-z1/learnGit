#!/usr/bin/python
import re
import os
import sys
import subprocess as sp
import argparse

def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)

def grep_r_string(string):
    cfg = []
    cmd = ['grep', '-r', string]
    out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    while True:
        line = out.stdout.readline()
        if not line:
                break
        info = line.strip()
        dir_path = info.split(":")[0]
        cfg.append(dir_path)
    return set(cfg)

def execute_replace(dir, string, rep):
    os.chdir(dir)
    adic = {string:rep}
    info = grep_r_string(string)
    for filename in info:
        print filename
        f = open(filename).read()
        out = multiple_replace(f, adic)
        f1 = open(filename, 'w+')
        f1.write(out)
        f1.close()

def list_dir(list, string, rep):
    for i in list:
        path = os.path.join(root_dir, i)
        execute_replace(i, string, rep)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replace git url to variable')
    parser.add_argument("-r", "--revert", action="store_true", help="revert replacement of gitlab url")
    args = parser.parse_args()
    
    origin_info = "git.mib3.technisat-digital"
    rep_info = '${DEFAULT_PCC_GIT_SERVER}'
    if args.revert:
        origin_info = '${DEFAULT_PCC_GIT_SERVER}'
        rep_info = "git.mib3.technisat-digital"

    cwd = sys.path[0]
    replace_list = []
    root_dir = os.path.dirname(cwd)
    for f in os.listdir(root_dir):
        if f not in ['.git', 'dev', 'work', 'contrib']:
            if os.path.isdir(os.path.join(root_dir, f)):
                replace_list.append(os.path.join(root_dir, f))
    list_dir(replace_list, origin_info, rep_info)
