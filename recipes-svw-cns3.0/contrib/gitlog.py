#!/usr/bin/python
# -*- coding:utf-8 -*-
# Filename:create_snapshot.py
# python contrib/gitlog.py -f daily -DCONFIG_ANDROID=1 -DCONFIG_HYPERVISOR=1 -DCONFIG_XTENSA=1 zr3

import os
import re
import sys
import shutil
import simplejson as json
import subprocess as sp
import yaml
from string import Template
import re
import argparse
import requests
import datetime
import xlwt
from xlwt import *
import gitlab
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import codecs

def excel_to_html(excel):
    xd = pd.ExcelFile(excel)
    df = xd.parse()
    with codecs.open('gitlog.html','w','utf-8') as html_file:
         html_file.write(df.to_html(header = True,index = False))

def draw_pie_person(labels,quants,expl):
    plt.figure(1, figsize=(8,8))
    colors  = ["blue","red","coral","green","yellow","orange"]
    plt.pie(quants, explode=expl, colors=colors, labels=labels, autopct='%1.1f%%',pctdistance=0.8, shadow=True)
    plt.title('Top 10 Person Commits', bbox={'facecolor':'0.8', 'pad':5})
    plt.savefig("person.png")
    plt.close()

def draw_pie_role(labels,quants):
    plt.figure(1, figsize=(8,8))
    expl = [0.1,0,0] 
    colors  = ["blue","red","yellow"]
    plt.pie(quants, explode=expl, colors=colors, labels=labels, autopct='%1.1f%%',pctdistance=0.8, shadow=True)
    plt.title('Top 3 Role Commits', bbox={'facecolor':'0.8', 'pad':5})
    plt.savefig("role.png")
    plt.close()

def get_pie_dict(dict):
    rank_dict = {}
    num = 0
    for key,value in sorted(dict.iteritems(),key=lambda a:len(a[1]),reverse=True):
        if num < 10:
            rank_dict[key] = len(value)
        num += 1
    return rank_dict

RETRY_COUNT = 5
RETRY_TIMEOUT = 3 # seconds

class GitlabAPI:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        #self.gl = gitlab.Gitlab(self.url, self.token, api_version=3) #useless for group visibility
        self.gl = gitlab.Gitlab(self.url, self.token)
        
    def get_prj_list(self):
        prj_list = {}
        projects = self.gl.projects.list(all=True, as_list=False)
        for p in projects:
            prj_list[p.path_with_namespace] = p.id
        return prj_list

    def get_prj_id(self, prj):
        '''
        input full path of project
        '''
        prj_id = (self.gl.projects.get(prj)).id
        return prj_id
    
    def get_commit_time(self, prj, commit):
        '''
        input full path of project, the commit id
        '''
        project = self.gl.projects.get(prj)
        commits = project.commits.get(commit)
        return commits.committed_date
    
    def get_prj_commit(self, prj, br, start, end):
        '''
        input full path of project, branch name, the beginning time, the ending time
        '''
        commit_history = {}
        commit_history[prj] = []
        project = self.gl.projects.get(prj)
        commits = project.commits.list(all=True,ref_name=br, since=start, until=end)
        for i in range (len(commits)):
            user     = commits[i].author_name
            email    = commits[i].author_email
            title    = commits[i].title
            id       = commits[i].id
            date     = commits[i].committed_date

            commit_history[prj].append({"user"   :user, 
                                        "email"  :email, 
                                        "id"     :id, 
                                        "title"  :title, 
                                        "date"   :date,
                                        "branch" : br})
            
        return commit_history
    
    def list_branch(self, prj):
        prj_branch = {}
        prj_branch[prj] = []
        project = self.gl.projects.get(prj)
        branches = project.branches.list(all=True)
        for b in branches:
            prj_branch[prj].append(b.name)
        return prj_branch

    def create_branch(self, prj, br, ref):
        branch_list = self.list_branch(prj)
        if br not in branch_list[prj]:
            project = self.gl.projects.get(prj)
            branch = project.branches.create({'branch': br, 'ref': ref})
            print ">>   Create Branch : %s"%br
        else:
            print ">>   Branch %s already exists!!"%br

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

