#!/usr/bin/python
# -*- coding:utf-8 -*-
# Filename:create_snapshot.py

import re
import os
import sys
import yaml
import argparse
import threading
from string import Template
from libs import Bob
from libs import Gitlab


def multiple_replace(text, replace_cfg):
    #rx = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, replace_cfg)))
    rx = re.compile('|'.join(map(re.escape, replace_cfg)))
    def get_match(match):
        return replace_cfg[match.group(0)]
    return rx.sub(get_match, text)

def replace_global_var(file, orig_url):
    ret_url = unicode(orig_url)
    default_env = {'DEFAULT_PCC_GIT_SERVER'        :'10.57.9.150',
                   'DEFAULT_JPCC_GIT_SERVER'       :'10.57.9.151',
                   'DEFAULT_JPCC_MODIFY_GIT_SERVER':'10.57.9.150'}
    f = open(file).read()
    match_url = re.findall('(.*)url\:\s*[\"\']?(\S*)[\"\']?\s', f)
    yaml_org = yaml.load(f)
    if yaml_org.has_key('environment'):
        yaml_env = yaml_org['environment']
        env = dict(default_env, **yaml_env)
    else:
        env = default_env
    for item in match_url:
        if not "#" in item[0]:
            val = Template(item[1]).safe_substitute(env)
            if orig_url == val:
                ret_url = unicode(item[1])
    return ret_url

def get_commit_of_revision(url, rev):
    prj = (url.split(":")[-1])[:-4]
    if "10.57.9.151" in url or "cnninvmgtlb01" in url:
        cmt = gitlab01api.get_latest_commit(prj, rev)
    else:
        cmt = gitlab02api.get_latest_commit(prj, rev)
    return cmt

def sort_scms(scms):
    s = {'tag':{},'branch':{}}
    for i in scms:
        if 'scm' in i.keys():
            for j in i['scm']:
                if j['scm'] == 'git':
                    recipe = j['recipe'].split('#')[0]
                    enum = int(j['recipe'].split('#')[1]) + 1
                    url = j['url']
                    if j['tag'] and not j['commit']:
                        if not s['tag'].has_key(recipe):
                            s['tag'][recipe] = []
                        info = {'url':url, 'rev':j['tag'], 'enum':enum}
                        if not info in s['tag'][recipe]:
                            s['tag'][recipe].append(info)
                    elif j['branch'] and not j['tag'] and not j['commit']:
                        if not s['branch'].has_key(recipe):
                            s['branch'][recipe] = []
                        info = {'url':url, 'rev':j['branch'], 'enum':enum}
                        if not info in s['branch'][recipe]:
                            s['branch'][recipe].append(info)
    return s

def get_config(pkg, define):
    origin_dict = bob.project(pkg, define)
    config_dict = sort_scms(origin_dict)
    return config_dict

def execute_replace(threadname, config, rev_type, verbose=False):
    for line in config:
        for k, v in line.items():
            #recipe = os.path.join(root_dir, k)
            recipe = k
            cmt_dict = replace_revision(recipe, v, rev_type)
            if verbose:
                for i in v:
                    url    = i['url']
                    rev    = i['rev']
                    enum   = i['enum']
                    commit = cmt_dict[url][enum]
                    
                    print(">> \033[92m%s recipe: %s\033[0m"%(threadname, recipe))
                    print(">>   url   : %s"%url)
                    if commit:
                        print(">>   %s: %s --> commit: %s\n"%(rev_type.ljust(6,' '), rev, commit))
                    else:
                        print('No Commit available for this URL and %s\n'%rev_type)

def handle_duplicate_gits(scm, recipe, commits, type):
    f = open(recipe).read()
    format = ""
    adict = {}
    rep_dict = {}
    scm.sort(key=lambda a:a['enum'])
    for i in range(len(scm)):
        url    = scm[i]['url']
        rev    = scm[i]['rev']
        enum   = scm[i]['enum']
        commit = commits[url][enum]
        match_url = replace_global_var(recipe, url)
        format += 'url\:\s*%s[\s\S]*?((rev|%s)\:\s*(%s)\s)[\s\S]*?'%(re.escape(match_url),type, re.escape(rev))
    rx = re.findall("(" + format + ")", f)
    if rx:
        info = rx[0][0]
        for i in range(1, len(rx[0]), 3):
            revisions = rx[0][i]
            for j in range(len(scm)):
                url    = scm[j]['url']
                rev    = scm[j]['rev']
                enum   = scm[j]['enum']
                commit = commits[url][enum]
                if "%s\n"%rev in revisions or "%s "%rev in revisions:
                    adict[revisions] = "commit: " + commit + "\n"
        if adict:
            rep_dict[info] = multiple_replace(info,adict)
    if rep_dict:
        out = multiple_replace(f, rep_dict)
        f1 = open(recipe,'w+')
        f1.write(out)
        f1.close()
    else:
        print ">>   \033[91mThere is an error with the script!\033[0m"
        sys.exit(-1)

