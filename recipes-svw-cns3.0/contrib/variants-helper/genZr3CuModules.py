#!/usr/bin/env python3
from collections import OrderedDict
from collections import namedtuple
from pprint import pformat

import argparse
import csv
import copy
import json
import os
import re
import sys
import datetime
from pccProject import PccProject

SystemVariantInfo = namedtuple('SystemVariantInfo', 'project boot_mode sop variant')
ContainerInfo = namedtuple('ContainerInfo', 'container_prefix train_prefix train_boot_mode')


Projects=PccProject.InitProjectList()

#
# Container and train information lookup from system variant components.
#
# See system_variant_info for details how the individual numbers are extracted
# from the system variant.
#
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
    # applications using a system information provider with wrong RdW2 region
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


#D141 or 0141
def output_mu_type(entry, args):
    system_variant = entry.get('System Variant')
    info = system_variant_info(system_variant)
    if info.boot_mode == CUSTOMER_BOOT_MODE:
        result = "0"
    else:
        result = "D"

    if info.boot_mode == CUSTOMER_BOOT_MODE and args.customer_mu_type_override:
        result = args.customer_mu_type_override
    elif info.boot_mode == DEVELOPER_BOOT_MODE and args.developer_mu_type_override:
        result = args.developer_mu_type_override

    return result


def read_entries(file_names, file_format):
    entries = []

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
                entries += json.load(data_file)
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

    parser = argparse.ArgumentParser(prog="genZr3CuVariants",
                                     description="Generator for zr3-cu-* yaml entries. The main unit and train software version gets formed after the scheme 'pvvvd' - see description of options below.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--customer-prefix",
                        default='R',
                        help='customer software version prefix (\'p\')for train number, for example \'R\', \'P\', or \'K\'')
    parser.add_argument("--developer-prefix",
                        default='E',
                        help='developer software version prefix (\'p\') for train number, typically \'E\'')
    parser.add_argument("--version",
                        required=True,
                        help="software version (\'vvv\') for use in train number and MU_VERSION")
    parser.add_argument("--delivery",
                        type=int,
                        default=datetime.date.today().isocalendar()[1],
                        help='subsequent software delivery (\'d\', Nachlieferung) for train number')
    parser.add_argument("--buildref",
                        type=int,
                        default=1,
                        help='release-candidate respectively version (\'d\', Buildref / RC)')
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
    # project string
    project_string_by_project = \
    {
            3: "MQB",
            7: "37W",
    }

    # read json file  into a map
    entries = read_entries(args.file, args.format)

    containers = OrderedDict()

    for row in sorted(entries, key=lambda entry: entry.get('System Variant')):
        system_variant = row.get('System Variant')
        cu_variant=row.get('SW_HMI_PROJECT').lower()
        variant_info = system_variant_info(system_variant)
        if variant_info.boot_mode == 1:
            cu_variant+="-sec"

        info = container_info_for_system_variant(system_variant)
        #map_variant = row.get('Map Variant')
        #if row.get('SW_UPDATE_KEY') == 'Customer':
        #    map_variant += '_sec'      
        region=row.get("SW_HMI_REGION")
        platform=row.get("SW_HMI_PROJECT").upper()
        if cu_variant not in containers.keys():
            containers[cu_variant] = OrderedDict()
            # Map Variant -> MU type, if customer boot == "0"
            containers[cu_variant]['MU_TYPE'] = output_mu_type(row, args)
#CNS3_JPCC_MQB_CU_WLAN_E${MAJOR}${DELIVERY}P
            containers[cu_variant]['TRAIN_SUFFIX'] = "CNS3_JPCC" + "_" \
                                                   + row.get('SW_HMI_PROJECT').upper() + "_" \
                                                   + "CU" + "_" \
                                                   + info.train_boot_mode \
                                                   + "${MAJOR}${DELIVERY}" + TRAIN_SUPPLIER_SUFFIX[info.train_prefix]

            containers[cu_variant]['VARIANTS'] = []
            containers[cu_variant]['UPDATE_VARIANTS'] = []

        containers[cu_variant]['VARIANTS'].append(system_variant)
        update_variant_infos = []
        add_update_variant_info(update_variant_infos, row.get('Variant Info String'))
        containers[cu_variant]['UPDATE_VARIANTS'].extend(update_variant_infos)


    with open('zr3-cu-modules.fragment.yaml', 'w') as f:
        # Write info/instructions header for the fragment.
        f.write("   # Variant package fragment generated by genZr3CuVariants.py Do not waste your\n")
        f.write("   # time with editing. Re-generate variant data from and with pure::variants\n")
        f.write("   # JSON export and genZr3CuVariants.py\n")
        f.write("   #\n")
        f.write("   # The lines below are intended to be used as multiPackage elements in\n")
        f.write("   # zr3-cu-*.yaml.\n")

        for k, v in containers.items():
            f.write("   " + k + ":\n")
            f.write("      environment:\n")
            print('   - zr3-cu-' + k)
            #f.write("         MU_VERSION: \"" + v.get('MU_TYPE') + args.version + "\"\n")
            f.write("         MU_VERSION: \"" + v.get('MU_TYPE') + "${MAJOR}" + "\"\n")
            f.write("         TRAIN_NUMBER: \"" + v.get('TRAIN_SUFFIX') + "\"\n")
            f.write("         VARIANTS: \"" + ",".join(sorted(v.get('VARIANTS'))) + "\"\n")
            #f.write("      privateEnvironment:\n")
            f.write("         UPDATE_VARIANTS: \"" + ",".join(sorted(v.get('UPDATE_VARIANTS'))) + "\"\n")
      
            #if "-sec" not in k.lower():
            #    f.write("         DEVELOPMENT_FLAGS: \"true\"\n")
            if "-sec" in k.lower():
                f.write("         SIGNATURE: \"false\"\n")
                f.write("         SECURE_DEVELOPMENT_FLAGS: \"true\"\n")

        #f.write("\nprovideVars:\n")
        #f.write("   TRAIN_PKG_VERSION: ${TRAIN_PKG_VERSION}\n")
        #f.write("   TRAIN_PREFIX: ${TRAIN_PREFIX}\n")
        #f.write("   MU_VERSION: ${MU_VERSION}\n")
        #f.write("   BUILDREF: ${BUILDREF}\n")


if __name__ == '__main__':
    genVariants()
