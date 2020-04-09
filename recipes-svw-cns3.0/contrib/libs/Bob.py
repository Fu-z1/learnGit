#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import simplejson as json
import subprocess as sp
import re

class BobFunction:
    def __init__(self, path):
        self.path = path

    def project(self, packages, defines, reuse=True):
        os.chdir(self.path)
        filename = 'config.json'
        if reuse:
            if not os.path.exists(filename):
                os.system('bob project ' + defines + ' -n json-config ' + packages)
        else:
            os.system('bob project ' + defines + ' -n json-config ' + packages)
        with open(filename, 'r') as f:
            json_list = json.loads(f.read())
        if not json_list:
            sys.stderr.write('File config.json not found!')
            return
        return json_list

    def query_path(self, packages, command, type, defines):
        '''
        :command: dev, build
        :type: src, build, dist
        '''
        os.chdir(self.path)
        if not defines:
            defines = ''
        if command == "dev":
            cmd_string = 'bob query-path -f {%s} %s --develop %s'%(type, defines, packages)
            format = 'dev'
        elif command == "build":
            cmd_string = 'bob query-path -f {%s} %s --release %s'%(type, defines, packages)
            format = 'work'
        cmd = re.split(r" +", cmd_string)
        print cmd
        out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
        while True:
            line = out.stdout.readline()
            if not line:
                break
            if (line.startswith(format)):
                info = line.strip()
                return info

    def query_scm(self, packages, format, defines):
        '''
        :format: eg. "-f git={url}#{tag} -f url={url}"
        '''
        scm_list = []
        os.chdir(self.path)
        if not defines:
            defines = ''
        cmd_string = 'bob query-scm -r %s %s %s'%(format, defines, packages)
        cmd = re.split(r" +", cmd_string)
        print cmd
        out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
        while True:
            line = out.stdout.readline()
            if not line:
                break
            if not (line.startswith("WARNING: ")) or (line.startswith("See ")) or (line.startswith("INFO: ")):
                info = line.strip()
                scm_list.append(info)
        return sorted(scm_list)

    def version(self):
        os.system("bob --version")
