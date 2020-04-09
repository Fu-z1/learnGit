#!/usr/bin/python
# -*- coding:utf-8 -*-
# Filename:get_variable.py

import os
import yaml
import argparse
import re

def hmi_version(file):
    hmi_version = ''
    f = open(file).read()
    info = yaml.load(f)

    if info.has_key('multiPackage'):
        if info['multiPackage'].has_key('high-pkg'):
            if info['multiPackage']['high-pkg'].has_key('checkoutSCM'):
                url = info['multiPackage']['high-pkg']['checkoutSCM']['url']
                hmi_version = url.split('/')[-2]
                return hmi_version

def MXNavi_version(file1, file2, file3, file4):
    MXNavi_version = []
    file_list = [file1, file2, file3, file4]
    for file in file_list:
        f = open(file).read()
        info = yaml.load(f)
        if info.has_key('checkoutSCM'):
            for scm in info['checkoutSCM']:
                url = scm['url']
                MXNavi_version.append(url.split('/')[-1])
    return MXNavi_version

def sds_version(file):
    sds_version = ''
    f = open(file).read()
    info = yaml.load(f)
    if info.has_key('environment'):
        sds_version = info['environment']['ZIP']
        return sds_version

def issw_version(file):
    issw_version = ''
    f = open(file).read()
    info = yaml.load(f)
    if info.has_key('metaEnvironment'):
        issw_version = info['metaEnvironment']['ISSW_VERSION']
        return issw_version

def hv_version(file):
    hv_version = ''
    f = open(file).read()
    info = yaml.load(f)
    if info.has_key('multiPackage'):
        hv_url = info['multiPackage']['']['checkoutSCM']['url']
        hv_version = hv_url.split('/')[-1]
        return hv_version

def android_url(file):
    f = open(file).read()
    format = '(repo\sinit\s-u\s([\s\S]*?)\s-b\s(.*)?)'
    rx = re.findall(format, f)
    url = rx[0][0]
    return url

def android_version(file):
    f = open(file).readlines()
    for i in f:
        line = i.strip()
        if line.startswith("TIMESTAMP="):
            TIMESTAMP = line.split("=")[-1]
        elif line.startswith("PROJECT="):
            PROJECT = line.split("=")[-1]
        elif line.startswith("BRANCH="):
            BRANCH = line.split("=")[-1]
    android_version = "/".join([PROJECT, BRANCH, TIMESTAMP])
    return android_version

def specific_version(file):
    f = open(file).read()
    info = yaml.load(f)
    if info.has_key('environment'):
        specific_version = info['environment']['TARGET_VERSION']
    return specific_version

def variant_dict(file):
    dict = {}
    f = open(file).read()
    info = yaml.load(f)
    if info.has_key('environment'):
        for i in info['environment']:
            dict[i] = info['environment'][i]
    return dict

