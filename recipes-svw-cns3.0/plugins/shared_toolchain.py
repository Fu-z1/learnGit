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


class Job:

    def __init__(self, jobName):
        self.__name = jobName
        self.__variants = {}
        self.__variantIds = []
        self.__scms = []
        self.__deps = []
        self.__provideTools = False

    def addDependency(self, jobName):
        if jobName not in self.__deps and jobName not in self.__name:
            self.__deps.append(jobName)

    def addScmList(self, scmList):
        self.__scms = scmList

    def addVariant(self, variantId, stack):
        if variantId not in self.__variantIds:
            self.__variantIds.append(variantId)
            self.__variants[variantId] = stack

    def setProvideTools(self, provideTools):
        self.__provideTools = provideTools

    def getDependencies(self):
        return self.__deps

    def getName(self):
        return self.__name

    def getScmList(self):
        return self.__scms

    def getVariants(self):
        return self.__variants

    def doesProvideTools(self):
        return self.__provideTools

    def replaceDependency(self, old, new):
        if old in self.__deps:
            self.__deps.remove(old)
            self.__deps.append(new)
        
jobNames = []
jobs = {}
allVariantIds = []
whiteList = ['images__rootfs', 'zr3-variant']
matchingJobs = {}
affectedJobs = []
affectedDeps = []

def getStepVariants(step, suffix):
    if step.isValid():
        variantId = step.getVariantId()
        if variantId in allVariantIds:
            return
        else:
            allVariantIds.append(variantId)

        variant = "/".join(step.getPackage().getStack())

        packageName = step.getPackage().getName().replace(':', '_')
        recipeName = step.getPackage().getRecipe().getName().replace(':', '_')

        jobName = recipeName
        
        multiPackage = packageName.replace(jobName, '')
        if len(multiPackage) > 0:
            newSuffix = multiPackage
        else:
            newSuffix = suffix

        if jobName in whiteList:
            jobName = jobName + newSuffix
            matchingJobs["%s"%variantId] = jobName
            affectedDeps.append("%s"%variantId)

        if jobName not in jobNames:
            jobNames.append(jobName)
            job = Job(jobName)
            jobs[jobName] = job
        else:
            job = jobs[jobName]

        if step.isPackageStep():
            job.addVariant(variantId, variant)

        if step.isCheckoutStep():
            job.addScmList(step.getScmList())

        if step.doesProvideTools() and step.isShared():
            job.setProvideTools(step.doesProvideTools())


        for dep in step.getAllDepSteps():
            if dep.isValid():
                depName = dep.getPackage().getRecipe().getName().replace(':', '_')
                if depName != recipeName:
                    if depName in whiteList:
                        if job not in affectedJobs: affectedJobs.append(job)
                        depName = "%s"%dep.getVariantId()

                    job.addDependency(depName)

                getStepVariants(dep, newSuffix)


def generateJSONTemplate(jsonFileName): #, destination, updateOnly, projectName, args):
    result = []

    for job in affectedJobs:
        for variantId in affectedDeps:
            job.replaceDependency(variantId, matchingJobs[variantId])

    filtered_jobs = [v for k,v in jobs.items() if v.doesProvideTools()]
    v = dict()
    v['name'] = "deploy_shared_toolchain_on_slaves"
    v['variants'] = []
    v['deps'] = []
    v['scm'] = []

    for job in filtered_jobs:
        variantList = []
        variants = job.getVariants()
        variantList = [v for k, v in variants.items()]
        # build steps
        v['variants'].extend(variantList)
        # deps
        # scm info (needed by hooks)
        scmList = []
        for scm in job.getScmList():
            scmList.extend(scm.getProperties())
        v['scm'].extend(scmList)

    result.append(v)

    jsonFile = open(jsonFileName, 'w')
    json.dump(result, jsonFile, sort_keys=True, indent=4)
    jsonFile.close


def jsonConfigGenerator(packages, argv, extra):
    parser = argparse.ArgumentParser(prog="bob project json-config", description='Generate a JSON configuration template')
    if isinstance(packages, list):
        for package in packages:
            getStepVariants(package.getPackageStep(), '')
    else:
        getStepVariants(packages.getPackageStep(), '')

    generateJSONTemplate("toolchains.json")


manifest = {
    'apiVersion' : "0.10",
    'projectGenerators' : {
        'shared_toolchain' : jsonConfigGenerator,
    }
}
