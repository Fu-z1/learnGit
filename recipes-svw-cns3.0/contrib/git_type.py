#!/usr/bin/python
# -*- coding:utf-8 -*-
# python contrib/git_type.py -DCONFIG_XTENSA=1 zr3

import os
import sys
import shutil
import simplejson as json
import subprocess as sp
import argparse
import xlwt
from xlwt import *

def sortScms(scms):
    s = {'carry_over':{},'pcc_managed':{},'jpcc_managed':{}}
    for i in scms:
        if 'scm' in i.keys():
            for j in i['scm']:
                if j['scm'] == 'git':
                    if j['url'].startswith('git@10.57.9.151') or j['url'].startswith('git@cnninvmgtlb01'):
                        if j['commit']:
                            s['jpcc_managed'][j['url']] = j['commit']
                        elif j['tag'] and not j['commit']:
                            s['jpcc_managed'][j['url']] = j['tag']
                        elif j['branch'] and not j['commit'] and not j['tag']:
                            s['jpcc_managed'][j['url']] = j['branch']
                    else:
                        if j['branch'] and not j['commit'] and not j['tag']:
                            s['pcc_managed'][j['url']] = j['branch']
                        elif j['tag'] and not j['commit']:
                            s['carry_over'][j['url']] = j['tag']
                        elif j['commit']:
                            s['carry_over'][j['url']] = j['commit']
    return s

def bob_project(packages, defines):
    filename = 'config.json'
    os.system('bob project ' + defines + ' -n json-config ' + packages)
    with open(filename, 'r') as f:
        json_dict = json.loads(f.read())
    if not json_dict:
        sys.stderr.write('File config.json not found!')
        return
    scmsSorted = sortScms(json_dict)
    return scmsSorted

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

def add_wb(git_log_dict):
    global wb
    global ws
    wb = xlwt.Workbook(encoding = 'utf-8', style_compression=2)
    headline = ['PROJECT','REFS','OWNER GROUP','OWNER','TYPE']
    col_width = [80,40,10,20,15]
    add_sheet('git type', headline, col_width, git_log_dict)
    wb.save('GitType.xls')

def add_sheet(sheet_name, head, column_width, list):
    row = 1
    ws = wb.add_sheet(sheet_name)
    for i in range(0,len(head)):
        ws.write(0,i,head[i],style_form('head'))
        ws.col(i).width=256*column_width[i]
    
    for key,value in sorted(list['jpcc_managed'].iteritems(),key=lambda a:a):
        ws.write(row,0,key,style_form('content'))
        ws.write(row,1,value,style_form('content'))
        ws.write(row,2,'JPCC',style_form('content'))
        ws.write(row,3,'',style_form('content'))
        ws.write(row,4,'jpcc-managed',style_form('content'))
        row = row+1
    for key,value in sorted(list['pcc_managed'].iteritems(),key=lambda a:a):
        ws.write(row,0,key,style_form('content'))
        ws.write(row,1,value,style_form('content'))
        ws.write(row,2,'PCC',style_form('content'))
        ws.write(row,3,'',style_form('content'))
        ws.write(row,4,'pcc-managed',style_form('content'))
        row = row+1
    for key,value in sorted(list['carry_over'].iteritems(),key=lambda a:a):
        ws.write(row,0,key,style_form('content'))
        ws.write(row,1,value,style_form('content'))
        ws.write(row,2,'PCC',style_form('content'))
        ws.write(row,3,'',style_form('content'))
        ws.write(row,4,'carry-over',style_form('content'))
        row = row+1

if __name__ == "__main__":
    cwd = sys.path[0]
    root_dir = os.path.dirname(cwd)
    parent_dir = os.path.dirname(root_dir)
    (git_dict, row) = [{}, 3]

    parser = argparse.ArgumentParser(description='Process Git type')
    parser.add_argument('package', nargs='+', help="Sub-package that is the root of the project")
    parser.add_argument('-D', default=[], action='append', dest="defines",
                        help="Override default environment variable")
    args = parser.parse_args()
    if isinstance(args.package, list):
        packages = ' '.join(args.package)
    else:
        packages = args.package
    defines = ""
    if args.defines:
        defines = " ".join(['-D'+x for x in args.defines])

    os.chdir(root_dir)
    info_dict = bob_project(packages, defines)
    add_wb(info_dict)