def get_file_from_git(root_path, url, branch, file):
    os.system('git archive --remote=%s --format=tar --prefix=manifest/ %s %s | (cd ../ && tar xf -)'%(url, branch, file))
    file_path = os.path.join(root_path, 'manifest', file)
    return file_path

def sortScms(scms, recipe_branch):
    s = {'gtlb01':{'svw-integration/recipes-svw-cns3.0':recipe_branch}, 'gtlb02':{}}
    for i in scms:
        if 'scm' in i.keys():
            for j in i['scm']:
                if j['scm'] == 'git':
                    if j['branch'] and not j['commit'] and not j['tag']:
                        prj = ((j['url'].split(':'))[-1])[:-4]
                        if j['url'].startswith('git@10.57.9.150') or j['url'].startswith('git@cnninvmplrn01'):
                            s['gtlb02'][prj] = j['branch']
                        elif j['url'].startswith('git@10.57.9.151') or j['url'].startswith('git@cnninvmgtlb01'):
                            s['gtlb01'][prj] = j['branch']
    return s

def bob_project(packages, recipe_branch, defines):
    filename = 'config.json'
    if not os.path.exists(filename):
        os.system('bob project ' + defines + ' -n json-config ' + packages)
    with open(filename, 'r') as f:
        json_dict = json.loads(f.read())
    if not json_dict:
        sys.stderr.write('File config.json not found!')
        return
    scmsSorted = sortScms(json_dict, recipe_branch)
    return scmsSorted

def arrange_dict(dict):
    usr_dict = {}
    for p in dict:
        for i in dict[p]:
            user   = i['user']
            email  = i['email']
            title  = i['title']
            id     = i['id']
            date   = i['date']
            branch = i['branch']
            if not usr_dict.has_key(user):
                usr_dict[user] = []
            if not (title).startswith('Merge branch'):
                usr_dict[user].append({"project":p, "email":email, "id":id, "subject":title, "commitDate":date, "branch":branch})
    return usr_dict

def arrange_role_dict(dict):
    role_dict = {'jpcc':0, 'pcc':0, 'amt':0}
    for p in dict:
        for i in dict[p]:
            email  = i['email']
            if email.endswith('preh.cn'):
                role_dict['jpcc'] += 1
            elif email.endswith('archermind.com'):
                role_dict['amt'] += 1
            elif email.endswith('preh.de'):
                role_dict['pcc'] += 1
    return role_dict

def excel_font(name,bold,ci,fc,border):
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.colour_index = ci

    pattern = xlwt.Pattern()
    pattern.pattern = 1
    pattern.pattern_fore_colour = fc

    alignment = Alignment()
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT

    borders = xlwt.Borders()
    borders.left = border
    borders.right = border
    borders.top = border
    borders.bottom = border
    borders.left_colour = 0x40
    borders.right_colour = 0x40
    borders.top_colour = 0x40
    borders.bottom_colour = 0x40

    style = XFStyle()
    style.pattern=pattern
    style.font = font
    style.alignment = alignment
    style.borders = borders

    return style

def style_form(format):
    if format == 'head':
        style = excel_font('Times New Roman',True,0,27,xlwt.Borders.MEDIUM)
    elif format == 'content':
        style = excel_font('Arial',False,0, 1,xlwt.Borders.THIN)
    return style

def add_wb(git_log_dict, name):
    global wb
    global ws
    wb = xlwt.Workbook(encoding = 'utf-8', style_compression=2)
    
    headline = ['PROJECT','BRANCH','NAME','EMAIL','ID','SUBJECT','commitDate']
    col_width = [30,30,20,25,40,30,30]
    add_sheet('git log', headline, col_width, 7, git_log_dict)

    wb.save('GitLog_%s.xls'%(name))

