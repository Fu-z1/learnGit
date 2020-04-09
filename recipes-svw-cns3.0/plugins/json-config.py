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

# Generator for Jenkins config templates

import argparse
from os.path import join
import json
import re

class Job:

    def __init__(self, jobName):
        self.__name = jobName
        self.__multiPackageList = []

    def addMultiPackage(self, multiPkg):
        self.__multiPackageList.append(multiPkg)

    def getName(self):
        return self.__name

    def getMultiPackageList(self):
        return self.__multiPackageList


class MultiPackage:

    def __init__(self, packageName, recipeName):
        self.__name = packageName
        self.__recipeName = recipeName
        self.__variantList = []
        self.__deps = []
        self.__packageList = []

    def addPackage(self, pkg):
        if pkg.getName() == self.__name and pkg.getRecipeName() == self.__recipeName:
            if pkg.getVariantId() not in self.__variantList:
                self.__packageList.append(pkg)
                self.__variantList.append(pkg.getVariantId())
                for dep in pkg.getDependencies():
                    self.__deps.append(dep)

    def setJobName(self, jobName):
        for pkg in self.__packageList:
            pkg.setJobName(jobName)

    def getName(self):
        return self.__name

    def getRecipeName(self):
        return self.__recipeName

    def getVariantList(self):
        return self.__variantList

    def getDependencies(self):
        return self.__deps

    def getPackages(self):
        return self.__packageList


class Package:

    def __init__(self, packageName, variantId, variant, recipeName):
        self.__name = packageName
        self.__variantId = variantId
        self.__variant = variant
        self.__recipeName = recipeName
        self.__scms = []
        self.__deps = []
        self.__directDeps = []
        self.__tools = set()
        self.__srcDir = set()
        self.__jobName = recipeName
        self.__klocwork = False

    def setVariant(self, variantId, stack):
        self.__variantId = variantId
        self.__variant = stack

    def setRecipeName(self, recipeName):
        self.__recipeName = recipeName

    def addDependency(self, packageName):
        if packageName not in self.__deps and packageName != self.__name:
            self.__deps.append(packageName)

    def addDirectDependency(self, packageName):
        if packageName not in self.__directDeps and packageName != self.__name:
            self.__directDeps.append(packageName)

    def setScmList(self, scmList):
        self.__scms = scmList

    def setSrcDir(self, dir):
        self.__srcDir.add(dir)

    def setTools(self, tools):
        self.__tools.update(tools)

    def setName(self, packageName):
        self.__name = packageName

    def setJobName(self, jobName):
        self.__jobName = jobName

    def setKlocwork(self, kw):
        self.__klocwork = kw

    def getName(self):
        return self.__name

    def getRecipeName(self):
        return self.__recipeName

    def getVariantId(self):
        return self.__variantId

    def getVariant(self):
        return self.__variant

    def getDependencies(self):
        return self.__deps

    def getDirectDependencies(self):
        return self.__directDeps

    def getScmList(self):
        return self.__scms

    def getSrcDir(self):
        return self.__srcDir

    def getTools(self):
        return self.__tools

    def getJobName(self):
        return self.__jobName

    def getKlocwork(self):
        return self.__klocwork


allVariantIds = []

packageList = {}
multiPackageList = {}
jobList = {}

splitMultiPackages = {}
splitJobs = {}

multiPkgCycles = []
jobCycles = []
multiPkgBlackList = []

variantNames = {}

klocworkWhiteListPattern = ['__ext-vw-carssw',
                            '__ext-vw-carssw-viwicarservice',
                            '__ext-vw-carssw-viwinavsdclient',
                            '__ext-vw-rsi-notificationservice',
                            '__ext-vw-rsi-onlineremoteupdate',
                            '__ext-vw-rsi-psodataexchange',
                            '__ext-vw-rsi-serviceregistry',
                            '__ext-vw-rsi-usermanagement',
                            '__ext-arm-trusted-firmware']
klocworkBlackList = ['sds__asr__resources',
                     'basic-services__persistence__tsd-persistence-client-mib3-initPersApp-pkg',
                     'sds__tts__tsd-sds-tts-app-mib3-config',
                     'system__tsd-swupdate-app-pkg',
                     'audio__microphoneprocessing__tsd-audio-microphoneprocessing-plugins-target']
toolchainSet = {'toolchain__aarch64-linux-gnu', 'toolchain__arm-bare-m0-eabi', 'toolchain__xtensa__xtensa-xcc', 'toolchain__i686-w64-mingw32', 'toolchain__arm-bare_newlib_cr7-eabi'}