def replace_revision(recipe, list, rev_type):
    f = open(recipe).read()
    rep_dict = {}
    retcommit = {}
    DUPLICATE = 0
    for i in list:
        url    = i['url']
        rev    = i['rev']
        enum   = i['enum']
        commit = get_commit_of_revision(url, rev)
        if not retcommit.has_key(url):
            retcommit[url] = {}
        retcommit[url][enum] = commit
        match_url = replace_global_var(recipe, url)
        url_format = '.+(url\:\s*%s)'%(re.escape(match_url))
        rx0 = re.findall(url_format, f)
        if len(rx0) >= 2:
            print "\033[93mWarning: Found two or more same gits in %s!\033[0m"%recipe
            DUPLICATE = 1
        else:
            format = '.+(url\:\s*%s[\s\S]*?((rev|%s)\:\s*(%s))\s+)'%(re.escape(match_url),rev_type, re.escape(rev))
            rx = re.findall(format, f)
            if rx:
                info = rx[0][0]
                adict = {rx[0][1] : 'commit: %s'%commit}
                if match_url == "git@${DEFAULT_JPCC_GIT_SERVER}:svw-integration/scm.android.git":
                    format_temp = '(repo\sinit\s-u\s(([\s\S]*?)\s-b\s(.*)?))'
                    rx_temp = re.findall(format_temp, f)
                    rep_dict[rx_temp[0][1]] = "%s -b %s -m manifest.xml"%(url, commit)
            elif not rx:
                format1 = '.+(url\:\s*%s[\s\S]*?((rev|%s)\:\s*(\S*))\s+)'%(re.escape(match_url),rev_type)
                rx1 = re.findall(format1, f)
                if rx1:
                    adict = {rx1[0][1] : 'commit: %s'%commit}
                    info = rx1[0][0]
                elif not rx1:
                    print ">>   \033[91mfind no revision\033[0m"
                    with open(recipe, "r+") as filein:
                        for line in filein:
                            if match_url in line:
                                info = line
                                realURL = re.search(r'(.*)url: (.+?)$', line, re.M|re.I)
                                gap = realURL.group(1)
                                replaceText = line + gap + 'commit: ' + commit + '\n'
                                adict = {info:replaceText}
            rep_dict[info] = multiple_replace(info,adict)
    if rep_dict:
        out = multiple_replace(f, rep_dict)
        f1 = open(recipe,'w+')
        f1.write(out)
        f1.close()
    else:
        if DUPLICATE:
            handle_duplicate_gits(list, recipe, retcommit, rev_type)
        else:
            print ">>   \033[91mThere is an error with the script!\033[0m"
            sys.exit(-1)
    return retcommit

def generate_snapshot(scm_info, rev_type):
    threadList = []
    for k, v in scm_info.items():
        threadList.append({k:v})
    execute_replace('thread-0', threadList, rev_type, args.verbose)

if __name__ == "__main__":
    THREAD_COUNT = 4
    cwd = sys.path[0]
    root_dir = os.path.dirname(cwd)
    bob = Bob.BobFunction(root_dir)
    gitlab01api = Gitlab.GitlabAPI('http://cnninvmgtlb01/', 'rdyDjp1ymkzWV_HKcgbC')
    gitlab02api = Gitlab.GitlabAPI('http://cnninvmplrn01/', 'UfnvvkokKmavXg3Q3Egy')
    
    parser = argparse.ArgumentParser(description='Process Snapshot')
    parser.add_argument('package', nargs='+', help="Sub-package that is the root of the project")
    parser.add_argument('-n', dest="nproc", required=False, help="#CPU", type=int)
    parser.add_argument('-t', dest="type", help="Revision Type need to create snapshot", 
                        type=str, default="branch", choices=['branch', 'tag'])
    parser.add_argument('-v', dest="verbose", default=True, action='store_true', help="Verbose")
    parser.add_argument('-D', default=[], action='append', dest="defines",
                        help="Override default environment variable")
    args = parser.parse_args()
    
    define = ""
    if args.defines:
        define = " ".join(['-D'+x for x in args.defines])
    if isinstance(args.package, list):
        packages = ' '.join(args.package)
    else:
        packages = args.package
    if args.nproc:
        THREAD_COUNT = args.nproc
    revision_type = args.type
    
    cfg = get_config(packages, define)
    rev_scm = cfg[revision_type]
    generate_snapshot(rev_scm, revision_type)

