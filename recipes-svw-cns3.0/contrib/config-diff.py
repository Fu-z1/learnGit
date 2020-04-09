#!/usr/bin/env python3
import argparse
import json
import os


def stripConfig(basePath, configPath, outputPath):

	baseData = json.load(open(basePath if os.path.isabs(basePath) else os.getcwd() + '/' + basePath, 'r+'))
	configData = json.load(open(configPath if os.path.isabs(configPath) else os.getcwd() + '/' + configPath, 'r+'))
	outputData = []

	for config in configData:
		configName = config.get('name')
		newConfig = True
		for base in baseData:
			if configName == base.get('name'):
				newConfig = False
				if config != base:
					outputData.append(config)
		if newConfig:
			outputData.append(config)

	outputFile = open(outputPath if os.path.isabs(outputPath) else os.getcwd() + '/' + outputPath, 'w')
	json.dump(outputData, outputFile, sort_keys=True, indent=4)
	outputFile.close

parser = argparse.ArgumentParser(description='Compares two json-configs and keeps only jobs that have differences')
parser.add_argument('base', help='path to the base configuration')
parser.add_argument('config', help='path to a configuration to be examined')
parser.add_argument('output', help='path to stripped output configuration')

args = parser.parse_args()

stripConfig(args.base, args.config, args.output)
