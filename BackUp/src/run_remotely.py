#!/usr/bin/env python3

# File: run_remotely.py

# A python module which provides run_remotely,
# a function used to run a command on a target host.

# We expect the command to be a script defined by 'script' which
# is to be found under the 'target' directory on the remote
# host.

# Short version: it runs the following:
# ssh -p${port} ${user}@${host} ${target}/${script}

"""
A module that provides run_remotely:
a function used to run a script residing on a target host.

It can be called directly as follows:
Usage:
  run_remotely.py [script [target [host [user [port]]]]]

Defaults are hard coded for any missing parameters.
"""

import os
import sys
import subprocess

def run(script, target, host=None, user=None, port=None):
    """
    Runs script in the target directory on remote host.
    port defaults to 22 and unless specified otherwise,
    user is current user.
    """
    if host==None: host = '127.0.0.1'
    if port==None: port = '22'
    if user:
        host = "{}@{}".format(user, host)
    path2script = os.path.join(target, script)
    cmd_args = (
        "ssh",
        "-p{}".format(port),
        host,
        path2script,
            )
    command = " ".join(cmd_args)
#   print("About to run the following command:")
#   print(command)
#   response = input("OK to proceed? ")
#   if response and response[:1] in 'yY':
#       ret = subprocess.call(command, shell=True)
#       print("The command returned a code of {}.".format(ret))
#   return ret
    return subprocess.call(command, shell=True)

if __name__ == "__main__":
    # Set defaults:
    script = "trivial.py"
    target = "/home/alex/BU"
    host = "10.10.10.10"
    user = os.getlogin()
    port = 22
    args = sys.argv[1:]
    n_args = len(args)
    if n_args > 0: script = args[0]
    if n_args > 1: target = args[1]
    if n_args > 2: host = args[2]
    if n_args > 3: user = args[3]
    if n_args > 4: port = args[4]
    ret = run(script, target, host, user, port)

