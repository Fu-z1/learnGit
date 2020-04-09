#!/usr/bin/env python3
from collections import OrderedDict
from collections import namedtuple
from pprint import pformat

import argparse
import csv
import json
import os
import re
import sys
from pccProject import PccProject



SystemVariantInfo = namedtuple('SystemVariantInfo', 'project boot_mode sop variant')
ContainerInfo = namedtuple('ContainerInfo', 'container_prefix train_prefix train_boot_mode')


Projects = PccProject.InitProjectList()

TRAIN_SUPPLIER_SUFFIX = {
    'MOI3': 'P',
    'CNS3': 'J'
}

# Gets populated after passing command line arguments.
train_boot_mode_by_boot_mode = {}

DEVELOPER_BOOT_MODE = 0
CUSTOMER_BOOT_MODE = 1


def add_update_variant_info(infos, info):
    infos.append(info)

    # Upward and backward compatibility quirks for older software update
    # applications using a system information proider with wrong RdW2 region
    # strings (R2 instead of W2). See
    # https://wiki-automotive.server.technisat-digital/pages/viewpage.action?pageId=375783909
    # for details.
    #
    # TODO: Remove up this quirks once the population of old software update
    # applications has died out in the field.
    match = re.match('^([^-]+-[^-]+-[^-]+-)W2(-[^-]+-[^-]+-[^-]+)$', info)
    if match:
        compatibility_info = match.group(1) + 'R2' + match.group(2)
        infos.append(compatibility_info)

    match = re.match('^([^-]+-[^-]+-[^-]+-)R2(-[^-]+-[^-]+-[^-]+)$', info)
    if match:
        compatibility_info = match.group(1) + 'W2' + match.group(2)
        infos.append(compatibility_info)


    # Upward and backward compatibility quirks for MQ2/37W variant 31. It has a
    # wrong region in its variant string which needs to be fixed but this
    # requires an upgrade path.
    #
    # TODO: Remove this quirks once the population of devices with the wrong
    # variant string has been completely updated.
    if info == 'FM3-S-NWBY4-RW-VW-MQ2-PC': infos.append('FM3-S-NWBY4-W2-VW-MQ2-PC')
    if info == 'FM3-S-NWBY4-W2-VW-MQ2-PC': infos.append('FM3-S-NWBY4-RW-VW-MQ2-PC')


def container_info_for_system_variant(system_variant):
    info = system_variant_info(system_variant)
    result = ContainerInfo(
        container_prefix=Projects[info.project].containerPrefix,
        train_prefix=Projects[info.project].trainPrefix,
        train_boot_mode=train_boot_mode_by_boot_mode[info.boot_mode])
    return result


def container_key_for_entry(entry):
   system_variant = entry.get('System Variant')
   info = container_info_for_system_variant(system_variant)
   return info.container_prefix + entry.get('Container Name')


def output_mu_type(entry, args):
    system_variant = entry.get('System Variant')
    info = system_variant_info(system_variant)
    result = entry.get('MU Type')

    if info.boot_mode == CUSTOMER_BOOT_MODE and args.customer_mu_type_override != None:
       result = args.customer_mu_type_override
    elif info.boot_mode == DEVELOPER_BOOT_MODE and args.developer_mu_type_override != None:
       result = args.developer_mu_type_override

    return result


def read_entries(file_names, file_format):

    entries = {}

    if file_format == "csv":
        for f in file_names:
            with open(f) as csvFile:
                reader = csv.DictReader(csvFile)
                # write zr3-variant.yaml entries. one for each container name.
                for row in reader:
                    entries.append(OrderedDict(sorted(row.items())))
    elif file_format == "json":
        for file in file_names:
            with open(file) as data_file:
                for entry in json.load(data_file):
                    if entry["System Variant"][0] not in entries.keys():
                        entries[entry["System Variant"][0]] = []
                    entries[entry["System Variant"][0]].append(entry)
    else:
        raise ValueError('Unsupported file format \'%s\'.' % file_format)

    return entries


