#!/usr/bin/python
# -*- coding:utf-8 -*-

import jenkins
import os
import sys

class JenkinsAPI:
    def __init__(self, url, username, token):
        '''
        the password could be real password or api token
        '''
        self.url = url
        self.username = username
        self.token = token
        self.server = jenkins.Jenkins(self.url, username=self.username, password=self.token)
    
    def get_jenkins_version(self):
        version = self.server.get_version()
        return version
    
    def get_current_user(self):
        user = self.server.get_whoami()
        #return user['fullName']
        return user['id']
    
    def get_job_counts(self):
        count = self.server.jobs_count()
        return count
    
    def get_server_jobs(self):
        jobs = self.server.get_jobs()
        return jobs
    
    def get_job_config(self, job_name):
        job_config = self.server.get_job_config(job_name)
        return job_config
    
    def create_job(self, job_name, *args):
        '''
        args0: config_file
        '''
        if len(args) >= 1:
            self.server.create_job(job_name, args[0])
        else:
            self.server.create_job(job_name, jenkins.EMPTY_CONFIG_XML)
        print "Create job: %s"%(job_name)
    
    def copy_job(self, from_name, to_name):
        self.server.copy_job(from_name, to_name)
        print "Copy from job %s to new job %s"%(from_name, to_name)

    def rename_job(self, from_name, to_name):
        self.server.rename_job(from_name, to_name)
        print "Rename job from %s to %s"%(from_name, to_name)

    def disable_job(self, job_name):
        self.server.disable_job(job_name)
        print "Disable job: %s"%(job_name)
    
    def enable_job(self, job_name):
        self.server.enable_job(job_name)
        print "Enable job: %s"%(job_name)
    
    def delete_job(self, job_name):
        self.server.delete_job(job_name)
        print "Delete job: %s"%(job_name)
    
    def reconfig_job(self, job_name, *args):
        '''
        args0: config_file
        '''
        if len(args) >= 1:
            self.server.reconfig_job(job_name, args[0])
            print "Reconfigure job: %s according to %s"%(job_name, args[0])
        else:
            self.server.reconfig_job(job_name)
            print "Reconfigure job: %s to an empty job"%(job_name)
    
    def build_job(self, job_name, **kwargs):
        self.server.build_job(job_name, kwargs)
        print "Build job: %s"%(job_name)
    
    def job_exists(self, job_name):
        return self.server.job_exists(job_name)
    
    def assert_job_exists(self, job_name):
        self.server.assert_job_exists(job_name, exception_message='job[%s] does not exist')
        return True
    
    def get_last_build_number(self, job_name):
        last_build_number = self.server.get_job_info(job_name)['lastCompletedBuild']['number']
        return last_build_number
    
    def get_build_info(self, job_name, build_num):
        build_info = self.server.get_build_info(job_name, build_num)
        return build_info
    
    def stop_build(self, job_name, build_num):
        self.server.stop_build(job_name, build_num)
        print "Stop the build num %s of job %s"%(build_num, job_name)
    
    def delete_build(self, job_name, build_num):
        self.server.delete_build(job_name, build_num)
        print "Delete the build num %s of job %s"%(build_num, job_name)
    
    def get_running_builds(self):
        running_builds = self.server.get_running_builds()
        return running_builds
    
    #========================views==================================#
    def create_view(self, view_name, *args):
        '''
        args0: config_file
        '''
        if len(args) >= 1:
            self.server.create_view(view_name, args[0])
        else:
            self.server.create_view(view_name, jenkins.EMPTY_VIEW_CONFIG_XML)
        print "Create view: %s"%(view_name)
    
    def reconfig_view(self, view_name, *args):
        '''
        args0: config_file
        the config file and the original view must be in the same type, eg. list view, or sectioned view
        '''
        if len(args) >= 1:
            self.server.reconfig_view(view_name, args[0])
        else:
            self.server.reconfig_view(view_name, jenkins.EMPTY_VIEW_CONFIG_XML)
        print "Reconfigure view: %s"%(view_name)
    
    def delete_view(self, view_name):
        self.server.delete_view(view_name)
        print "Delete view: %s"%(view_name)
    
    def get_view_config(self, view_name):
        view_config = self.server.get_view_config(view_name)
        return view_config
    
    def get_server_views(self):
        views = self.server.get_views()
        return views
    
    def get_view_jobs(self, view_name):
        jobs = self.server.get_jobs(view_name=view_name)
        return jobs
    
    def view_exists(self, view_name):
        return self.server.view_exists(view_name)
    
    def assert_view_exists(self, view_name):
        self.server.assert_view_exists(view_name, exception_message='view[%s] does not exist')
        return True
