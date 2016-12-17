#!/usr/bin/env python3

# File: run_remotely.py

"""
A python module which provides <send> and <run> functions:
The first parameter of each is a list of files expected to
be in the same directory as is run_remotely.py.

<send> sends copies of its file(s) to the target directory
on the specified host. It does this by running
scp -P${port} ${full_path2file} ${user}@${host}:${target}
for each file.

<run> runs one or more commands on the specified target host.
We expect its first parameter to be a list of files of which only
those ending in '.py' are considered.  They are expected to be
found within the 'target' directory on the specified host.
ssh -p${port} ${user}@${host} ${target}/${script}
is run for each qualifying file. 

This module can be called directly as follows:
Usage:
  run_remotely.py [files [target [host [user [port]]]]]

<files> is a sequence.
All files will be provided first to <send> and then to <run>.

Defaults are hard coded for any missing parameters.
"""

import os
import sys
import subprocess

def get_dir():
    """
    A one liner only used for experimentation.
    Not used except to provide importation.
    """
    return os.path.dirname(os.path.abspath(__file__))


def send(files, target, host=None, user=None, port=None):
    """
    Uses scp to send <files> (a list of file names) to the target
    directory on the foreign host.  The files are expected to be
    within the same directory as this module.
    """
    path2files = os.path.dirname(os.path.abspath(__file__))
    if host==None: host = '127.0.0.1'
    if port==None: port = '22'
    if user:
        host = "{}@{}".format(user, host)
    # scp -P${port} ${full_path2file} ${user}@${host}:${target}
    for f in files:
        cmd_args = (
            "scp",
            "-P{}".format(port),
            os.path.join(path2files, f),
            "{}:{}".format(host, target)
            )
        ret = subprocess.call(cmd_args)
        if ret:
            print("ERROR: scp '{}' failed.".format(f))
            print("\tError code {} was returned.".format(ret))

def run(scripts, target, host=None, user=None, port=None):
    """
    <scripts> is expected to be an iterable of file names.
    Any of the file names that end in '.py' are run
    in the target directory on remote host.
    <port> defaults to 22 and unless specified otherwise,
    user is current user.
    """
    path2files = os.path.dirname(os.path.abspath(__file__))
    executables = [
        script for script in scripts if script.endswith(".py")]
    if host==None: host = '127.0.0.1'
    if port==None: port = '22'
    if user:
        host = "{}@{}".format(user, host)
    # ssh -p${port} ${user}@${host} ${target}/${script}
    for script in executables:
        path2script = os.path.join(target, script)
        cmd_args = (
            "ssh",
            "-p{}".format(port),
            host,
            path2script,
                )
        command = " ".join(cmd_args)
        ### Following 4 lines...
        ret = subprocess.call(command, shell=True)
        if ret:
            print("ERROR: Call to '{}' failed.".format(script))
            print("\tError code {} was returned.".format(ret))
        ### OR next 8 lines...
#       print("About to run the following command:")
#       print(command)
#       response = input("OK to proceed? ")
#       if response and response[:1] in 'yY':
#           ret = subprocess.call(command, shell=True)
#           if ret:
#               print("ERROR: Call to '{}' failed.".format(script))
#               print("\tError code {} was returned.".format(ret))

def string2list(csv, delimeter=','):
    return csv.split(delimeter)

if __name__ == "__main__":
    # Create a 'params' file.
    directory = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(directory, 'params'), 'w') as f:
        f.write("bu\n3")
    # Set defaults:
    files_py = ("trivial.py",)
    #files_py = ("link_remotely.py", "rip_remotely.py",)
    files_txt = ('params',)
    files = files_py + files_txt
    target = "/home/alex/BU"
    host = "10.10.10.10"
    user = os.getlogin()
    port = 22
    args = sys.argv[1:]
    n_args = len(args)
    if n_args > 0: files = string2list(args[0])
    if n_args > 1: target = args[1]
    if n_args > 2: host = args[2]
    if n_args > 3: user = args[3]
    if n_args > 4: port = args[4]
    send(files, target, host, user, port)
    run(files, target, host, user, port)

