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

SystemVariantInfo = namedtuple('SystemVariantInfo', 'project boot_mode sop variant')
ContainerInfo = namedtuple('ContainerInfo', 'train_boot_mode')

#
# Container and train information lookup from system variant components.
#
# See system_variant_info for details how the individual numbers are extracted
# from the system variant.
#

MU_TYPE_MAPPING = \
    {
        'DACHCZ': 'X',
        'EU1': 'X',
        'EU2': 'X',
        'JP': 'J',
        'KR': 'K',
        'RDW1': 'R',
        'RDW2': 'R',
        'RDW2_INDIEN': 'R',
        'CHN': 'C',
        'TW': 'T'
    }

TRAIN_SUPPLIER_SUFFIX = 'P'

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
        train_boot_mode=train_boot_mode_by_boot_mode[info.boot_mode])
    return result


def output_mu_type(entry, args):
    system_variant = entry.get('System Variant')
    info = system_variant_info(system_variant)
    if info.boot_mode == CUSTOMER_BOOT_MODE:
        result = "0"
    else:
        result = MU_TYPE_MAPPING[entry.get('Map Variant')]

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


def genNavimaps():
    global train_boot_mode_by_boot_mode

    parser = argparse.ArgumentParser(prog="genNavimaps",
                                     description="Generator for zr3-navimap yaml entries. The main unit and train software version gets formed after the scheme 'pvvvd' - see description of options below.",
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

    entries = read_entries(args.file, args.format)

    containers = OrderedDict()
    for row in sorted(entries, key=lambda entry: entry.get('Map Variant')):
        system_variant = row.get('System Variant')
        map_variant = row.get('Map Variant')

        info = container_info_for_system_variant(system_variant)

        if map_variant not in containers.keys():
            containers[map_variant] = OrderedDict()

            # DEFECT-29991
            containers[map_variant]['MR_TRAIN_SUFFIX'] = "M_" + "${MAP_MAJOR}" + "_" + "${MAP_DELIVERY}" + "_" + \
                                          "${MAP_BUILDREF}" + "_" + TRAIN_SUPPLIER_SUFFIX

            containers[map_variant]['MAP_VARIANT'] = row.get('Map Variant')


    #special container DACHCZ
    containers['DACHCZ'] = copy.deepcopy(containers['EU1'])
    containers['DACHCZ']['MAP_VARIANT'] = 'DACHCZ'


    with open('zr3-navimap-multirelease.fragment.yaml', 'w') as f:
        # Write info/instructions header for the fragment.
        f.write("   # Variant package fragment generated by genNavimapsMultirelease.py. Do not waste your\n")
        f.write("   # time with editing. Re-generate variant data from and with pure::variants\n")
        f.write("   # JSON export and genNavimapsMultirelease.py.\n")
        f.write("   #\n")
        f.write("   # The lines below are intended to be used as multiPackage elements in\n")
        f.write("   # zr3-navimap-multirelease.yaml.\n")

        for k, v in containers.items():
            f.write("   " + k + ":\n")
            print('   - zr3-navimap-multirelease-' + k)
            f.write("      depends:\n")
            f.write("         - name: zr3-navimap-" + k + "\n")
            f.write("           use: [result, environment]\n")
            f.write("         - name: zr3-navimap-" + k + "_sec\n")
            f.write("      environment:\n")
            f.write("         MAP_REGION: \"" + k + "\"\n")
            f.write("         MR_TRAIN_SUFFIX: \"" + v.get('MR_TRAIN_SUFFIX') + "\"\n")


if __name__ == '__main__':
    genNavimaps()
