#!/usr/bin/python
# -*- coding:utf-8 -*-

import xml.etree.ElementTree as ET

class XMLAPI:
    def __init__(self, path):
        self.path = path
        self.tree = ET.parse(self.path)
        self.root = self.tree.getroot()

    def get_dict(self):
        info = {}
        for default in self.root.findall('default'):
            default_branch = default.get('revision')
        for project in self.root.findall('project'):
            prj_name = project.get('name')
            prj_path = project.get('path')
            if not info.has_key(prj_name):
                info[prj_name] = {}
            info[prj_name]['path'] = prj_path
            if project.get('revision'):
                info[prj_name]['revision'] = project.get('revision')
            else:
                info[prj_name]['revision'] = default_branch
            if project.get('clone-depth'):
                info[prj_name]['depth'] = project.get('clone-depth')
            else:
                info[prj_name]['depth'] = "default"
            if project.get('groups'):
                info[prj_name]['groups'] = project.get('groups')
            else:
                info[prj_name]['groups'] = "no-group"
        return info

    def insert_new_prj(self, name, path, *args):
        node_lens = len(self.root) - 1
        newNode = ET.Element('project')
        newNode.attrib['name'] = name
        newNode.attrib['path'] = path
        if len(args) >= 1:
            newNode.attrib['revision'] = args[0]
        newNode.tail = '\n  '
        self.root.insert(node_lens, newNode)
        self.tree.write(self.path,'utf-8',True)

'''
if __name__ == "__main__":
    xml = XMLAPI("default.xml")
    xml_dict = xml.get_dict()
    print xml_dict
    xml.insert_new_prj("bb", "workspace/bb")
'''
