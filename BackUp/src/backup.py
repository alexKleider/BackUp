#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :
#
# File: 'backup.py'
# Part of ___, ____.

# Copyright 2016 Alex Kleider
# See COPYING.txt distributed with this file.
"""
backup.py: main module of BackUp
"""

import os
import sys
import configparser
#import shlex
import subprocess

CONFIG_FILE = 'BackUp/config'  # The default configuration file.
# RIPPLER = 'rippple.py'
RIPPLER = 'rip_remote.py'
LINKER = 'link_remote.py'
REMOTELY = 'run_remotely.py'

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
    locations: BackUp/config, ~/.ripple.conf, /usr/local/etc/ripple.conf in that
    order unless specified by a parameter to the command line
    -f, --file CONFIGURATION_FILE option.
    Have yet to implement docopt module.
    """
    return CONFIG_FILE

def get_suffix(number, length):
    """
    If able, returns a <length> long string representing <number>
    padded with leading zeros if needed. Otherwise (number is
    negative or won't fit) returns None.
    """
    len_ = int(length)
    num_ = int(number)
    if (len_ < 1
    or num_ < 0
    or num_ > int("9"*len_)):
        return None
    format_string = "{{:0>{}d}}".format(len_)
    return format_string.format(num_)

def get_section_specifics(section=None):
    """
    Returns a dict of required data based on the config file.
    Relies on get_config_file_name().

    As of Thu Dec 15 22:50:10 PST 2016
    Arguments are ...
      backup_name: bu
      bu0: bu.000
      bu1: bu.001
      bu2: bu.002
      comment: for testing: bu on remote host 10.10.10.10.
      exclude_file: /home/alex/Py/BackUp/BackUp/tests/data/rip_exclude
      host: 10.10.10.10
      max_number_of_snapshots: 999  # Based on 'suffix_length' 
      ordered_commands: ['rsync', 'ripple', 'link']
      port: 22
      rippler: /home/alex/Py/BackUp/BackUp/src/ripple.py
      source: /home/alex/Py/BackUp/BackUp/tests/data/source/
      suffix_length: 3
      target: /home/alex/BU
      to_expand: source target exclude_file rippler
      user: alex  # If not provided, set by os.getlogin()
      ... end of report.

    Not yet implemented is query for a <section> if not provided.
    """
    config = configparser.ConfigParser()
    config_file_name = get_config_file_name()
#   print(" about to call config.read() with {} as parameter."
#               .format(config_file_name))
    config.read(config_file_name)
    ret = {}
    if section is None:
        # Yet to be implemented: query user for a section.
        print("<get_section_specifics(section=None)> does not")
        print("as yet support absence of a <section> parameter.")
        sys.exit(1)
    elif (section == "DEFAULT") or (section in config.sections()):
        section_dict =  config[section]
#       print("Calling <get_section_specifics({})>."
#                                   .format(section))
#       print("""It has the following key/value pairs:""")
        ret = {key:section_dict[key] for key in section_dict}
#       for key in section_dict:
#           print("{}: {}".format(key, section_dict[key]))
#           ret[key] = section_dict[key]
        ret['max_number_of_snapshots'] = int(
                '9' * int(ret['suffix_length']))
        if not ret['user']:
            ret['user'] = os.getlogin()
        ret['bu0'] = "{}.{}".format(ret["backup_name"],
                            get_suffix(0, ret['suffix_length']))
        ret['bu1'] = "{}.{}".format(ret["backup_name"],
                            get_suffix(1, ret['suffix_length']))
        ret['bu2'] = "{}.{}".format(ret["backup_name"],
                            get_suffix(2, ret['suffix_length']))
        path_names = ret["to_expand"].split()
        for path in path_names:
            ret[path] = os.path.abspath(ret[path])
        # The above line strips trailing slash which mustn't be lost
        # for the source file if there.
        if section_dict[path_names[0]][-1] == '/':
            ret[path_names[0]] = ''.join((ret[path_names[0]],'/'))
        ret["ordered_commands"] = ret["ordered_commands"].split()
        return ret
    else:  # No such section in file!!
        print("""There is no such section in the file!!""")
        sys.exit(1)

def get_commands(section_specifics):
    """
    Takes the output of get_section_specifics() (a dict)
    and returns a dict of the 3 required commands:
    1. Run rsync on the client machine:
        $ rsync -az --delete -e "ssh -p<port> <user>" \
            --exclude-from=<exclude_file> \
            <source> \
            <host>:<target>/bu.000
    ## --exclude-from=FILE     read exclude patterns from FILE
    2. Send the foreign script and its params to target host.
    3. Run the foreign script on the target host:
        to do the rippling and linking.
    I've failed in my attempts to acheive the following:
    2. Run the local ripple.py script (with command line
    parameters) remotely (on the backup host:)
        $ ssh -p<port> <user>@<host> python3 -u - \
         <target> <backup_name> <suffix_length> < <rippler>
    3. Create the hard link copy using rsync:
        $ ssh -p<port> <host> 'bash -s' -- < rsync \
            -a --link-dest=../bu.001 \
            <target>/bu.001/ <target>/bu.000
    """
    check("$ within get_commands: CWD is {}.\n".format(os.getcwd()))
    ret = dict()

    # 0  Be sure a bu1 directory exists in the target hierarchy.
    ret["prn"] = ' '.join([
    # Assign env vars:
    "bu1={}".format(sp["bu1"]),
    "&&",
    "&&",
    "if [ ! -d $bu1 ] then mkdir $bu1 fi",
    "prn.sh",
    "${}".format("bu1"),
    "-av",
    "--link-dest=$PWD/prior_dir host:src_dir/new_dir/",
    ])

    # 1  Run rsync:
    sp = section_specifics
    rsync_ssh = ' -e "ssh -p{}"'.format(sp["port"])
    rsync_exclude = ' --exclude-from={}'.format(sp["exclude_file"])
    rsync_dest = ' {}@{}:{}/{}'.format(sp["user"],
                                    sp["host"],
                                    sp["target"],
                                    sp["bu0"])
    ret["rsync"] = "rsync -az --delete{}{} {}{}".format(
                rsync_ssh,  #---------^ ^  ^ ^
                rsync_exclude,  #-------'  | |
                sp["source"],  #-----------' |
                rsync_dest,  #---------------'
                )

    # 2  Run local ripple script on remote host with parameters:
    ret["ripple"] = ('ssh -p{} {}@{} python3 -u - {} {} {} < {}'
                # Command line parameters:         ^  ^  ^    ^
                #    target------------------------'  |  |    |
                #    backup_name----------------------'  |    |
                #    suffix_length-----------------------'    |
                # Script to execute (on remote host)----------'
                .format(sp["port"], sp["user"], sp["host"],
            sp["target"], sp["backup_name"], sp["suffix_length"],
                    sp["rippler"]))

    # 3  Run local rsync remotely (with parameters)
    #    to create the hard link copy:
    link_dest_file = os.path.join(sp["target"], sp["bu1"])
    link_dest = "--link-dest={}".format(link_dest_file)
    src = sp["source"]
    dest = os.path.join(sp["target"], sp["bu0"])
    print("""=============================
    Four parameters:
{}
{}
{}
{}
---------
""".format(link_dest_file, link_dest, src, dest))
    """
rsync: link_stat "/home/bu.001" failed: No such file or directory (2)
rsync: change_dir "/home/alex//Target/bu.001" failed: No such file or
directory (2)
rsync: change_dir#3 "/home/alex//Target" failed: No such file or
directory (2)
"""
    ret["link"] = ' '.join([
    "cd {}".format(sp["target"]),
    "&&",
    "link_dest={}".format(link_dest),
    "&&",
    "src={}".format(src),
    "&&",
    "dest={}".format(dest),
    "&&",
    "ssh -p{} {}@{}".format(sp["port"], sp["user"], sp["host"]),
    '"rsync -avz $link_dest $src $dest"',
    ])
    return ret

### Tests follow ###

sections = [
    "test_local",
    "test_remote_pi",
    "test_remote_indi",
    ]

def clear_testing_targets(sections=sections):
    for n in range(len(sections)):
        sp = get_section_specifics(sections[n])
        command = (
#   "ssh -p{} {}@{} 'bash -s' -- < rm -rf {}"
    "ssh -p{} {}@{} 'rm -rf {}/*'"
        .format(sp["port"], sp["user"], sp["host"], sp["target"]))
        print(command)
#       ret = subprocess.call(shlex.split(command))
        ret = subprocess.call(command, shell=True)
        if ret:
            print("  !! Above command returned '{}'!!".format(ret))
        else:
            print("  Above command returned successfully.")

def main():
    print("Running 'BackUp.BackUp.src.backup.main()' tests .....")
    clear_testing_targets()
    for n in range(len(sections)):
#       print("### currently for '{}' ###".format(sections[n]))
        config = get_section_specifics(sections[n])
        commands = get_commands(config)
        print(show_args(config))
        print(show_args(commands, "Commands:"))
        for command in config['ordered_commands']:
            response = input(
            "? Execute next command:\n{}\n Enter 'y' to proceed.. ".
                    format(commands[command]))
            if response and response[0] in 'yY':
#               print("calling command as follows:")
#               print(shlex.split(commands[command]))
#               ret = subprocess.call(shlex.split(commands[command]))
                ret = subprocess.call(commands[command], shell=True)
                print("Return code: {}.".format(ret))
                if ret:
                    print("Command failed!!")
                check("Pause to examine results.")
            else:
                print("Moving on without execution...")

if __name__ == '__main__':  # code block to run the application
    cwd = os.getcwd()
    if not (cwd in sys.path):
        sys.path.insert(0, cwd)
    from BackUp.tests.test1 import check
    main()

