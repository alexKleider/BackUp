#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :
#
# file: 'backup.py'
# Part of ___, ____.

# Copyright 2016 Alex Kleider
# See COPYING.txt distributed with this file.
"""
backup.py: main module of BackUp
"""

import os
import sys
import getpass
import configparser

CONFIG_FILE = 'BackUp/config'  # The default configuration file.
RIPPLER = 'rippple.py'

def show_args(args, name = 'Arguments'):
    """                     [../tests/test1.py: global_show_args]
    A helper function for testing.
    Returns a string displaying args, which can be any iteration
    supporting collection including dictionary like objects (ones
    that implement an items() method.)
    """
    def show_l():
        return('  {}'.format(arg))
    def show():
        return('  {}: {}'.format(arg, args[arg]))
    dictionary = True
    try:
        args.items()  # See if it quacks like a dictionary.
    except AttributeError:
        show = show_l
        dictionary = False
    ret = ["{} are ...".format(name)]
    data = []
    for arg in args:
        data.append(show())
    if dictionary:
        data.sort()
    ret.extend(data)
    ret.append('  ... end of report.\n')
    return '\n'.join(ret)

def get_config_file_name():
    """
    Place holder for a function to check for config file in various
    locations: cwd, ~/.ripple.conf, /usr/local/etc/ripple.conf in that
    order unless specified by a parameter to the command line
    -f, --file CONFIGURATION_FILE option.
    """
    return CONFIG_FILE

def get_section_specifics(section=None):
    """
    Get the required data from the config file.
    Relies on get_config_file_name().
    Sets 'max_number_of_snapshots' based on 'suffix_length' 
    """
    config = configparser.ConfigParser()
    config_file_name = get_config_file_name()
#   print(" about to call config.read() with {} as parameter."
#               .format(config_file_name))
    config.read(config_file_name)
    ret = {}
    if section:
#       print("""<get_section_specifics() being called
#       with parameter '{}'.""".format(section))
        if section:
            if (section == "DEFAULT"
            or section in config.sections()):
                section_dict =  config[section]
            else:  # No such section in file!!
                print("""There is no such section in the file!!""")
                sys.exit(1)
        else:
            print("""<get_section_specifics(section=None) does
            not as yet support absence of a <section> parameter.""")
            sys.exit(1)
#       print("""It has the following key/value pairs:""")
        for key in section_dict:
#           print("{}: {}".format(key, section_dict[key]))
            ret[key] = section_dict[key]
        ret['max_number_of_snapshots'] = int(
                '9' * int(ret['suffix_length']))
        if not ret['user']:
            ret['user'] = getpass.getuser()
        return ret

def get_commands(section_specifics):
    """
    Takes the output of get_section_specifics() (a dict)
    and returns a dict of the 3 required commands:
    1. Run rsync on the client machine:
        $ rsync -az --delete -e "ssh -p<port> <user>" \
            --exclude-from=<exclude_file> \
            <source> \
            <host>:<destination_dir>/bu.000
    ## --exclude-from=FILE     read exclude patterns from FILE
    2. Run the local ripple.py script (with command line
    parameters) remotely (on the backup host:)
        $ ssh -p<port> <user>@<destination_host> python3 -u - \
         <destination_dir> <backup_name> <suffix_length> < <rippler>
    3. Create the hard link copy using rsync:
        $ ssh -p<port> <destination_host> 'bash -s' -- < rsync \
            -a --link-dest=../bu.001 \
            <destination_dir>/bu.001/ <destination_dir>/bu.000
    """
    ret = dict()

    # 1  Run rsync:
    sp = section_specifics
    rsync_ssh = ' -e "ssh -p{} {}"'.format(sp.port, sp.user)
    rsync_exclude = ' --exclude-from={}'.format(sp.exclude_file)
    rsync_dest = ' {}:{}'.format(sp.destination_host,
                                    sp.destination_dir)
    ret["rsync"] = "rsync -az --delete{}{}{}{}{}".format(
                rsync_ssh, rsync_exclude, sp.source, rsync_dest)

    # 2  Run the local ripple script on the remote host:
    ret["ripple"] = ('ssh -p{} {}@{} python3 -u - {} {} {} < {}'
                # Command line parameters:         ^  ^  ^    ^
                #    target------------------------'  |  |    |
                #    backup_name----------------------'  |    |
                #    suffix_length-----------------------'    |
                # Script to execute (on remote host)----------'
                .format(sp.port, sp.user, sp.destination_host,
                        target, sp.backup_name, sp.suffix_length,
                        sp.rippler))

    # 3  Run local rsync remotely to create the hard link copy:
    link_dest = '../bu.001' 
    target_bu1 = 'Target/bu.001/' 
    target_bu2 = 'Target/bu.000'
    ret["link"] = (
    "ssh -p{} {}@{} 'bash -s' -- < rsync -a --link-dest={} {} {}"
                .format(port, user, destination_host,
                        target, backup_name, suffix_length))

    return ret

def main():
    print("Running 'backup.main()'.......")


if __name__ == '__main__':  # code block to run the application
    main()

