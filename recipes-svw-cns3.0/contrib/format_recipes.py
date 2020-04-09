#!/usr/bin/python3

import argparse
import os
import re
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.scalarstring import SingleQuotedScalarString, DoubleQuotedScalarString
from ruamel.yaml.error import YAMLStreamError

debug = False

def printDebug(s):
    if (debug):
        print(s)

def formatRecipe(recipe):
    yaml = YAML(typ='rt')
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    yaml.indent(mapping=3, sequence=4, offset=2)
    yaml.allow_duplicate_keys = True
    with open(recipe) as f:
        content = yaml.load(f)

    printDebug(content)

    with open(recipe, "w") as f:
        yaml.dump(content, f)

    #ruaml add identation after literal block mapping scalar operator. pyyaml did not understand..
    with open(recipe) as f:
        content = f.read()

    content = re.sub(r"checkoutScript: \|.*", "checkoutScript: |", content)
    content = re.sub(r"buildScript: \|.*", "buildScript: |", content)
    content = re.sub(r"packageScript: \|.*", "packageScript: |", content)

    with open(recipe, "w") as f:
        f.write(content)


def main():
    global debug

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='yaml file to process')
    parser.add_argument('-d', '--debug', default=False, action='store_true',
            help='enable debug prints')
    ret = parser.parse_args()

    debug = ret.debug

    try:
        formatRecipe(ret.file)
    except YAMLStreamError as e:
        print(ret.file + "\terror while parsing!" + e)

if __name__ == "__main__": main()
