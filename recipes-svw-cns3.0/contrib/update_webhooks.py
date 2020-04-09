#!/usr/bin/env python3
import argparse
import json
import os
import re
import collections
import gitlab       # from python-gitlab
import urllib3
from urllib.parse import urlsplit, quote_plus

def parseScms (jobs):
    scms = collections.OrderedDict()
    for item in jobs:
        for scm in item.get ('scm'):
            if 'git' in scm ['scm']:
                # keep list of job names related to this git url
                scms.setdefault (scm['url'], []).append (item['name'])
    return scms

def parseJSON (filePath):
    with open(filePath, 'r') as jsonFile:
        return parseScms (json.load (jsonFile))

def parseJSON_addremove (previousConfig, currentConfig):
    adds = []
    removes = []
    with open(previousConfig, 'r') as prev, open(currentConfig, 'r') as curr:
        prevJobs = json.load (prev)
        currJobs = json.load (curr)
        prevJobNames = [item.get('name')  for item in prevJobs]
        for item in currJobs:
            if item.get('name') not in prevJobNames:
                adds.append (item)
        currJobNames = [item.get('name')  for item in currJobs]
        for item in prevJobs:
            if item.get('name') not in currJobNames:
                removes.append (item)
    return (parseScms (adds), parseScms (removes))

def getProjectName (gitlabUrl, gitscmUrl):
    m = re.match ('^git@' + urlsplit (gitlabUrl).netloc + ':(.*)\\.git.*', gitscmUrl)
    if m:
        return m.group (1)
    else:
        print ('Warning: project not found for SCM:', gitscmUrl)
        return None

def getHookUrl (jenkinsUrl, jobPrefix=None, jobName=None):
    if jobPrefix and jobName:
        return jenkinsUrl + '/project/' + jobPrefix + '_' + jobName
    elif jobPrefix:
        return jenkinsUrl + '/project/' + jobPrefix + '_'
    else:
        return jenkinsUrl + '/project/'


def listHooks (project, urlPrefix):
    try:
        hooks = project.hooks.list()
        print()    # go to next line if no exception is thrown
        for hook in hooks:
            ####print('   Hook', hook.url)l
            if hook.url.startswith (urlPrefix):
                print ('   Hook found', hook.url)
    except gitlab.exceptions.GitlabError as e:
        print ('Error: {err}'.format(err=str(e)))


def addHooks (project, url, mergeRequest=False, dryrun=False):
    try:
        found = False
        for hook in project.hooks.list():
            if hook.url == url:
                print ("   Warning: hook already exist", hook.url)
                found = True
        if not found:
            if dryrun:
                print ("   (dryrun) Adding hook", url)
            else:
                print ("   Adding hook", url)
                if mergeRequest:
                    project.hooks.create ({'url' : url, 'push_events' : False, 'merge_requests_events' : True})
                else:
                    project.hooks.create ({'url' : url, 'push_events' : True, 'merge_requests_events' : False})
    except gitlab.exceptions.GitlabError as e:
        print ('   Error: {err}'.format(err=str(e)))

def removeHooks (project, url=None, urlPrefix=None, dryrun=False):
    try:
        for hook in project.hooks.list():
            if url and hook.url == url or \
               urlPrefix and hook.url.startswith (urlPrefix):
                if dryrun:
                    print ("   (dryrun) Removing hook", hook.url)
                else:
                    print ("   Removing hook", hook.url)
                    hook.delete()
    except gitlab.exceptions.GitlabError as e:
        print ('   Error: {err}'.format(err=str(e)))