def add_sheet(sheet_name, head, column_width, num, list):
    row = 1
    ws = wb.add_sheet(sheet_name)
    for i in range(0,num):
        ws.write(0,i,head[i],style_form('head'))
        ws.col(i).width=256*column_width[i]
    
    for key,value in sorted(list.iteritems(),key=lambda a:len(a[1]),reverse=True):
        if num == 7:
            for element in value:
                ws.write(row,0,element['project'],style_form('content'))
                ws.write(row,1,element['branch'],style_form('content'))
                ws.write(row,2,key,style_form('content'))
                ws.write(row,3,element['email'],style_form('content'))
                ws.write(row,4,element['id'],style_form('content'))
                ws.write(row,5,element['subject'],style_form('content'))
                ws.write(row,6,element['commitDate'],style_form('content'))
                time_list.append(element['commitDate'])
                row = row+1
        elif num == 2:
            ws.write(row,0,key,style_form('content'))
            ws.write(row,1,value,style_form('content'))
            row = row+1

def transfer_to_isoTime(str):
    '''
    str is the version of android, such as '1812031501'
    return a iso time format, such as '2018-12-03T15:00:01.000+08:00'
    '''
    time_info = "20" + str
    iso_time = "%s.000+08:00"%datetime.datetime.strptime(time_info, "%Y%m%d%H%M%S").isoformat()
    return iso_time

def get_current_time_format(TIMEFORMAT):
    format = datetime.datetime.strftime(datetime.datetime.now(), TIMEFORMAT)
    return format

def get_last_cw():
    last_week_date = (datetime.date.today()-datetime.timedelta(days=7)).isocalendar()
    last_week = "0%s0"%str(last_week_date[1]).zfill(2)
    return last_week

def get_last_build_time(timefile, latest_info):
    if not os.path.exists(timefile):
        with open(timefile,'w') as time_file_tmp:
            time_file_tmp.write('"%s"\n'%latest_info)
        time_file_tmp.close()
    time_file = open(timefile,'r')
    lines = time_file.readlines()
    info = (lines[-1]).strip()
    time_file.close()
    return info

def append_new_build_time(timefile, time_str):
    if time_str:
        with open(timefile,'a') as time_data:
            time_data.write('%s\n'%time_str)
        time_data.close()
        print ">> \033[91mLatest commit time is %s\033[0m"%(time_str)
    else:
        print ">> \033[93mThere is not commit latest!\033[0m"

def git_clone(url, branch, path):
    if os.path.exists(path):
        print ">> \033[93m%s exists, deleting\033[0m"%path
        shutil.rmtree(path)
    if os.system('git clone %s -b %s %s'%(url, branch, path)):
        print ">> \033[91mgit clone %s failed\033[0m"%url
    else:
        print ">> \033[93mclone %s\n\033[0m"%url

def get_diff(sha1sum1, sha1sum2):
    prj_dict = {}
    start_time = end_time = ''
    if not (sha1sum1 == sha1sum2):
        cmd = ['git', 'diff', sha1sum1, sha1sum2, "manifest.xml"]
        out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
        info= out.stdout.readlines()
        for line in info:
            if (line.startswith("+")):
                if not (line.startswith("+++")):
                    project = ((line.strip()).split('name="')[1]).split('"')[0]
                    print project
                    branch = (line.strip()).split('upstream="')[-1].split('"')[0]
                    if not prj_dict.has_key(project):
                        prj_dict[project] = branch
        cmd2 = ['git', 'diff', sha1sum1, sha1sum2, "ECF"]
        out2 = sp.Popen(cmd2, stdout=sp.PIPE, stderr=sp.STDOUT)
        info2= out2.stdout.readlines()
        for line in info2:
            if (line.startswith("-TIMESTAMP")):
                start_time_str = (line.strip()).split("=")[-1]
                start_time = transfer_to_isoTime(start_time_str)
            elif (line.startswith("+TIMESTAMP")):
                end_time_str = (line.strip()).split("=")[-1]
                end_time = transfer_to_isoTime(end_time_str)
    else:
        start_time = end_time = get_current_time_format('%Y-%m-%dT%H:%M:%S.000+08:00')
    return prj_dict, start_time, end_time

