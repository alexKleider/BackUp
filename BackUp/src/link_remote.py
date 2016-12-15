#!/usr/bin/env python3

# File: link_remote.py

# This is the linking script that expects itself to reside on the
# target host in the target directory.  It checks for the presence
# of a 'params' file in the same directory and if found, uses it to
# over-ride the values of the two parameters it requires:
#    backup_prefix
#    suffix_length

# It is called from the source host using the following command:
# ssh -p22 alex@10.10.10.10 ${target}/link_remote.py

# It sets up and runs the following command on the target host:
# rsync -av --link-dest=${TARGET}/bu.001 ${TARGET}/bu.001/  ${TARGET}/bu.000 

import os
import subprocess

param_filename = 'params'

backup_prefix = 'bu'
suffix_length = 3
# the following are how they are declared in the config file:
#  backup_name = 'bu'
#  suffix_length = 3

def bu_name(prefix, length, n):
    return "{0:}.{2:0>{1:d}d}".format(prefix, int(length), n)

target = os.path.dirname(os.path.abspath(__file__))

# Check if defaults need to be over ridden by a params file:
path2params = os.path.join(target, param_filename)
if os.path.isfile(path2params):
    lines = []
    with open(path2params, 'r') as f:
        for line in f:
            if line:
                line = line.strip()
                lines.append(line)
    n_lines = len(lines)
    if n_lines > 0:
        backup_prefix = lines[0]
    else:
        print(
        "'params' file lacks even one parameter! => FAILURE")
    if n_lines > 1:
        suffix_length = int(lines[1])


#print("SANITY CHECK:")    
#print("  target is {}.".format(target))
#print("  backup_prefix is '{}'.".format(backup_prefix))
#print("  suffix_length is '{}'.".format(suffix_length))
#print("Target directory contains:")
#for item in os.listdir(target):
#    print('\t' + item)

bu1 = os.path.join(target, bu_name(backup_prefix, suffix_length, 1))
bu0 = os.path.join(target, bu_name(backup_prefix, suffix_length, 0))
command_sequence = (
                    "rsync",
                    "-av",
                    "--link-dest={}".format(bu1),
                    "{}/".format(bu1),  # Ensure crucial trailing /.
                    bu0,
                    )

#print("About to run the following command:")
#print(" ".join(command_sequence))
#response = input("Go ahead? ")
#if response and response[0] in 'yY':
#    ret = subprocess.call(command_sequence)
ret = subprocess.call(command_sequence)
if ret:
    print("ERROR: creation of bu.000 using linking failed."