def check_module_length(step):
    script = step.getScript()
    if 'buildSwupModule' in script:
        res = re.findall(r'[.\n\s]+buildSwupModule[.\n\s]+-n\s+["\']?([^"\' \n]+)', script)
        fail = '\033[91m'
        warning = '\033[93m'
        end = '\033[0m'
        if res:
            with open('config.warnings', 'a') as fd:
                for x in res:
                    if "$" in x:
                        print(warning, "WARNING - Check module name and length manually:", x, end, file=fd)
                    elif len(x) > 31:
                        print(fail, "ERROR - module name is longer than 31 characters:", x, end, file=fd)
                    if 'tsd-' in x:
                        print(fail, "ERROR - module name contains 'tsd-':", x, end, file=fd)


def getPackages(step, parent):
    if step.isValid():
        variantId = ''.join(format(x, '02x') for x in step.getVariantId())

        if step.isPackageStep():
            if variantId in allVariantIds:
                return
            else:
                allVariantIds.append(variantId)

        stepPkg = step.getPackage()
        packageName = stepPkg.getName().replace(':', '_')
        recipeName = stepPkg.getRecipe().getName().replace(':', '_')
        variant = "/".join(stepPkg.getStack())
        variantNames[variantId] = packageName

        if step.isPackageStep():
            pkg = Package(packageName, variantId, variant, recipeName)
            scmList = stepPkg.getCheckoutStep().getScmList()

            pkg.setScmList(scmList)
            pkg.setTools(set(step.getTools()))
            if scmList:
                pkg.setSrcDir('work/' + recipeName.replace('__', '/') + '/src')

            packageList[variantId] = pkg
            check_module_length(step)
        else:
            pkg = parent

        pkgDepSteps = stepPkg.getDirectDepSteps()
        for dep in step.getAllDepSteps(True):
            if dep.isValid():
                if dep.isPackageStep():
                    depName = ''.join(format(x, '02x') for x in dep.getVariantId())
                    if dep.getPackage().getName() != stepPkg.getRecipe().getName():
                        pkg.addDependency(depName)
                        if dep in pkgDepSteps:
                            pkg.addDirectDependency(depName)

                getPackages(dep, pkg)


def splitMultiPackage(multiPkg):
    count = 1
    multiPkgName = multiPkg.getName()
    multiPkgRecipeName = multiPkg.getRecipeName()
    variantList = []
    for pkg in multiPkg.getPackages():
        variantList.append(pkg.getVariant())
    variantList.sort()
    variantMap = {}
    for var in variantList:
        variantMap[var] = count
        count += 1
    for pkg in multiPkg.getPackages():
        packageName = multiPkgName + '-' + str(variantMap[pkg.getVariant()])
        variantNames[pkg.getVariantId()] = packageName
        pkg.setName(packageName)
        multiPkg = MultiPackage(packageName, multiPkgRecipeName)
        multiPkg.addPackage(pkg)
        splitMultiPackages[packageName] = multiPkg
    multiPkgCycles.append(multiPkgName)
    multiPkgBlackList.append(multiPkgRecipeName)


def traverseDeps(pkg, multiDepList, depList, recipeDepList):
    for dep in pkg.getDependencies():
        if dep not in depList:
            multiDepList.add(variantNames[dep])
            depList.add(dep)
            recipeDepList.add(packageList[dep].getRecipeName())
            traverseDeps(packageList[dep], multiDepList, depList, recipeDepList)


def fixMultiPackageCycles(multiPkg):
    recursiveDepList = set()
    recursiveRecipeDepList = set()
    for pkg in multiPkg.getPackages():
        pkgDepList = set()
        multiPkgDepList = set()
        recipeDepList = set()
        traverseDeps(pkg, multiPkgDepList, pkgDepList, recipeDepList)
        recursiveDepList.update(multiPkgDepList)
        recursiveRecipeDepList.update(recipeDepList)
    if multiPkg.getName() in recursiveDepList:
        splitMultiPackage(multiPkg)

    recipeName = multiPkg.getRecipeName()
    if recipeName in recursiveRecipeDepList and recipeName not in multiPkgBlackList:
        multiPkgBlackList.append(recipeName)


def checkWhiteList(name):
    for item in klocworkWhiteListPattern:
        if item in name:
            return True
    return False


def checkKlocwork(pkg):
    if (not '__ext-' in pkg.getJobName() or checkWhiteList(pkg.getJobName())):
        deps = set()
        for dep in pkg.getDependencies():
            deps.add(packageList[dep].getJobName())
        if deps.intersection(toolchainSet) and \
                'toolchain__cmake' in deps and \
                'capi-generator' not in pkg.getTools():
            for scm in pkg.getScmList():
                if isinstance(scm.getProperties(), dict):
                    scmType = scm.getProperties()['scm']
                else: #assuming it's a list of one element
                    scmType = scm.getProperties()[0]['scm']
                if (scmType  == 'git') and (pkg.getJobName() not in klocworkBlackList):
                    return True
    return False