def system_variant_info(system_variant):
    """
    Extracts system variant component information from a given system variant
    number (as a string).

    The numbering scheme is given in the variant matrix excel sheet. See:
        * https://dms-auto1.server.technisat-digital/svn/SVN_DMS_CARRADIO/OEM-Projekte/201601_VW_MIB3_OI_MQB/08_Entwicklung/081_System/MIB3_OI_MQB_Variantenmatrix_SOP1.xls
        * https://wiki-automotive.server.technisat-digital/display/MIB3SERIE/Systemkonzept%3A+Varianten#Systemkonzept:Varianten-Variantenmatrix
    """
    match = re.match('^\d+$', system_variant)
    if not match:
        raise ValueError('Unsupported system variant \'%s\'.' % system_variant)
    result = SystemVariantInfo(
        project=int(system_variant[:-5]),
        boot_mode=int(system_variant[-5:-4]),
        sop=int(system_variant[-4:-3]),
        variant=int(system_variant[-3:]))
    return result


def update_variants_string_for_infos(infos):
    infos.sort()
    return ','.join(infos)


def variants_string_for_system_variants(variants):
    variants.sort()
    return ','.join(map(str, variants))


def genVariants():
    global train_boot_mode_by_boot_mode

    parser = argparse.ArgumentParser(prog="genVariants",
                                     description="Generator for zr3-variant yaml entries. The main unit and train software version gets formed after the scheme 'pvvvd' - see description of options below.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--customer-prefix",
                        default='P',
                        help='customer software version prefix (\'p\')for train number, for example \'R\', \'P\', or \'K\'')
    parser.add_argument("--developer-prefix",
                        default='E',
                        help='developer software version prefix (\'p\') for train number, typically \'E\'')
    parser.add_argument("--customer-mu-type-override",
                        help='override main unit type for customer hardware (secure boot)')
    parser.add_argument("--developer-mu-type-override",
                        help='override main unit type for developer hardware (non-secure boot)')
    parser.add_argument("--format",
                        choices=['csv', 'json'],
                        default='json',
                        help='variant data file format')
    parser.add_argument('file',
                        nargs='+',
                        metavar='FILE',
                        help="variant data file")


    args = parser.parse_args(sys.argv[1:])

    train_boot_mode_by_boot_mode = \
        {
            DEVELOPER_BOOT_MODE: args.developer_prefix,
            CUSTOMER_BOOT_MODE: args.customer_prefix,
        }


    entries_dict = read_entries(args.file, args.format)
    containers = []
    for project, entries in entries_dict.items():
        with open(project + '-variant.fragment.yaml', 'w') as f:
           # Write info/instructions header for the fragment.
           f.write("   # Variant package fragment generated by genVariants.py. Do not waste your\n")
           f.write("   # time with editing. Re-generate variant data from and with pure::variants\n")
           f.write("   # JSON export and genVariants.py.\n")
           f.write("   #\n")
           f.write("   # The lines below are intended to be used as multiPackage elements in\n")
           f.write("   # zr3-variant.yaml.\n")

           # add variants we want to build to zr3-variant.yaml. I'm using
           # 'Container Name' for now to define the varinats in a container.
           container = ''
           # Output container infos in a defined order for diffs. Use the key
           # appearing in the YAML fragment because this order should be
           # intuitively understood by the readers.
           for row in sorted(entries, key=lambda entry: container_key_for_entry(entry)):
               system_variant = row.get('System Variant')
               info = container_info_for_system_variant(system_variant)

               # The user might have requested overriding the main unit type. As it
               # gets used for both artifacts, we'll fix-up the data itself.
               muType = output_mu_type(row, args)
               row['MU Type'] = muType

               container_name = row.get('Container Name')
               if container_name == '':
                   continue

               container = container_key_for_entry(row)
               if not container in containers:
                   f.write("   " + container + ":\n")
                   f.write("      environment:\n")
                   print('   - zr3-variant-'+container)
                   system_variants = []
                   update_variant_infos = []
                   platform = ""
                   trainNumber = ''
                   isProvidingTrainNumber = False

                   # Beware: The MU type might not be fixed up yet in this loop.
                   for row in entries:
                       system_variant = row.get('System Variant')
                       info = container_info_for_system_variant(system_variant)

                       c = row.get('Container Name')
                       c = info.container_prefix + c

                       if (c == container):
                           if len(system_variants) == 0:
                               isProvidingTrainNumber = PccProject.FromSystemVariantNo(system_variant).deliverUpdateContainer;
                               if ( isProvidingTrainNumber ):
                                   # I suggest here some more general region flag (and SW_HMI_REGION is contrained in PV model!)
                                   region = row.get('SW_HMI_REGION')
                                   if "RDW1" in row.get('Region'):
                                       region = "RW"
                                   elif "RDW2" in row.get('Region'):
                                       region = "RW"
                                   elif row.get('Region').endswith("RDW"):
                                       region = "RW"
                                   # build a Train Number using the fields we
                                   # have:
                                   # (MOI3|M37W)_REGION_BRAND_E<version>0P"
                                   # trainNumber = info.train_prefix \
                                   #    + '_' + region.upper() \
                                   #    + "_" + row.get('SW_HMI_BRAND').upper() \
                                   #    + "_" + info.train_boot_mode + args.version + str(args.delivery) + TRAIN_SUPPLIER_SUFFIX

                                   # MOI3_<REGION>_<BRAND><PLATFORM>_E<version>0P"
                                   platform = row.get('SW_HMI_PROJECT').upper()
                                   trainNumber = info.train_prefix \
                                       + '_' + region.upper() \
                                       + "_" + row.get('SW_HMI_BRAND').upper() + platform \
                                       + "_" + info.train_boot_mode + "${MAJOR}" + "${DELIVERY}" + TRAIN_SUPPLIER_SUFFIX[info.train_prefix]

                           system_variants.append(system_variant)
                           add_update_variant_info(update_variant_infos, row.get('Variant Info String'))

                   variants = variants_string_for_system_variants(system_variants)
                   update_variants = update_variants_string_for_infos(update_variant_infos)
                   f.write("         MU_VERSION: \"" + muType + "${MAJOR}" + "\"\n")
                   if ( isProvidingTrainNumber ):
                       f.write("         TRAIN_NUMBER: \"" + trainNumber + "\"\n")
                   f.write("         VARIANTS: \"" + variants + "\"\n")
                   f.write("         PLATFORM: \"" + platform + "\"\n")
                   if ( "_sec" in container.lower() ):
                       f.write("         SIGNATURE: \"false\"\n")
                       f.write("         DEVELOPMENT_FLAGS: \"false\"\n")
                   f.write("      privateEnvironment:\n")
                   f.write("         UPDATE_VARIANTS: \"" + update_variants + "\"\n")

               containers.append(container)

    with open('variants-helper.py', 'w') as f:
       f.write("# This file is generated! Do not edit manually! see contrib/genVariants.yaml\n")
       f.write("import sys\n")
       f.write("import re\n")
       f.write("from bob.errors import ParseError\n")
       f.write("\n")
       f.write("# HW_MATCH is a dictionary associating the supported hardware variants as keys\n")
       f.write("# to arrays of the supported hardware versions. For example,\n")
       f.write("# {'42' : ['47', '11']} means hardware variant 42 in versions 47 and 11 is\n")
       f.write("# supported.\n")
       f.write("variants = {\n")
       # Output system variants in a defined order for having clean artifact
       # diffs.
       for e in sorted([item for sublist in list(entries_dict.values()) for item in sublist], key=lambda entry: entry['System Variant']):
           sysVar = e['System Variant']
           del e['System Variant']
           f.write("  " + sysVar + " : {\n")
           # Output items in a defined order for diffs too.
           for k,v in sorted(e.items()):
               f.write("      '" + k + "' : " + pformat(v) + ",\n")
           f.write("   },\n")
       f.write("}\n\n")

       f.write("""
def getBrand(args, **kwargs):
    \"\"\"
    Get Brand

    Returns the Brand for a single system variant.

    Parameters
    ----------
    arg1: string
        System variant string (e.g. '100101')

    Returns
    -------
    string
        Brand (e.g 'VW')
    \"\"\"
    return variants[int(args[0])]['Brand']

def getRegion(args, **kwargs):
    \"\"\"
    Get Region

    Returns the Region for a single system variant.

    Parameters
    ----------
    arg1: string
        System variant string (e.g. '100101')

    Returns
    -------
    string
        Region (e.g 'EU')
    \"\"\"
    return variants[int(args[0])]['Region']

def getFeature(args, **kwargs):
    \"\"\"
    Get Feature value

    Returns the value of a feature for a single system variant.

    Parameters
    ----------
    arg1: string
        System variant string (e.g. '100101')
    arg2: string
        Feature-Key (e.g. 'SW_HMI_REGION)

    Returns
    -------
    string
        corresponding value (e.g 'EU')
    \"\"\"
    return variants[int(args[0])][args[1]]

def getUniqueFeatureFromList(args, **kwargs):
    \"\"\"
    Get Feature value

    Returns the value of a feature for a list of system variants.
    Raises an Error, if different features are defined.

    Parameters
    ----------
    arg1: string
        Comma separated list of System variant strings (e.g.
        '100101,100102,100103')
    arg2: string
        Feature-Key (e.g. 'SW_HMI_REGION)

    Returns
    -------
    string
        corresponding value (e.g 'EU')
    \"\"\"
    try:
        Features=[]
        for v in args[0].split(','):
           Features.append(variants[int(v)][args[1]])
        if len(set(Features)) == 1:
            return Features[0]
        else:
            raise ParseError(\"ERROR: multiple features defined for system variant \" + str(Features))
    except IndexError as e:
        raise ParseError(\"Index Error: \" + str(e) + \" Args:\" + str(args))
    except KeyError as e:
        raise ParseError(\"Key Error: \" + str(e) + \" Args:\" + str(args))
    return \"False\"

def getVariantInfoString(args, **kwargs):
    \"\"\"
    Get Variant Info String

    Returns the variant info string for a single system variant.

    Parameters
    ----------
    arg1: string
        System variant string (e.g. '100101')

    Returns
    -------
    string
        Variant Info String (e.g 'FM3-SM-NWBY4-EU-VW-MQB-PC')
    \"\"\"
    return variants[int(args[0])]['Variant Info String']

def getProjectNo(args, **kwargs):
    '''
    Get Project number related to https://wiki-automotive.server.technisat-digital/x/4wj-Gg

    Parameters
    ----------
    arg1: list of string
        System variant string (e.g. ['100101'])
        Attention: Uses just the first item in list!

    Returns
    -------
    integer
        1 - for PCC MQB
        2 - for PCC 37W
        3 - for CNS
        4 - for LG MQB
        5 - for LG 37W
        6 - for ICAS MEB
    '''
    # reuse this implementation of genVariants.py -> system_variant_info()
    # TODO think about to generate this system number from flag an query a flag here!
    project=int(str(args[0])[:-5])
    return project

def flagIsSet(args,**kwargs):
    \"\"\"
    Test if a flag is set in a list of system variants.

    These function can be used to select the packages which need to be
    build for a update container.

    Parameters
    ----------
    arg1: string
        Comma separated list of System variant strings (e.g.
        '100101,100102,100103')
    arg2: string
        Name of the flag.
    arg3: string
        Value of the flag.

    Returns
    -------
    string
        True or False
    \"\"\"

    try:
       for v in args[0].split(','):
          if variants[int(v)][args[1]] == args[2]:
             return "True"
    except IndexError as e:
        raise ParseError("Index Error: " + str(e) + " Args:" + str(args))
    except KeyError as e:
        raise ParseError("Key Error: " + str(e) + " Args:" + str(args))
    return "False"

# arg's: flag=value
def getMatchingVariantStrings(args, **kwargs):
    \"\"\"
    Get matching varinat strings

    Get a comma seperated list of variant info strings where the flag
    matches some value. This returns a list of all known system varinats.
    The mib3-minfest generatur will filter them out when building the
    release container for a smaller subset of variants.

    These function can be used to add variant informations in a swupdate
    package recipe.

    Parameters
    ----------
    args: string
        Key=Value pair of Flags which should be set in the variant.

    Returns
    -------
    string
        Comma seperated list of variant strings
    \"\"\"

    ret = ''
    for variantid in sorted(variants.keys()):
       variant = variants[variantid]
       try:
         match = True
         for f in args:
            (flag,sep,value) = f.partition("=")
            if sep != '=':
               raise ParseError("Error: malformed check! " + f)
            regex = re.compile(value)
            _value = variant.get(flag,None)
            if _value is None:
               match=False
            else:
               if not regex.match(_value):
                  match=False
         if match and not variant.get('Variant Info String') in ret:
            ret += variant.get('Variant Info String') + ','
       except IndexError as e:
          raise ParseError("Index Error: " + str(e) + " Args:" + str(args))
       except KeyError as e:
          raise ParseError("Key Error: " + str(e) + " Args:" + str(args))
    return ret[:-1]

# get a list of variant Flags for given Systemvariants
# arg: comma seperated list of systemvariant ID's
# arg: Flags
def queryVariantFlags(args, **kwargs):
    \"\"\"
    Query for variant flags

    Get a comma seperated list of variant flags for a comma separated
    list of system variants.

    Parameters
    ----------
    arg1: string
        Comma separated list of system variant ID's.
    args: string
        Variant flag

    Returns
    -------
    string
        comma seperated key=value pair for each variant delimited by semi-colon prefixed by systemvariant
        e.g. queryVariantFlags('100104,100116,100119',SW_HMI_REGION,SW_HMI_BRAND) will return:
        100104:SW_HMI_REGION=eu,SW_HMI_BRAND=vw;100116:SW_HMI_REGION=kr,SW_HMI_BRAND=vw;100119:SW_HMI_REGION=tw,SW_HMI_BRAND=vw
    \"\"\"

    ret = ''
    v = [v for v in args[0].split(',') if v != '']
    for _v in v:
       try:
          variant = variants[int(_v)]
          ret += _v + ':'
          for flag in args[1:]:
             # dictionaries are transfered to bash arrays
             #'HW_MATCH' : {'33': ['9'], '7': ['5', '6', '7', '8']},
             if type(variant[flag]) is dict:
                 ret += flag + '=('
                 for k,v in sorted(variant[flag].items()):
                     ret += '[' + k + ']="'
                     if type(v) is list:
                        ret += ",".join(map(str,v))
                     else:
                        ret += v
                     ret += '" '
                 ret += ')#'
             else:
                ret += flag + '=' + variant[flag] +'#'
          ret = ret[:-1] + ';'
       except IndexError as e:
          raise ParseError("Index Error: " + str(e) + " Args:" + str(args))
       except KeyError as e:
          raise ParseError("Key Error: " + str(e) + " Args:" + str(args))
    return ret[:-1]
""")

       f.write("""manifest = {
    'apiVersion' : "0.2",
    'stringFunctions' : {
        "flagIsSet" : flagIsSet,
        "getBrand" : getBrand,
        "getRegion" : getRegion,
        "getFeature" : getFeature,
        "getUniqueFeatureFromList" : getUniqueFeatureFromList,
        "getVariantInfoString" : getVariantInfoString,
        "getMatchingVariantStrings" : getMatchingVariantStrings,
        "queryVariantFlags" : queryVariantFlags
    }
}""")


if __name__ == '__main__':
    genVariants()
