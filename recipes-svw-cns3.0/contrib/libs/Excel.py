#!/usr/bin/python
# -*- coding:utf-8 -*-

from xlwt import *

class ExcelFunction:
    def __init__(self, file):
        self.file = file
        self.wb = Workbook(encoding = 'utf-8', style_compression=2)
        self.sheets = {}

    def excel_font(self, font_name, bold, ci, fc, border):
        font = Font()
        font.name = font_name
        font.bold = bold
        font.colour_index = ci

        pattern = Pattern()
        pattern.pattern = 1
        pattern.pattern_fore_colour = fc

        alignment = Alignment()
        alignment.vert = Alignment.VERT_CENTER
        alignment.wrap = Alignment.WRAP_AT_RIGHT

        borders = Borders()
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

    def get_style(self, format):
        if format == 'head':
            style = self.excel_font('Times New Roman',True,0,27,Borders.MEDIUM)
        elif format == 'content':
            style = self.excel_font('Arial',False,0, 1,Borders.THIN)
        return style

    def create_sheet(self, sheet_name='sheet'):
        if sheet_name in self.sheets:
            sheet_index = self.sheets[sheet_name]['index'] + 1
        else:
            sheet_index = 0
            self.sheets[sheet_name] = {'header': []}
        self.sheets[sheet_name]['index'] = sheet_index
        self.sheets[sheet_name]['sheet'] = self.wb.add_sheet('%s%s' % (sheet_name, sheet_index if sheet_index else ''), cell_overwrite_ok=True)
        self.sheets[sheet_name]['rows'] = 1

    def write(self, row, colum, element, format, sheet_name='sheet'):
        if sheet_name not in self.sheets:
            self.create_sheet(sheet_name)

        style = self.get_style(format)
        self.sheets[sheet_name]['sheet'].write(row,colum,element,style)
        self.sheets[sheet_name]['rows'] += 1

    def merge(self, row1, row2, colum1, colum2, element, format, sheet_name='sheet'):
        if sheet_name not in self.sheets:
            self.create_sheet(sheet_name)

        style = self.get_style(format)
        self.sheets[sheet_name]['sheet'].write_merge(row1, row2, colum1, colum2, element,style)

    def colum_width(self, width_list, sheet_name='sheet'):
        if sheet_name not in self.sheets:
            self.create_sheet(sheet_name)

        num = len(width_list)
        for i in range(0,num):
            self.sheets[sheet_name]['sheet'].col(i).width=256*width_list[i]

    def cell(self, s):
        if isinstance(s, basestring):
            if not isinstance(s, unicode):
                s = s.decode(self.encoding)
        elif s is None:
            s = ''
        else:
            s = str(s)
        return s

    def save(self):
        self.wb.save(self.file)

    def excel_2_html(self):
        import pandas as pd
        import codecs
        xd = pd.ExcelFile(self.file)
        df = xd.parse()
        with codecs.open('gitlog.html','w','utf-8') as html_file:
             html_file.write(df.to_html(header = True,index = False))


if __name__ == '__main__':
    xls = ExcelFunction(u'test.xls')
    xls.colum_width([3, 4, 5, 2], "git")
    xls.colum_width([10], "commit")
    
    for i in range(10):
        for j in range(4):
            xls.write(i, j, i, "head", "git")
    for i in range(80):
        for j in range(1):
            xls.write(i, j, i, "content", "commit")
    xls.save()
