#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import argparse
import subprocess as sp
from libs import Bob

def get_target_version(file):
    f = open(file).read()
    info = yaml.load(f)
    if info.has_key('environment'):
        TARGET_VERSION = info['environment']['TARGET_VERSION']
    return TARGET_VERSION

def get_main_version(file):
    dict = {}
    f = open(file).read()
    info = yaml.load(f)
    if info.has_key('environment'):
        for i in info['environment']:
            dict[i] = info['environment'][i]
    return dict

def get_remote_dir_name(path, form, version, date, tag, variant_name):
    path_dict = {'daily':'daily_build', 
                 'weekly':'weekly_release', 
                 'temp':'temp_release'}
    form_path = path_dict[form]
    dir = date
    if form == 'temp':
        dir = version.replace("/", "-")
    elif form == 'weekly':
        dir = date + "_" + tag
    remote_dir_name = os.path.join("/var", "www", path, "linux", form_path, dir, variant_name)
    print ">> \033[92mREMOTE DIR NAME: %s\033[0m"%remote_dir_name
    return remote_dir_name

def get_variant_dir(variant):
    return ((variant.split("/")[-1]).split("zr3-variant-")[-1]).split("37W-")[-1]

def get_package_name(prj, variant, info, descrip, date, release_form, key):
    major = info[key + 'MAJOR']
    buildref = info[key + 'BUILDREF']
    abbrev = '0'
    if not "sec" in variant:
        if 'zr3-cu-' in variant:
            abbrev = 'D'
        elif 'zr3-navimap-' in variant:
            abbrev = (variant.split("-")[-1])[0]
        else:
            abbrev = (variant.split("_")[-1])[0]
    
    var_version = abbrev + major.zfill(3) + '_RC' + buildref
    var_name = get_variant_dir(variant)
    package_name = ("-".join([prj, var_name, var_version, descrip, date, release_form]) + ".tgz")
    print ">> \033[92mPACKAGE NAME: %s\033[0m"%package_name
    return package_name

def tar_tgz(pkg_name, variant, whole=False):
    if whole:
        os.system('tar czf %s ./*'%(pkg_name))
    else:
        os.system('tar czf %s UpdateContainer\/'%(pkg_name))
        if "zr3-variant" in variant:
            os.system('tar czf %s FlashContainer\/'%(pkg_name.replace(".tgz", "-flashcontainer.tgz")))
            os.system('tar czf %s Symbols\/'%(pkg_name.replace(".tgz", "-symbols.tgz")))
    os.system('sha1sum ./*.tgz >> sha1sum.txt')

def upload_2_remote(source, path, form, version, info, variant, prj, release_form, whole, suffix):
    date = ".".join(version.split(".")[-2:])
    key = ''
    if "navimap" in variant:
        key = 'MAP_'
    
    descrip = "MAIN"
    if (form == "temp"):
        if suffix:
            descrip = suffix.upper()
    
    pkg_name = get_package_name(prj, variant, info, descrip, date, release_form, key)
    var_name = get_variant_dir(variant)
    tag_name = get_tag_name(info, suffix, key)
    target = get_remote_dir_name(path, form, version, date, tag_name, var_name)
    
    os.system('echo \"%s\" > dir.txt'%target)
    os.chdir(source)
    tar_tgz(pkg_name, variant, whole)
    os.system('ssh upload \"mkdir -p %s\"'%target)
    os.system('rsync -avr --delete \
               *.txt \
               *.tgz \
               ../audit.json.gz \
               UpdateContainer/Meta/main.mnf.cks \
               upload@cnninvmlgcldc01:%s\/'%(target))

def verify_manifest(file):
    if os.system('python contrib\/manifest_validate.py %s'%file):
        sys.exit(-1)

def get_tag_name(info, suffix, key):
    tag = info[key + 'MAJOR'] + info[key + 'DELIVERY'] + "-rc" + info[key + 'BUILDREF']
    if suffix:
        tag = info[key + 'MAJOR'] + info[key + 'DELIVERY'] + "-rc" + info[key + 'BUILDREF'] + '-' + suffix
    return tag

if __name__ == "__main__":
    platform_path = {'MQB' : 'cns-c-sample', '37W' : '37w-b0-sample'}
    parser = argparse.ArgumentParser(description='Process Upload')
    parser.add_argument('package', nargs='+', help="Sub-package that is the root of the project")
    parser.add_argument("-f", "--form", required=True, type=str, choices=['daily', 'weekly', 'temp'], help="Build Type")
    parser.add_argument('-D', default=[], action='append', dest="defines", help="Override default environment variable")
    parser.add_argument("-s", "--suffix", type=str, help="Add tag suffix if needed")
    parser.add_argument("-c", "--command", type=str, required=True, choices=['dev', 'build'], help="choose command used for bob")
    parser.add_argument("-p", "--platform", required=True, type=str, choices=['MQB', '37W', 'VBOX'],
                         help="Build Platform")
    parser.add_argument("--prj", type=str, default='CNS3.0', help="Project Name")
    parser.add_argument("-w", "--whole", default=False, action='store_false', help="Do not divide package tar ball")
    parser.add_argument("-v", "--verify", action='store_true', help="Judge if validate manifest")
    args = parser.parse_args()
    
    platform = args.platform
    project_name = args.prj + "_" + platform
    form = args.form
    tag_suffix = args.suffix
    bob_command = args.command
    manifest_verify = args.verify
    defines = ""
    if args.defines:
        defines = " ".join(['-D'+x for x in args.defines])
    if isinstance(args.package, list):
        packages = ' '.join(args.package)
    else:
        packages = args.package
    
    if (form == "weekly"):
        package_type = "REL"
    else:
        package_type = "DEV"
    
    cwd = sys.path[0]
    root_dir = os.path.dirname(cwd)
    parent_dir = os.path.dirname(root_dir)
    bob = Bob.BobFunction(root_dir)
    product_path = os.path.join(root_dir, bob.query_path(packages, bob_command, "dist", defines))
    
    if manifest_verify:
        verify_manifest(os.path.join(product_path, "UpdateContainer"))
    
    main_file = os.path.join(root_dir, 'recipes', '%s.yaml'%(packages.split("/")[0]))
    version_file = os.path.join(root_dir, 'recipes', 'system', 'target-version.yaml')
    target_version = get_target_version(version_file)
    main_version = get_main_version(main_file)
    
    upload_2_remote(product_path, platform_path[platform], form, target_version, main_version, 
                    packages, project_name, package_type, args.whole, tag_suffix)

