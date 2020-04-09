#!/usr/bin/env python3
import argparse
import json
import os
import sys

parser = argparse.ArgumentParser(description='Compares two json-configs and keeps only jobs that have differences')
parser.add_argument('config', help='path to the configuration file')
parser.add_argument('output', nargs='?', help='output file path')
parser.add_argument('-e', '--exclude', nargs='*', help='Groups also to exclude but group itself', default=[])

args = parser.parse_args()
jsonData = json.load(open(args.config if os.path.isabs(args.config) else os.getcwd() + '/' + args.config, 'r+'))
jobList = {x.get('name') : x.get('deps') for x in jsonData}
jobs = set()

def add_traverse_deps(jobName, exludes):
    jobs.update(set([x for x in jobList[jobName] if x in jobList.keys() and x.split('__')[0] not in exludes]))
    for dep in jobList[jobName]:
        if dep in jobList.keys():
            add_traverse_deps(dep, exludes)

for node in jsonData:
    if node.get('overridden'):
        jobs.add(node.get('name'))
        add_traverse_deps(node.get('name'), args.exclude)

if not jobs:
    print("No overrides!")
    sys.exit(0)

jobList = [x for x in jsonData if x.get('name') in jobs]
if args.output:
    file = args.output
else:
    file = args.config
with open(file, 'w+') as f:
    json.dump(jobList, f, sort_keys=True, indent=4)
