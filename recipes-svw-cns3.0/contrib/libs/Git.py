#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import subprocess as sp
import shutil

class GitFunction:
    def __init__(self, path):
        self.path = path

    def clone(self, url, *args):
        if os.path.exists(self.path):
            print ">> \033[93m%s exists, deleting\033[0m"%(self.path)
            shutil.rmtree(self.path)
        if len(args) >= 1:
            os.system("git clone %s -b %s %s"%(url, args[0], self.path))
        else:
           os.system("git clone %s %s"%(url, self.path))

    def clone_mirror(self, url):
        '''
        self.path should be *.git format
        '''
        if os.path.exists(self.path):
            print ">> \033[93m%s already exists!\033[0m"%(self.path)
            sys.exit(-1)
        os.system("git clone --mirror %s %s"%(url, self.path))

    def current_branch(self):
        os.chdir(self.path)
        cmd = ['git', 'branch']
        out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
        while True:
            line = out.stdout.readline()
            if not line:
                break
            if (line.startswith('*')):
                info = ((line.strip()).split(' '))[-1]
                return info

    def create_branch(self, branch, *args):
        os.chdir(self.path)
        if len(args) >= 1:
            if not os.system("git checkout -b %s origin/%s"%(branch, args[0])):
                print ">> \033[92mCreate and Checkout to branch: %s tracking remote: %s !\033[0m\n"%(branch, args[0])
        else:
            if not os.system("git checkout -b %s"%(branch)):
                print ">> \033[92mCheckout to branch: %s !\033[0m\n"%(branch)

    def checkout(self, branch):
        os.chdir(self.path)
        if not os.system("git checkout %s"%(branch)):
            print ">> \033[92mCheckout to branch: %s !\033[0m\n"%(branch)

    def status(self):
        os.chdir(self.path)
        os.system("git status")
        cmd = ['git', 'status']
        out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
        while True:
            info = out.stdout.readline()
            print info
            if not info:
                break
            if "nothing to commit, working tree clean" in info:
                return None
            else:
                return 1

    def add(self, format):
        '''
        :format: could be file name , or "-u", or ".", or "-A"
        '''
        os.chdir(self.path)
        os.system("git add %s"%(format))

    def commit(self, message):
        os.chdir(self.path)
        os.system("git commit -m\"%s\""%(message))

    def create_tag(self, tag):
        os.chdir(self.path)
        if not os.system("git tag %s"%(tag)):
            print "Create Tag: %s !"%tag

    def list_tag(self):
        os.chdir(self.path)
        cmd = ['git', 'tag']
        out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
        info= out.stdout.readlines()
        return info

    def push_tag(self, tag):
        os.chdir(self.path)
        os.system("git push origin %s"%(tag))

    def push_branch(self, current_branch, remote_branch):
        os.chdir(self.path)
        os.system("git push origin %s:%s"%(current_branch, remote_branch))

    def get_file(self, url, branch, file):
        cwd = os.getcwd()
        os.system('git archive --remote=%s --format=tar %s %s | tar xf -'%(url, branch, file))
        file_path = os.path.join(cwd, file)
        return file_path

    def get_HEAD(self):
        os.chdir(self.path)
        cmd = ['git', 'rev-parse', 'HEAD']
        out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
        info= (out.stdout.readlines())[0].strip()
        return info

    def show(self, sha1sum):
        os.chdir(self.path)
        os.system("git show %s"%sha1sum)

    def log(self, *args):
        os.chdir(self.path)
        if len(args) >= 1:
            os.system("git log %s"%(args[0]))
        else:
            os.system("git log")

    def diff(self, sha1sum1, sha1sum2, *args):
        if not (sha1sum1 == sha1sum2):
            os.chdir(self.path)
            if len(args) >= 1:
                cmd = ['git', 'diff', sha1sum1, sha1sum2, args[0]]
            else:
                cmd = ['git', 'diff', sha1sum1, sha1sum2]
            out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
            info = out.stdout.readlines()
            return info

    def get_remote_url(self):
        cmd = ['git', 'remote', '-v']
        out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
        info = out.stdout.readlines()
        for line in info:
            l = line.strip()
            if l.startswith("origin") and l.endswith("fetch)"):
                url = (l.split(" ")[0]).split("\t")[-1]
        return url

    def remote_update(self):
        os.chdir(self.path)
        if os.system("git remote update"):
            print ">> \033[91mRemote update failed: %s !\033[0m\n"%(self.path)

    def remote_add(self, remote, url):
        os.chdir(self.path)
        os.system("git remote add %s %s"%(remote, url))

    def fetch(self, remote, source_ref, target_ref):
        os.chdir(self.path)
        if os.system('git fetch %s +refs/heads/%s:refs/heads/%s'%(remote, source_ref, target_ref)):
            print ">> \033[91mGit fetch %s %s failed!\033[0m"%(self.path, source_ref)
            sys.exit(-1)