def getMultiPackages():
    for variantId, pkg in packageList.items():
        packageName = pkg.getName()
        recipeName = pkg.getRecipeName()
        if packageName in multiPackageList.keys():
            multiPkg = multiPackageList[packageName]
        else:
            multiPkg = MultiPackage(packageName, recipeName)
            multiPackageList[packageName] = multiPkg
        multiPkg.addPackage(pkg)

    for multiPkgName, multiPkg in multiPackageList.items():
        fixMultiPackageCycles(multiPkg)

    for multiPkg in multiPkgCycles:
        del multiPackageList[multiPkg]

    multiPackageList.update(splitMultiPackages)


def getJobs():
    for multiPkgName, multiPkg in multiPackageList.items():
        jobName = multiPkg.getRecipeName() if multiPkg.getRecipeName() not in multiPkgBlackList else multiPkg.getName()
        if jobName in jobList.keys():
            job = jobList[jobName]
        else:
            job = Job(jobName)
            jobList[jobName] = job
        job.addMultiPackage(multiPkg)
        multiPkg.setJobName(jobName)

    for variantId, pkg in packageList.items():
        pkg.setKlocwork(checkKlocwork(pkg))


def generateJSONTemplate(jsonFileName):
    result = []

    for jobName, job in sorted(jobList.items()):
        v = dict()
        variants = []
        variantIds = {}
        deps = set()
        directDeps = set()
        scmList = []
        overridden = False
        klocwork = False
        srcDirs = set()
        for multiPkg in job.getMultiPackageList():

            for pkg in multiPkg.getPackages():
                variants.append(pkg.getVariant())
                variantIds[pkg.getVariantId()] = pkg.getVariant()
                for dep in pkg.getDependencies():
                    deps.add(packageList[dep].getJobName())
                for dep in pkg.getDirectDependencies():
                    directDeps.add(packageList[dep].getJobName())
                for scm in pkg.getScmList():
                    if isinstance(scm.getProperties(), dict):
                        prop = scm.getProperties()
                        if prop not in scmList:
                            scmList.append(prop)
                    else: #assuming a list of properties
                        for prop in scm.getProperties():
                            if prop not in scmList:
                                scmList.append(prop)
                    overridden = bool(scm.getActiveOverrides()) or overridden
                klocwork = bool(pkg.getKlocwork()) or klocwork
                srcDirs.update(pkg.getSrcDir())
        v['name'] = jobName
        v['variants'] = sorted(variants)
        v['variantIds'] = variantIds
        v['deps'] = sorted(list(deps))
        v['directDeps'] = sorted(list(directDeps))
        v['scm'] = sorted(scmList, key=lambda x: (x['url'], x['recipe']))
        v['klocwork'] = klocwork
        v['srcDirs'] = list(srcDirs)
        v['overridden'] = overridden
        result.append(v)

    jsonFile = open(jsonFileName, 'w')
    json.dump(result, jsonFile, sort_keys=True, indent=4)
    jsonFile.close


def filterPackages(package, argv):
    result = []
    for item in argv:
        tmp = __filterPackages(package.getPackageStep(), item.split('/'))
        if tmp:
            result.append(tmp)
    return result


def __filterPackages(step, item):
    result = None
    if step.isValid() and item:
        if len(item) == 1:
            if step.getPackage().getName() == item[0]:
                return step.getPackage()
        else:
            for dep in step.getAllDepSteps(True):
                if dep.isValid():
                    if dep.getPackage().getName() == item[1]:
                        item.pop(0)
                        result = __filterPackages(dep, item)
                        if result:
                            return result
                    elif dep.getPackage() == step.getPackage():
                        result = __filterPackages(dep, item)
                        if result:
                            return result

    return result


def jsonConfigGenerator(package, argv, extra):
    parser = argparse.ArgumentParser(prog="bob project json-config", description='Generate a JSON configuration template')
    if argv:
        packagelist = filterPackages(package, argv)
    else:
        packagelist = [package]

    open('config.warnings', 'w').close()
    for pkg in packagelist:
        multiPkgBlackList.append(pkg.getRecipe().getName().replace(':', '_'))
        getPackages(pkg.getPackageStep(), None)

    getMultiPackages()

    getJobs()

    generateJSONTemplate("config.json")


manifest = {
    'apiVersion' : "0.13",
    'projectGenerators' : {
        'json-config' : jsonConfigGenerator,
    }
}
