#!/usr/bin/env python3
import argparse
import gitlab3
import json
import os
import re
from urllib.parse import urlsplit, quote_plus


def parseJSON(filePath):

	scmList = {}
	
	with open(filePath if os.path.isabs(filePath) else os.getcwd() + '/' + filePath, 'r+') as jsonFile:
		jsonData = json.load(jsonFile)

		for item in jsonData:
			for scm in item.get('scm'):
				if 'git' in scm['scm']:
					if not scm['url'] in scmList.keys():
						scmList[scm['url']] = []
					scmList[scm['url']].append(item['name'])

	return scmList


def updateWebHooks(repositories, remove, gitServer, privateToken, jenkinsServer, jobPrefix):

	gl = gitlab3.GitLab(gitServer, privateToken, ssl_verify=False)
	serverURL = urlsplit(gitServer).netloc

	for projectURL in repositories:
		m = re.match('^git@' + serverURL + ':(.*)\\.git.*', projectURL)
		if not m: continue
		projectName = m.group(1)
		print("Examining", projectName, "...")

		for jobName in repositories[projectURL]:
			webHook = jenkinsServer + '/project/' + jobPrefix + '_' + jobName
			try:
				project = gl.project(quote_plus(projectName))
				found = False
				for hook in project.hooks():
					if hook.url == webHook:
						found = True
						if remove:
							print("   Remove hook", webHook)
							project.delete_hook(hook)
				if not found and not remove:
					print("   Add hook", webHook)
					project.add_hook(webHook)
			except Exception as e:
				print('   Could not {mod} hook: {err}'.format(mod='remove' if remove else 'add', err=str(e)))


parser = argparse.ArgumentParser(description='Adds/removes a webhook to/from all repositories in the configuration database (JSON).')
parser.add_argument('--remove', action='store_true', help='will remove webhooks instead of adding them')
parser.add_argument('filepath', help='path to the configuration database (config.json)')
parser.add_argument('gitlab', help='URL of the GitLab-Server')
parser.add_argument('token', help='private token required for accessing GitLab API')
parser.add_argument('jenkins', help='URL of the Jenkins-Server')
parser.add_argument('prefix', help='Jenkins job prefix (predefined by seed configuration)')

args = parser.parse_args()

repositories = parseJSON(args.filepath)

updateWebHooks(repositories, args.remove, args.gitlab, args.token, args.jenkins, args.prefix)
