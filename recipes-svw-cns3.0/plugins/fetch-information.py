import argparse
import os, sys
import pprint as pp
from bob.state import BobState
import bob.utils as bu
import json
from urllib.parse import urljoin

buildstate = None
bobstate = BobState()

def getBuildState():
    return bobstate.getBuildState()

def getHashOfDir(path):
    return bu.asHexStr(buildstate[path]) if path in buildstate.keys() else ''

def getStepInputHash(path):
    hashes = bobstate.getInputHashes(path)
    if isinstance(hashes, list) and len(hashes)>0:
        hashes = hashes[0]
    try:
        result = bu.asHexStr(hashes)
    except:
        print("Can't get BuildId of path:", path, sep=' ')
        print("Abort!")
        sys.exit(1)
    return result

def getPackageDir(package):
    return package.getPackageStep().getWorkspacePath()

def getBuildDir(package):
    return package.getBuildStep().getWorkspacePath()

def getCheckoutDir(package):
    return package.getCheckoutStep().getWorkspacePath()

def isDownloaded(package):
    packageDir = getPackageDir(package)
    buildDir = getBuildDir(package)
    return getHashOfDir(packageDir) and not getHashOfDir(buildDir)

def isUploaded(package):
    packageDir = getPackageDir(package)
    buildDir = getBuildDir(package)
    return getHashOfDir(packageDir) and getHashOfDir(buildDir)

def getDownloads(packages):
    def getDict(dep, result):
        if isDownloaded(dep.getPackage()):
            varId = bu.asHexStr(dep.getVariantId())
            if varId in result.keys():
                return
            result[varId] = dict()
            result[varId]['name'] = dep.getPackage().getName()
            result[varId]['buildId'] = getStepInputHash(dep.getWorkspacePath())

    result = dict()
    if isinstance(packages,list):
        for package in packages:
            for dep in package.getAllDepSteps():
                getDict(dep, result)
            getDict(package.getPackageStep(), result)
    else:
        for dep in packages.getAllDepSteps():
            getDict(dep, result)
        getDict(packages.getPackageStep(), result)

    return result

def getUploads(packages):
    def getDict(package, result):
        if isUploaded(package):
            varId = bu.asHexStr(package.getPackageStep().getVariantId())
            if varId in result.keys():
                return
            result[varId] = dict()
            result[varId]['name'] = package.getName()
            result[varId]['buildId'] = getStepInputHash(getPackageDir(package))

    result = dict()
    if isinstance(packages, list):
        for package in packages:
            getDict(package, result)
    else:
            getDict(packages, result)

    return result

def getPath(packages, step):
    def getDict(package, step, result):
        stepFunc = {'Checkout': package.getCheckoutStep,
                    'Build': package.getBuildStep,
                    'Package': package.getPackageStep}

        stepObj = stepFunc[step]()
        varId = bu.asHexStr(stepObj.getVariantId())
        if varId in result.keys():
            return
        result[varId] = dict()
        result[varId]['name'] = package.getName()
        result[varId]['path'] = stepObj.getWorkspacePath() if getHashOfDir(stepObj.getWorkspacePath()) else None

    result = dict()
    if isinstance(packages, list):
        for package in packages:
            getDict(package, step, result)
    else:
            getDict(packages, step, result)
    return result

def getDatabaseInformation(packages, uploadurl):
    def getDict(package, result, uploadurl):
        if not package.getName().startswith('zr3-variant-'):
            print(package.getName(), "is not a zr3-variant package", sep=' ')
            return
        packageStep = package.getPackageStep()
        varId = bu.asHexStr(packageStep.getVariantId())
        if varId in result.keys():
            return
        try:
            release = dict()
            release['name'] = packageStep.getEnv()['TRAIN_NUMBER'][-5:-1]

            release_candidate = dict()
            release_candidate['no'] = packageStep.getEnv()['BUILDREF']

            update_container = dict()
            update_container['name'] = package.getName()
            update_container['train_name'] = packageStep.getEnv()['TRAIN_NUMBER']
            update_container['build_id'] = getStepInputHash(packageStep.getWorkspacePath())
            update_container['mu_version'] = packageStep.getEnv()['MU_VERSION']
            update_container['binary_url'] = uploadurl + "/".join([update_container['build_id'][:2],
                                                               update_container['build_id'][2:4],
                                                               update_container['build_id'][4:]]) + '-1.tgz'

            result[varId] = dict()
            result[varId]['release'] = release
            result[varId]['release_candidate'] = release_candidate
            result[varId]['update_container'] = update_container
            result[varId]['audit_trail_path'] = urljoin(packageStep.getWorkspacePath(), "audit.json.gz")
        except:
            print("Could not generate json for", package.getName(), sep=' ')
            sys.exit(1)
    result = dict()
    if uploadurl[-1] != '/':
        uploadurl += '/'
    if isinstance(packages, list):
        for package in packages:
            getDict(package, result, uploadurl)
    else:
            getDict(packages, result, uploadurl)
    return result

def fetchInformation(packages, argv, extra):
    global buildstate
    parser = argparse.ArgumentParser(prog="bob project fetch-information", description='Get special information from state')
    parser.add_argument('--info', choices=['downloads', 'uploads', 'downanduploads',
                                           'checkout', 'build', 'package', 'database'])
    parser.add_argument('--output', choices=['json', 'bash-path'], default='json')
    parser.add_argument('--uploadurl', required=False)
    args = parser.parse_args(argv)
    buildstate = getBuildState()
    if not buildstate:
       return
    result = {}
    if not args.info:
        print("Please choose information: 'downloads', 'uploads', 'downanduploads', \
               'checkout', 'build', 'package', 'database'")
        sys.exit(1)
    if args.info in ['downloads', 'downanduploads']:
        result['downloads'] = dict()
        result['downloads'] = getDownloads(packages)
    if args.info in ['uploads', 'downanduploads']:
        result['uploads'] = dict()
        result['uploads'] = getUploads(packages)
    if args.info in ['checkout', 'build', 'package']:
        result[args.info] = dict()
        result[args.info] = getPath(packages, args.info.capitalize())
    if args.info in ['database']:
        if not args.uploadurl:
            print('Please input an upload url! (--uploadurl)')
            sys.exit(1)
        result[args.info] = dict()
        result[args.info] = getDatabaseInformation(packages, args.uploadurl)

    print(result)
    if args.output == 'json':
        jsonFileName = "info.json"
        with open(jsonFileName, 'w') as jsonFile:
          json.dump(result, jsonFile, sort_keys=True, indent=4)

    if args.output == 'bash-path':
        bashFileName = "information.txt"
        if args.info in ['checkout', 'build', 'package']:
            dicts = [dict(v)['path'] for (k,v) in result[args.info].items() if dict(v)['path'] is not None]
            with open(bashFileName, 'w') as bashFile:
                bashFile.write("\n".join(dicts))
        else:
            print("bash-path not possible for ", args.info, ". Only checkout, build and package", sep='')

manifest = {
    'apiVersion' : "0.10",
    'projectGenerators' : {
        'fetch-information' : fetchInformation,
    }
}
