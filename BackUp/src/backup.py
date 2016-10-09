#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :
#
# file: 'backup.py'
# Part of ___, ____.

# Copyright 2016 Alex Kleider
# See COPYING.txt distributed with this file.
"""
Put your docstring here.
"""

import os
import sys
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
        return ret

def get_commands(section_specifics):
    """
    Takes the output of get_section_specifics()
    and returns a dict of 5 commands.
        rsync: to do the backup using rsync-
            "rsync -a{} --delete {} {} {} {} ".format(
                    compression_option,
                        rsync_port, exclude,
                        section_specifics["source"],
                        dest),
        scp_conf: to move config data to destination.
        scp_script: to run local rippling script on the
            destination host:
            ssh root@MachineB 'bash -s' < local_script.sh
        chmod: NOT NEEDED because we will run local script
            on destination machine rather than send the script to the
            destination machine and run it there.
        ripple= rip_cmd,

Implementation on foreign host:
    1. Run rsync on the client machine:
        $ rsync -az --delete -e "ssh -p5322 alex" \
            --exclude-from=rip_exclude \
            source \
            indi303.net:/mnt/BU/Sandbox/bu.000
    ## --exclude-from=FILE     read exclude patterns from FILE
    2. Run ripple.py (with cl parameters) remotely (on backup host.)
        $ ssh -p5322 alex@indi303.net python3 -u - \
                                     target bu 3 < ripple.py
    3. Create the hard link copy using rsync:
        $ ssh -p5322 indi303.net 'bash -s' -- < rsync \
            -a --link-dest=../bu.001 Target/bu.001/ Target/bu.000
    """
    colon = ''
    compression_option = ""
    host = section_specifics["destination_host"]
    port = section_specifics["destination_port"]
    dest_dir = section_specifics["destination_dir"]
    if  section_specifics["destination_user"]:
        user_option = "-oUser={}".format(
                section_specifics['destination_user'])
    else:
        user_option = ''
    if dest_dir[-1] != '/':
        dest_dir = dest_dir + '/'
    if (not host) or (host  == "localhost"):
        host = ""
        port = ""
    else:
        colon = ':'
        compression_option = "z"
    if port:
        rsync_port = '-e "ssh -p{} {}"'.format(port, user_option)
        ssh_port = '-oPort={} {}'.format(port, user_option)
    else:
        rsync_port = ''
        ssh_port = ''
    outf = '{}{}.{}'.format(dest_dir,
                section_specifics["backup_name"],
                '0' * int(section_specifics["suffix_length"]))
    dest = '{}{}{}'.format(host, colon, outf)


    if section_specifics["exclude_file"]:
        if os.path.isfile(section_specifics["exclude_file"]):
            exclude = ('--exclude-from={}'
                .format(section_specifics["exclude_file"]))
        else:
            exclude = ''
            aklib.optional_info(globals.debug,
                    "Specified exclude file doesn't exist.")
    else:
        exclude = ''


    rsync_cmd = "rsync -a{} --delete {} {} {} {}".format(
            compression_option, rsync_port,
            exclude, section_specifics["source"],
            dest)


    if host:  # Back up is to a remote host.
        # Arrange rippling cmd to be on remote host
        # and make sure rippling cmd is executable.
        Remote_Rippling_Script = os.path.join(
                section_specifics["destination_tmp_dir"], RIPPLER)
        dest = '{}{}{}'.format(host, colon,
                                Remote_Rippling_Script)
        scp_script_cmd  = 'scp -p {} {} {}'.format(ssh_port,
                                        RIPPLER, dest)
        chmod_cmd = 'ssh {} {} chmod 755 {}'.format(ssh_port,
                                    host, Remote_Rippling_Script)
        rip_cmd = 'ssh {} {} {}'.format(ssh_port, host,
                                        Remote_Rippling_Script)
    else:
        scp_conf_cmd = ''
        scp_script_cmd = ''
        chmod_cmd = ''
        rip_cmd = RIPPLER

    return dict(
        rsync= "rsync -a{} --delete {} {} {} {} ".format(
                    compression_option,
                        rsync_port, exclude,
                        section_specifics["source"],
                        dest),
        scp_conf= scp_conf_cmd,
        scp_script= scp_script_cmd,
        chmod= chmod_cmd,
        ripple= rip_cmd,
            )

def main():
    print("Running 'backup.main()'.......")


if __name__ == '__main__':  # code block to run the application
    main()