def transfer_to_isoTime(str):
    '''
    str is the version of android, such as '1812031501'
    return a iso time format, such as '2018-12-03T15:00:01.000+08:00'
    '''
    time_info = "20" + str + "00"
    iso_time = "%s.000+08:00"%datetime.datetime.strptime(time_info, "%Y%m%d%H%M%S").isoformat()
    return iso_time

def get_current_commit(dir):
    os.chdir(dir)
    cmd = ['git', 'rev-parse', 'HEAD']
    out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    info= (out.stdout.readlines())[0].strip()
    return info

def git_push(dir, branch, form):
    os.chdir(dir)
    if os.system('git add .'):
        print ">> Git Add Fail!"
        sys.exit(-1)
    
    os.system('git status')
    if os.system('git commit -m\"%%REM%% update git log time for %s\"'%form):
        print ">> Git Commit Fail!"
        sys.exit(-1)

    if os.system('git push origin HEAD:%s'%branch):
        print ">> Git Push Fail!"
        sys.exit(-1)

if __name__ == "__main__":
    gtlb01_url = 'http://cnninvmgtlb01/'
    gtlb01_token = 'rdyDjp1ymkzWV_HKcgbC'
    gitlab01api = GitlabAPI(gtlb01_url, gtlb01_token)
    
    gtlb02_url = 'http://cnninvmplrn01/'
    gtlb02_token = 'UfnvvkokKmavXg3Q3Egy'
    gitlab02api = GitlabAPI(gtlb02_url, gtlb02_token)
    
    cwd = sys.path[0]
    root_dir = os.path.dirname(cwd)
    parent_dir = os.path.dirname(root_dir)
    current_branch = get_branch()
    (git_dict, cloc_dict, time_list,row,row2) = [{},{},[],3,3]
    current_time=get_current_time_format('%Y-%m-%d-%H-%M-%S')
    
    parser = argparse.ArgumentParser(description='Process Git Log')
    parser.add_argument('package', nargs='+', help="Sub-package that is the root of the project")
    parser.add_argument("-f", "--form", required=True, type=str, choices=['daily', 'weekly', 'customer', 'temp'],
                         help="Build Form")
    parser.add_argument('-D', default=[], action='append', dest="defines",
                        help="Override default environment variable")
    parser.add_argument("-s", "--suffix", type=str, help="Add tag suffix if needed")
    args = parser.parse_args()
    if isinstance(args.package, list):
        packages = ' '.join(args.package)
    else:
        packages = args.package
    if args.form:
        linux_time_file = '_'.join(['linux', args.form])
        print "Linux Time file is %s"%linux_time_file
        android_time_file = '_'.join(['android', args.form])
        print "Android Time file is %s"%android_time_file
    defines = ""
    if args.defines:
        defines = " ".join(['-D'+x for x in args.defines])
    time_url = "git@cnninvmgtlb01:svw-integration/git-log-time.git"
    time_path = os.path.join(parent_dir, "time")
    gitlab01api.create_branch("svw-integration/git-log-time", current_branch, "master")
    git_clone(time_url, current_branch, time_path)
    #Get linux dict
    print "\033[93m=========================Linux Checking=========================\033[0m"
    linux_time_path = os.path.join(time_path, linux_time_file)
    commit_time=get_current_time_format('%Y-%m-%dT%H:%M:%S.000+08:00')
    linux_time = get_last_build_time(linux_time_path, commit_time)
    print "\033[92mLinux last commit time is   :%s\033[0m"%linux_time
    print "\033[92mLinux current commit time is:%s\033[0m"%commit_time
    info_dict = bob_project(packages, current_branch, defines)
    #print info_dict
    for gtlb in info_dict:
        for prj in info_dict[gtlb]:
            print ">> \033[91m%s\033[0m"%prj
            branch = info_dict[gtlb][prj]
            print ">>   %s"%branch
            if gtlb == 'gtlb01':
                commit_dict = gitlab01api.get_prj_commit(prj, branch, linux_time, '')
            else:
                commit_dict = gitlab02api.get_prj_commit(prj, branch, linux_time, '')
            git_dict = dict(git_dict, **commit_dict)
    print "\033[93m=========================Linux ending==========================\033[0m"
    #Get Android dict

    if info_dict['gtlb01'].has_key("svw-integration/scm.android"):
        print "\033[94m=========================Android Checking=========================\033[0m"
        android_time_path = os.path.join(time_path, android_time_file)
        android_git = "git@cnninvmgtlb01:svw-integration/scm.android.git"
        android_branch = info_dict['gtlb01']["svw-integration/scm.android"]
        android_path = os.path.join(parent_dir, "android")
        git_clone(android_git, android_branch, android_path)
        latest_android_commit = get_current_commit(android_path)
        last_android_commit = get_last_build_time(android_time_path,latest_android_commit)
        os.chdir(android_path)
        (android_dict, android_start, android_end) = get_diff(last_android_commit, latest_android_commit)
        print "\033[92mAndroid last commit time is   :%s\033[0m"%android_start
        print "\033[92mAndroid current commit time is:%s\033[0m"%android_end
        for prj in android_dict:
            print ">> \033[91m%s\033[0m"%prj
            branch = android_dict[prj]
            print ">>   %s"%branch
            android_commit_dict = gitlab01api.get_prj_commit(prj, branch, android_start, android_end)
            git_dict = dict(git_dict, **android_commit_dict)
        print "\033[94m=========================Android Ending==========================\033[0m"
        append_new_build_time(android_time_path, latest_android_commit)
    elif not info_dict['gtlb01'].has_key("svw-integration/scm.android"):
        print "\033[94m=========================No Android change=========================\033[0m"
        android_recipe = os.path.join(root_dir, "recipes","system","bsp","ext-renesas-h3-android.yaml")
        android_f = open(android_recipe).read()
        format = "repo\sinit\s-u\sgit\@10\.57\.9\.151:svw-integration\/scm\.android\.git\s-b\s(\\w+)"
        rx = re.findall(format, android_f)
        android_cmt = rx[0]
        android_path = os.path.join(parent_dir, "android")
        git_clone("git@10.57.9.151:svw-integration/scm.android.git", "master", android_path)
        os.chdir(android_path)
        os.system("git checkout %s"%android_cmt)
    
    #Arrange whole dict
    new_dict = arrange_dict(git_dict)
    os.chdir(root_dir)
    add_wb(new_dict, current_time)
    excel_path = os.path.join(root_dir, 'GitLog_%s.xls'%current_time)
    excel_to_html(excel_path)
    if not (time_list == []):
        append_new_build_time(linux_time_path, max(time_list))
    
    git_push(time_path, current_branch, args.form)
    os.chdir(root_dir)
    
    (labels, quants, expl ) = ([], [], [0.1])
    rank_dict = get_pie_dict(new_dict)
    for key,value in sorted(rank_dict.iteritems(),key=lambda a:a[1],reverse=True):
        labels.append(key)
        quants.append(value)
        expl.append(0)
    print ">> LABELS: \033[91m%s\033[0m"%labels
    print ">> QUANTS: \033[91m%s\033[0m"%quants
    draw_pie_person(labels,quants,expl[:-1])
    
    role_dict = arrange_role_dict(git_dict)
    roles = ['jpcc', 'pcc', 'amt']
    counts = [role_dict['jpcc'], role_dict['pcc'], role_dict['amt']]
    draw_pie_role(roles, counts)
    print "\033[95m====================Drawing pictures succeed=====================\033[0m"
