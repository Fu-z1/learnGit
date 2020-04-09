# Bob build tool
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Generator for SmartGit
#
# SmartGit stores repositories in it's settings directory in a file named
# repositories.xml
#
# The location of the settings directory can be set in VM Options:
# https://www.syntevo.com/doc/display/SG/VM+options#VMoptions-settings-dir.change-location
#
# This generator generates a new settings dir by copying and modifying the vm settings and
# a startup script.
#
# Therefor the generator needs at least one environment variable named 'SMARTGIT_HOME'
# pointing to SmartGit install dir. If you have allready changed the settings dir you'll
# need to point to the new one by setting 'SMARTGIT_SETTINGS' env var.
#

import argparse
import re
import os
import shutil,errno,stat
from pipes import quote
from os.path import expanduser
from collections import OrderedDict

# scan package recursivelely with its dependencies and build a list of checkout dirs
def getCheckOutDirs(package, dirs):
    if package.getCheckoutStep().isValid():
        dirs.append([package.getName(), package.getCheckoutStep().getWorkspacePath()])
    for d in package.getDirectDepSteps():
        getCheckOutDirs(d.getPackage(), dirs)

def generateFile(entries, fileName):
    try:
        os.remove(fileName)
    except OSError:
        pass
    fileName = open(fileName, "w")
    for e in entries:
        fileName.write(e + "\n")
    fileName.close()

def generateSmartGit(package, destination, projectName, args):
    project = "/".join(package.getStack())

    dirs = []
    getCheckOutDirs(package, dirs)
    if not projectName:
        # use package name for project name
        projectName = package.getName()
    if not destination:
        # use package stack for project directory
        destination = os.path.join(os.getcwd(), "projects", "_".join(package.getStack()))
        destination = destination.replace(':', '_')
    if not os.path.exists(destination):
        os.makedirs(destination)

    smartgitHome = os.environ.get('SMARTGIT_HOME')
    if not smartgitHome:
        print("No SMARTGIT_HOME Environment variable defined!")
        return 1

    newSettingsDir = os.path.join(destination, "settings")

    smartgitSettings = os.getenv('SMARTGIT_SETTINGS', os.path.join(expanduser('~'), ".smartgit"))
    # try to get the version number
    versionDirExp = re.compile(r""+smartgitSettings+ os.path.sep + "([0-9]+)\Z")
    versions = []
    for root, directories, filenames in os.walk(smartgitSettings):
        if versionDirExp.match(root):
            versions.append(versionDirExp.match(root).group(1))

    smartGitVersion = max(versions)
    if len(versions) > 1:
        print("Warning: looks like there is more than one version installed. Assuming you're using the latest one ("+smartGitVersion+")")

    # generate a new startup file to setup new setting dir
    with open(os.path.join(smartgitHome, "bin", "smartgit.sh"), "r") as o:
        with open(os.path.join(destination, "smartgit.sh"), "w") as n:
            for line in o:
                if 'PRG=$0' in line:
                    n.write("PRG=" + os.path.join(smartgitHome, "bin", "smartgit.sh")+"\n")
                else:
                    n.write(line)
                if '_GC_OPTS="' in line:
                    n.write('_VM_PROPERTIES="$_VM_PROPERTIES -Dsmartgit.settings="' + newSettingsDir + '\n')
    os.chmod(os.path.join(destination, "smartgit.sh"), stat.S_IRWXU | stat.S_IRGRP | stat.S_IWGRP |
        stat.S_IROTH | stat.S_IWOTH)
    # copy old settings dir
    if os.path.exists(newSettingsDir):
        shutil.rmtree(newSettingsDir)

    try:
        shutil.copytree(os.path.join(smartgitSettings, smartGitVersion), newSettingsDir)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

    repoFile = os.path.join(newSettingsDir, "repositories.xml")
    toRemove = [ os.path.join(newSettingsDir, "projects.xml") ,
            os.path.join(newSettingsDir, "log.txt"), repoFile]

    for f in toRemove:
        if os.path.exists(f):
            os.remove(f)

    def addRepo(file, name, path,id):
        r.write('  <obj key="" type="@Repository" id="_ID_' + str(id) + '">\n')
        r.write('   <prop key="name" value="'+name+'" type="String"/>\n')
        r.write('   <prop key="favorite" value="false" type="boolean"/>\n')
        r.write('   <prop key="git" value="true" type="boolean"/>\n')
        r.write('   <prop key="path" value="'+path+'" type="String"/>')
        r.write('   <prop key="path.absolute" value="'+path+'" type="String"/>\n')
        r.write('  </obj>\n')

    gitDirExp = re.compile(r".*"+os.path.sep+".git\Z")
    with open(repoFile, "w") as r:
        r.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        r.write('<obj key="Repositories" type="@Repositories" id="_ID_1">\n')
        r.write(' <collection key="repositories" type="Object">\n')
        id = 2
        groups = []
        for pname,path in OrderedDict(sorted(dirs, key=lambda t: t[1])).items():
            groupMembers = []
            for root, directories, filenames in os.walk(path):
                if gitDirExp.match(root):
                    root = root[:-5]
                    name = root.split(os.path.sep)
                    name = name[len(name)-1]
                    addRepo(r, name, os.path.join(os.getcwd(), root), id)
                    groupMembers.append(id)
                    id += 1
            groups.append([pname, groupMembers])

        r.write(' </collection>\n')
        r.write(' <collection key="groups" type="Object">\n')

        gid = id
        for name, members in groups:
            r.write('   <obj key="" type="@Group" id="_ID_'+str(id)+'">\n')
            r.write('    <prop key="name" value="' + name +'" type="String"/>\n')
            r.write('    <prop key="expanded" value="false" type="boolean"/>\n')
            r.write('   </obj>\n')
            id += 1
        r.write(' </collection>\n')

        r.write(' <collection key="mapping" type="Object">\n')
        for n,members in groups:
            for m in members:
                r.write('   <obj key="" type="@RepositoryToGroup" id="_ID_'+str(id)+'">\n')
                r.write('    <ref key="repository" type="@Repository" id="_REF_'+str(m)+'"/>\n')
                r.write('    <ref key="group" type="@Group" id="_REF_'+str(gid)+'"/>\n')
                r.write('   </obj>\n')
                id += 1
            gid += 1
        r.write(' </collection>\n')

        r.write(' <collection key="reopenAtStartup" type="Reference">\n')
        r.write('  <ref key="" type="@Repository" id="_REF_3"/>\n')
        r.write(' </collection>\n')
        r.write(' <collection key="recentlyUsed" type="Reference">\n')
        r.write('  <ref key="" type="@Repository" id="_REF_3"/>\n')
        r.write(' </collection>\n')
        r.write('</obj>\n')


def smartgit(package, argv, extra):
    parser = argparse.ArgumentParser(prog="bob project smartgit", description='Generate QTCreator Project Files')
    parser.add_argument('--destination', metavar="DEST",
        help="Destination of project files")
    parser.add_argument('--name', metavar="NAME",
        help="Name of project. Default is complete_path_to_package")

    args = parser.parse_args(argv)
    extra = " ".join(quote(e) for e in extra)
    generateSmartGit(package, args.destination, args.name, extra)

manifest = {
    'apiVersion' : "0.5",
    'projectGenerators' : {
        'smartgit' : smartgit,
    }
}
