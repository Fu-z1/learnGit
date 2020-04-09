#!/usr/bin/env python3
import argparse
import json
import os

def modifyJSON(filePath, gitRepo, branch, commitHash):
	
	with open(filePath if os.path.isabs(filePath) else os.getcwd() + '/' + filePath, 'r+') as jsonFile:
		jsonData = json.load(jsonFile)

		for item in jsonData:
			name = item.get('name')
			for scm in item.get('scm'):
				scmType = scm.get('scm')
				if 'git' in scmType:
					if (gitRepo in scm['url']) and (branch in scm['branch']):
						scm['commit'] = commitHash
						print(name)

		jsonFile.seek(0)
		json.dump(jsonData, jsonFile, sort_keys=True, indent=4)
		jsonFile.truncate()


parser = argparse.ArgumentParser(description='Updates the latest commit hash of a given repository in the configuration database (JSON).')
parser.add_argument('filepath', help='path to the configuration database (config.json)')
parser.add_argument('repository', help='Git URL of repository to be checked')
parser.add_argument('branch', help='branch to be verified')
parser.add_argument('commit', help='latest commit hash to replace a previous one')

args = parser.parse_args()

modifyJSON(args.filepath, args.repository, args.branch, args.commit)