if __name__ == "__main__":
    cwd = os.getcwd()
    root_dir = os.path.dirname(cwd)
    workspace = os.path.dirname(root_dir)

    parser = argparse.ArgumentParser(description='Process Upload')
    parser.add_argument("-p", "--platform", required=True, type=str, choices=['MQB', '37W'],
                         help="Build Platform")
    parser.add_argument("-s", "--stage", required=True, type=str, choices=['A-Sample', 'B-Sample', 'C-Sample'],
                         help="Build Stage")
    parser.add_argument("-b", "--base", required=True, type=str, help="MIB3 base version tag")
    args = parser.parse_args()
    platform = args.platform
    project_name = "CNS3.0_%s"%(platform)
    platform_path_dict = {'MQB' : 'cns-b-sample', '37W' : '37w-a-sample'}
    http_url = 'http://cnninvmlgcldc01:82/%s/linux/weekly_release'%(platform_path_dict[platform])
    base_version = args.base
    stage = args.stage
    
    sds_yaml = os.path.join(root_dir, 'recipes', 'sds', 'speech.external', 'ext-resource.yaml')
    issw_yaml = os.path.join(root_dir, 'recipes', 'basic-services', 'car-function-management', 'ext-vw-carssw.yaml')
    MXNavi_yaml1 = os.path.join(root_dir, 'recipes', 'MXNavi', 'ext-MXNavi.yaml')
    MXNavi_yaml2 = os.path.join(root_dir, 'recipes', 'MXNavi', 'ext-MXNavi-map-chn2mesh.yaml')
    MXNavi_yaml3 = os.path.join(root_dir, 'recipes', 'MXNavi', 'ext-MXNavi-map-chn.yaml')
    MXNavi_yaml4 = os.path.join(root_dir, 'recipes', 'MXNavi', 'ext-MXNavi-map-tw.yaml')
    rc_yaml = os.path.join(root_dir, 'recipes', 'zr3.yaml')
    version_yaml = os.path.join(root_dir, 'recipes', 'system', 'target-version.yaml')
    hv_yaml = os.path.join(root_dir, 'recipes', 'system', 'bsp', 'ext-opensynergy.yaml')
    android_yaml = os.path.join(root_dir, 'recipes', 'system', 'bsp', 'ext-renesas-h3-android.yaml')
    android_ECF = os.path.join(workspace, 'ECF')

    MXNavi_version = MXNavi_version(MXNavi_yaml1,MXNavi_yaml2,MXNavi_yaml3,MXNavi_yaml4)
    sds_version = sds_version(sds_yaml)
    issw_version= issw_version(issw_yaml)
    hv_version = hv_version(hv_yaml)
    android_version = android_version(android_ECF)
    android_url = android_url(android_yaml)
    specific_version = specific_version(version_yaml)
    variant_dict = variant_dict(rc_yaml)
    TAG = variant_dict['MAJOR'].zfill(3) + variant_dict['DELIVERY'] + "-rc" +variant_dict['BUILDREF']
    TAG_NAVIMAP = variant_dict['MAP_MAJOR'].zfill(3) + variant_dict['MAP_DELIVERY'] + "-rc" +variant_dict['MAP_BUILDREF'] + "-NAVIMAP"
    remote_dir = '.'.join(specific_version.split('.')[-2:]) + "_" + TAG
    remote_dir_NAVIMAP = '.'.join(specific_version.split('.')[-2:]) + "_" + TAG_NAVIMAP
    git_log_url = os.path.join(http_url, remote_dir, "gitlog.html")
    
    info_dict = {"VW_CHN":{"hmi_yaml" : "vw-chn", "abbr" : "C"},
                 "VW_HM":{"hmi_yaml" : "vw-twn", "abbr" : "H"},
                 "VW_TW":{"hmi_yaml" : "vw-chn", "abbr" : "T"},
                 "SK_CHN":{"hmi_yaml" : "skoda-chn", "abbr" : "C"},
                 "SK_TW":{"hmi_yaml" : "skoda-twn", "abbr" : "T"},
                 "zr3-navimap-CHN":{"hmi_yaml" : "vw-chn", "abbr" : "C"},
                 "zr3-navimap-TW":{"hmi_yaml" : "vw-twn", "abbr" : "T"},
                 "zr3-navimap-CHN_2mesh":{"hmi_yaml" : "vw-chn", "abbr" : "C"}}

    for i in info_dict:
        info_dict[i]["NAVI_TARBALL1"] = MXNavi_version[0]
        info_dict[i]["NAVI_TARBALL2"] = MXNavi_version[1]
        info_dict[i]["NAVI_TARBALL3"] = MXNavi_version[2]
        info_dict[i]["NAVI_TARBALL4"] = MXNavi_version[3]
        info_dict[i]["NAVI_TARBALL5"] = MXNavi_version[4]
        info_dict[i]["SPECIFIC_VERSION"] = specific_version
        build_num = '.'.join(specific_version.split('.')[-2:])
        info_dict[i]["TAG"] = TAG
        info_dict[i]["TAG_NAVIMAP"] = TAG_NAVIMAP
        info_dict[i]["SDS"] = sds_version
        info_dict[i]["ISSW"] = issw_version
        info_dict[i]["HV"] = hv_version
        info_dict[i]["ANDROID"] = android_version
        info_dict[i]["ANDROID_URL"] = android_url
        info_dict[i]["SW_VERSION"] = info_dict[i]["abbr"] + variant_dict['MAJOR'].zfill(3)
        info_dict[i]["SW_VERSION_NAVIMAP"] = info_dict[i]["abbr"] + variant_dict['MAP_MAJOR'].zfill(3)
        
        hmi_recipe = os.path.join(root_dir, 'recipes', 'hmi', 'pcc-hmi-%s.yaml'%info_dict[i]["hmi_yaml"])
        info_dict[i]["HMI"] = hmi_version(hmi_recipe)
        
        PKG = '-'.join([project_name, i, info_dict[i]["SW_VERSION"] + '_RC' + variant_dict['BUILDREF'], 'MAIN', build_num, 'REL'] )+ '.tgz'
        PKG_FC = '-'.join([project_name, i, info_dict[i]["SW_VERSION"] +'_RC' + variant_dict['BUILDREF'], 'MAIN', build_num, 'REL',"flashcontainer"] )+ '.tgz'
        PKG_NAVIMAP = '-'.join([project_name, i, info_dict[i]["SW_VERSION_NAVIMAP"] + '_RC' + variant_dict['MAP_BUILDREF'], 'MAIN', build_num, 'REL'] )+ '.tgz'
        info_dict[i]["PACKAGE"] = os.path.join(http_url, remote_dir, i, PKG)
        info_dict[i]["PACKAGE_FC"] = os.path.join(http_url, remote_dir, i, PKG_FC)
        info_dict[i]["PACKAGE_NAVIMAP"] = os.path.join(http_url, remote_dir_NAVIMAP, i, PKG_NAVIMAP)

    title = stage + " " + TAG + " ( " + remote_dir.split('.')[0] + " )"
    week = 'Release ' + TAG.split('-')[0]
    title_NAVIMAP = stage + " " + TAG_NAVIMAP + " ( " + remote_dir.split('.')[0] + " )"
    week_NAVIMAP = 'Release ' + TAG_NAVIMAP.split('-')[0]

    info_file = os.path.join(root_dir, 'info')
    with open(info_file,'a') as info_data:
        info_data.write('export TITLE=\"%s\"\n'%(title))
        info_data.write('export WEEK=\"%s\"\n'%(week))
        info_data.write('export TITLE_NAVIMAP=\"%s\"\n'%(title_NAVIMAP))
        info_data.write('export WEEK_NAVIMAP=\"%s\"\n'%(week_NAVIMAP))
        info_data.write('export BASE_NAME=\"%s\"\n'%(base_version))
        for i in info_dict:
            name = i.replace("-", "_")
            for j in info_dict[i]:
                info_data.write('export %s_%s=\"%s\"\n'%(name, j, info_dict[i][j]))
        info_data.write('export CHANGES_URL=\"%s\"\n'%(git_log_url))
    info_data.close()
