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

Usage:
backup.py -h|--help
backup.py --version
backup.py [-d|--debug] [--config=CONFIG] [--section=SECTION]

Options:
-h --help  Show this screen.
--version  Show version.
-d --debug  Run in debugging mode: confirm all subprocess calls.
-c CONFIG --config=CONFIG  Specify configuration file to use.
                        If not specified, a default is provided.
                            [default: BackUp/config]
-s SECTION --section=SECTION  Which section to use for parameters.
                            If not provided, user will be queried 
                            although this is not yet implemented
                            so for now you should specify a section.
"""

import os
import sys
import configparser
#import shlex
import subprocess
from docopt import docopt

# We have two sets of globals:
#    opts: from command line via docopt,  and
#    args: from a configuration file.

opts = docopt(__doc__, version="backu.py 0.0.0")

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

#print(show_args(opts, 'Options'))
#sys.exit()

def get_config_file_name(opts):
    """
    Place holder for a function to check for config file in various
    locations: BackUp/config, ~/.ripple.conf, /usr/local/etc/ripple.conf in that
    order unless specified by a parameter to the command line
    -c CONFIG --config=CONFIG  Specify configuration file to use.
    For now, default supplied by docopt (see docstring __doc__.)
    """
    return opts["--config"]

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

def get_section_specifics(section=None, opts=opts):
    """
    Returns a dict of required data based on the config
    and command line options file.
    Relies on get_config_file_name().

    As of Thu Dec 15 22:50:10 PST 2016
    Dictionary returned is ...
      backup_prefix: bu
      bu0: bu.000
      comment: for testing: bu on remote host 10.10.10.10.
      debug: 0
      exclude_file: /home/alex/Py/BackUp/BackUp/tests/data/rip_exclude
      host: 10.10.10.10
      max_number_of_snapshots: 999  # Based on 'suffix_length' 
      params_file: params
      port: 22
      remote_script: /home/alex/Py/BackUp/BackUp/src/remotely.py
      source: /home/alex/Py/BackUp/BackUp/tests/data/source/
      suffix_length: 3
      target: /home/alex/BU
      to_expand: source target exclude_file
      user: alex  # If not provided, set by os.getlogin()
      ... end of report.

    Not yet implemented is query for a <section> if not provided.
    """
    config = configparser.ConfigParser()
    config_file_name = get_config_file_name(opts)
#   print(" about to call config.read() with {} as parameter."
#               .format(config_file_name))
    config.read(config_file_name)
    if section is None:
        # Yet to be implemented: query user for a section.
        print("<get_section_specifics(section=None)> does not")
        print("as yet support absence of a <section> parameter.")
        sys.exit(1)
    elif (section == "DEFAULT") or (section in config.sections()):
        section_dict =  config[section]
        ret = {key:section_dict[key] for key in section_dict}
        ret['max_number_of_snapshots'] = int(
                '9' * int(ret['suffix_length']))
        # Backup_zero defined here to facilitate testing:
        ret["bu0"] = "{0:}.{2:0>{1:d}d}".format(
                                    ret["backup_prefix"],
                                    int(ret["suffix_length"]),
                                    0)
        if opts["--debug"] == 'True':
            ret["debug"] = True
        else:
            ret["debug"] = False
        if not ret['user']:
            ret['user'] = os.getlogin()
        if not ret['port']: ret['port'] = '22'
        if not ret['host']: ret['host'] = '127.0.0.1'
        path_names = ret["to_expand"].split()
        for path in path_names:
            ret[path] = (
                os.path.abspath(os.path.expanduser(ret[path])))
        # The above line strips trailing slash which in the case
        # of the source file must not be lost:
        if section_dict["source"][-1] == '/':
            ret["source"] = ''.join((ret["source"],'/'))
        return ret
    else:  # No such section in file!!
        print("""There is no such section in the file!!""")
        sys.exit(1)

def verify_cmd(cmd,
                debug_flag=True,
#               debug_flag=opts["--debug"],
                shell=False):
    """
    If debug_flag is True, user is shown the command and
    asked for verification before the command is run.
    cmd can be a string or a sequence of strings.
    """
    if debug_flag:
        print("About to run the following command:")
        print(cmd)
        response = input("OK to proceed? ")
        if response and response[:1] in 'yY':
            ret = subprocess.call(cmd, shell=shell)
        else:
            print("User chose to abort.")
            sys.exit()
    else:
        ret = subprocess.call(cmd, shell=shell)
    return ret

def rsync(args):
    """
    Use get_section_specifics() as its paramter.
    Sets up and executes the following command:
    $ rsync -az --delete -e "ssh -p<port>" \
        --exclude-from=<exclude_file> \
        <source> \
         <user>@<host>:<target>/bu.000
    $ rsync -avz --delete /home/alex/Py/BackUp/Sandbox/Source/ \
                        alex@10.10.10.10:/home/alex/BU/bu.000
    """
    exclude_file = args["exclude_file"]

    if exclude_file and os.path.isfile(exclude_file):
        exclude_file_arg = ("--exclude-from={}"
                                .format(exclude_file))
    else:
        exclude_file_arg = ''
    destination = os.path.join(args["target"], 
                            args["bu0"])
    cmd = (
        "rsync",
        "-avz",
        "--delete",
        exclude_file_arg,
        '-e "ssh -p{}"'.format(args["port"]),
        "{}".format(args["source"]),
        "{}@{}:{}".format(args["user"], args["host"], destination),
        )
    ret = verify_cmd(" ".join(cmd), args["debug"], shell=True)
    if ret:
        print("ERROR: backup failed with error code '{}'."
                        .format(ret))
        sys.exit(ret)

def create_and_send_params_file(args):
    """
    Create the params_file and send it over to the target.
    It is created in /tmp.
    """
    # Create:
    content = "{}\n{}".format(args["backup_prefix"],
                                args["suffix_length"])
    file_name = args["params_file"]
    full_path = os.path.join('/tmp', file_name)  
    with open(full_path, 'w') as f:
        f.write(content)
    # Send:
    host = args["host"]
    if args["user"]:
        host = "{}@{}".format(args["user"], host)
    # scp -P${port} ${full_path2file} ${user}@${host}:${target}
    cmd_args = (
        "scp",
        "-P{}".format(args["port"]),
        full_path,
        "{}:{}".format(host, args["target"])
        )
    ret = verify_cmd(cmd_args)
    if ret:
        print("ERROR: scp '{}' failed.".format(args["params_file"]))
        print("\tError code {} was returned.".format(ret))
    else:
        os.remove(full_path)

def send_and_run(args):
    """
    Uses scp to send the remote_script file to the target and then
    uses ssh to run it on the target host.
    """
    # Expect the remote script to be in same directory as this code:
    containing_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(containing_dir, args["remote_script"])
    host = args["host"]
    if args["user"]:
        host = "{}@{}".format(args["user"], host)
    # scp -P${port} ${full_path2file} ${user}@${host}:${target}
    cmd_args = (
        "scp",
        "-P{}".format(args["port"]),
        full_path,
        "{}:{}".format(host, args["target"])
        )
    ret = verify_cmd(cmd_args)
    if ret:
        print("ERROR: scp '{}' failed.".format(full_path))
        print("\tError code {} was returned.".format(ret))
    else:
        full_path2script = os.path.join(args["target"],
                                        args["remote_script"])
        cmd_args = (
                    "ssh",
                    "-p{}".format(args["port"]),
                    host,
                    full_path2script,
                    )
        ret = verify_cmd(cmd_args)
        if ret:
            print("ERROR: script '{}' failed to run on target host."
                                                .format(full_path))
            print("\tError code {} was returned.".format(ret))

def backup(args):
    rsync(args)
    create_and_sent_params_file(args)
    send_and_run(args)


### Tests follow ###

sections = (
    "test_local",
    "test_remote_pi",
#   "test_remote_indi",
    )

def clear_testing_targets(sections=sections):
    for n in range(len(sections)):
        sp = get_section_specifics(sections[n])
        command = ("ssh -p{} {}@{} 'rm -rf {}/*'".format(
                sp["port"], sp["user"], sp["host"], sp["target"]))
        ret = verify_cmd(command, shell=True)
        if ret:
            print("  !! Above command returned '{}'!!".format(ret))
        else:
            print("  Above command returned successfully.")

if __name__ == '__main__':  # code block to run the application
    cwd = os.getcwd()
    if not (cwd in sys.path):
        sys.path.insert(0, cwd)
    from BackUp.tests.test1 import check

