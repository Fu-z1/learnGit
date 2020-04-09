#!/usr/bin/python
# -*- coding:utf-8 -*-


class FileFunction:
    def __init__(self, path):
        self.path = path

    def read(self):
        file = self.path
        with open(file,'r') as f:
            info = f.read()
            return info

    def readlines(self):
        file = self.path
        info = []
        with open(file,'r') as f:
            lines = f.readlines()
            for line in lines:
                info.append(line.strip("\n"))
            return info

    def get_last_line(self):
        file = self.path
        info = self.readlines()
        last_line = (info[-1]).strip()
        return last_line

    def append_new_line(self, line):
        file = self.path
        with open(file,'a') as f:
            f.write('%s\n'%line)
        f.close()
