#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import simplejson as json
import xlwt
from xlwt import *

def analyze_json(json_file):
    s = {}
    with open(json_file, 'r') as f:
        json_dict = json.loads(f.read())
    if not json_dict:
        sys.stderr.write('File config.json not found!')
        return
    for i in range(len(json_dict)):
        system_variant = json_dict[i].pop('System Variant')
        if not s.has_key(system_variant):
            s[system_variant] = {}
        s[system_variant] = json_dict[i]
    return s

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

if __name__ == "__main__":
    cwd = sys.path[0]
    json_file = "variants-data.json"
    varaint_dict = analyze_json(json_file)
    (headline, col_width, feature_list) = (['FEATURE'], [35], [])
    
    for i in varaint_dict:
        headline.append(i)
        col_width.append(20)

    (row, col) = (3, 2)
    num = len(headline) + 1
    
    wb = xlwt.Workbook(encoding = 'utf-8', style_compression=2)
    ws = wb.add_sheet("variant")
    for i in range(1,num):
        ws.write(2,i,headline[i-1],style_form('head'))
        ws.col(i).width=256*col_width[i-1]
    
    for key,value in sorted(varaint_dict.iteritems()):
        for element in sorted(value.iteritems(),key=lambda a:a,reverse=False):
            print element
            ws.write(row,col,str(element[1]),style_form('content'))
            row = row+1
            if not element[0] in feature_list:
                feature_list.append(element[0])
        row = 3
        col = col+1

    for key in feature_list:
        ws.write(row,1,key,style_form('content'))
        row = row+1
    wb.save('variant-json.xls')