def performAction (action, dryrun, mergeRequest, jobPrefix, jsonFile, previousJsonFile, gitlabUrl, privateToken, jenkinsUrl):
    gl = gitlab.Gitlab (gitlabUrl, private_token=privateToken, ssl_verify=False, api_version=4)
    if not gl:
        print ('Gitlab not connected')
        return

    if action == 'list':
            page = 1
            while 1:
                projects = gl.projects.list (page=page, per_page=50, as_list=False)
                if not projects:
                    break
                for project in projects:
                    print ("Listing hooks for", project.attributes['name_with_namespace'], "...", end=' ')
                    urlPrefix = getHookUrl (jenkinsUrl, jobPrefix)
                    listHooks (project, urlPrefix)
                page += 1

    elif action == 'addremove':
        if not jobPrefix:
            print ('Job prefix is required for addremove action')
            return

        if jsonFile and previousJsonFile:
            adds, removes = parseJSON_addremove (previousJsonFile, jsonFile)

            # first add new hooks
            for gitscmUrl, jobNames in adds.items():
                projectName = getProjectName (gitlabUrl, gitscmUrl)
                if not projectName:
                    continue
                print ("Examining project", projectName, "...")

                for jobName in jobNames:
                    project = gl.projects.get (projectName)
                    if not project:
                        print ('   Warning: project not found', projectName)
                        continue

                    webHook = getHookUrl (jenkinsUrl, jobPrefix, jobName)
                    addHooks (project, webHook, mergeRequest=mergeRequest, dryrun=dryrun)

            # then remove obsolete hooks
            for gitscmUrl, jobNames in removes.items():
                projectName = getProjectName (gitlabUrl, gitscmUrl)
                if not projectName:
                    continue
                print ("Examining project", projectName, "...")

                for jobName in jobNames:
                    project = gl.projects.get (projectName)
                    if not project:
                        print ('   Warning: project not found', projectName)
                        continue

                    webHook = getHookUrl (jenkinsUrl, jobPrefix, jobName)
                    removeHooks (project, url=webHook, dryrun=dryrun)

        else:
            print ('Action addremove requires two json configs (one passed)')
            return

    elif action == 'add' or action == 'remove':
        if not jobPrefix:
            print ('Job prefix is required for add or remove actions')
            return

        if jsonFile and previousJsonFile:
            print ('Action addremove requires only one json config (two passed)')
            return

        elif jsonFile:
            for gitscmUrl, jobNames in parseJSON (jsonFile).items():
                projectName = getProjectName (gitlabUrl, gitscmUrl)
                if not projectName:
                    continue
                print ("Examining project", projectName, "...")

                for jobName in jobNames:
                    project = gl.projects.get (projectName)
                    if not project:
                        print ('   Warning: project not found', projectName)
                        continue

                    webHook = getHookUrl (jenkinsUrl, jobPrefix, jobName)
                    if action == 'add':
                        addHooks (project, webHook, mergeRequest=mergeRequest, dryrun=dryrun)

                    elif action == 'remove':
                        removeHooks (project, url=webHook, dryrun=dryrun)

        else:
            if action == 'add':
                print ('Adding webhooks requires passing json config')
                return

            elif action == 'remove':
                page = 1
                while 1:
                    projects = gl.projects.list (page=page, per_page=10)
                    if not projects:
                        break
                    for project in projects:
                        print ("Examining project", project.name, "...")
                        urlPrefix = getHookUrl (jenkinsUrl, jobPrefix)
                        removeHooks (project, urlPrefix=urlPrefix, dryrun=dryrun)
                    page += 1


parser = argparse.ArgumentParser (description='Adds/removes/addremoves a webhook to/from all repositories in the configuration database (JSON)')
parser.add_argument ('--action', help='action to perform (add/remove/list/addremove)', required=True)
parser.add_argument ('--dryrun', help='Do not perform any actions', default=False, action='store_true')
parser.add_argument ('--merge-request', help='Created webhook will be assigned to merge request events instead of casual push events', default=False, action='store_true')
parser.add_argument ('--prefix', help='Jenkins job prefix (predefined by seed configuration)', default=None)
parser.add_argument ('--json-config', help='path to the configuration database (config.json)', default=None)
parser.add_argument ('--previous-json-config', help='path to the configuration database (previous_config.json), used for addremove action', default=None)
parser.add_argument ('gitlab', help='URL of the GitLab-Server')
parser.add_argument ('token', help='private token required for accessing GitLab API')
parser.add_argument ('jenkins', help='URL of the Jenkins-Server')
args = parser.parse_args()

# ignore SSL warnings
urllib3.disable_warnings()
if args.json_config:
    json_config = args.json_config  if os.path.isabs(args.json_config)  else os.getcwd() + '/' + args.json_config
else:
    json_config = ''
if args.previous_json_config:
    previous_json_config = args.previous_json_config  if os.path.isabs(args.previous_json_config)  else os.getcwd() + '/' + args.previous_json_config
else:
    previous_json_config = ''
performAction (args.action, args.dryrun, args.merge_request, args.prefix, json_config, previous_json_config, args.gitlab, args.token, args.jenkins)
