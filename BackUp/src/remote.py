#!/usr/bin/env python3

# File: remote.py

"""
This script expects itself to reside on the target host in
the target directory.  It takes the place of the two scripts
initially used: rip.remote.py and link_remote.py

It is called from the source host using run_remotely.py which
sets up and issues the following command:
ssh -p22 alex@10.10.10.10 ${target}/remote.py
See run_remotely.__doc__

remote.py checks for the presence of a 'params' file in the its
own directory and if found uses it to over-ride the values of
the two parameters it requires:
    buckup_prefix
    suffix_length

Its purpose is to perform two functions within the target file
hierarchy on the backup host:

1. 'ripple':   (formerly done by rip_remote.py)
Take files of the form ${bu}.${n} and rename each to ${bu}.${n+1}

2. 'link':   (formerly done by link_remote.py)
Create a bu.000 directory- a hard linked copy of bu.000
It sets up and runs the following command on its own (target) host:
rsync -av --link-dest=${TARGET}/bu.001 ${TARGET}/bu.001/  ${TARGET}/bu.000 
"""

import os
import shutil
import subprocess

param_filename = 'params'

backup_prefix = 'bu'
suffix_length = 3

# We expect our target directory to be
# the one containing this script:
target = os.path.dirname(os.path.abspath(__file__))

def bu_name(prefix, suffix_length, n):
    """
    Returns the directory name of backup #n.
    """
    return "{0:}.{2:0>{1:d}d}".format(prefix, int(suffix_length), n)

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
#       print("'backup_prefix' reset to '{}'."
#                           .format(backup_prefix))
    else:
        print(
        "WARNING: 'params' is empty, using defaults.")
    if n_lines > 1:
        suffix_length = int(lines[1])
else:
    print("WARNING: No 'params' file, using defaults.")

#print("SANITY CHECK:")
#print("  target is {}.".format(target))
#print("  backup_prefix is '{}'.".format(backup_prefix))
#print("  suffix_length is '{}'.".format(suffix_length))
#print("Target directory contains:")
#for item in os.listdir(target):
#    print('\t' + item)

def is_a_backup(directory,
                target=target,
                backup_prefix=backup_prefix,
                suffix_length=suffix_length):
    """
    A filter helper function: returns a Boolean.
    The required parameter is a directory name- not a path.
    The named parameter has been derived from the location of this
    script- assumed to be the backup target directory.
    Also depends on the two globals: backup_prefix & suffix_length
     b u . 0 0 0
        ^ ^ ^ ^
        | | | `-- -1
        | | `---- -2
        | `------ -3 ([-3:] == -suffix_length)
         `-------  2 (prefix_length <= len(backup_prefix))
         
    """
    suffix_length = int(suffix_length)
    full_path = os.path.join(target, directory)
    prefix_length = len(backup_prefix)
    if (os.path.isdir(full_path)
    and len(directory)==(prefix_length+1+suffix_length)
    and directory[:prefix_length]==backup_prefix
    and directory[prefix_length] == '.'
    and directory[-suffix_length:].isdigit()
        ):
#       print("'{}' is a backup.".format(full_path))
        return True
    else:
#       print("'{}' is NOT a backup.".format(full_path))
        return False

def rename(directory):
    new_dir_name = backup_prefix + '.' + "{:03n}".format(1 +
                            int(directory[-suffix_length:]))
#   print("Trying to 'mv {} {}'.".format(directory, new_dir_name))
    ret = shutil.move(os.path.join(target, directory),
                    os.path.join(target, new_dir_name))
    return ret

bu1 = os.path.join(target, bu_name(backup_prefix, suffix_length, 1))
bu0 = os.path.join(target, bu_name(backup_prefix, suffix_length, 0))


# Do the rippling:
if os.path.isdir(target):
#   print("You've given me an existing directory.")
#   print("'{}' contains:".format(target))
    dir_listing = os.listdir(target)
#   for item in dir_listing:
#       print('\t' + item)
    unsorted_backups_listing = [
      listing for listing in dir_listing if is_a_backup(listing)]
    sorted_backups_listing = sorted(unsorted_backups_listing,
                                reverse=True)
#   print("Contents of sorted_backups_listing:")
#   for item in sorted_backups_listing:
#       print('\t' + item)
#   print("Now for the renaming:")
    for item in sorted_backups_listing:
        new_name = rename(item)
#       print("\t '{}' renamed '{}'.".format(item, new_name))
else:
    print("ERROR: Target directory doesn't exist.")
    sys.exit(1)
    
# Hard link backup zero:
link_sequence = (
                    "rsync",
                    "-av",
                    "--link-dest={}".format(bu1),
                    "{}/".format(bu1),  # Ensure crucial trailing /.
                    bu0,
                    )

### Next 5 lines OR..
#print("About to run the following command:")
#print(" ".join(link_sequence))
#response = input("Go ahead? ")
#if response and response[0] in 'yY':
#    ret = subprocess.call(link_sequence)
### the line that follows..
ret = subprocess.call(link_sequence)
if ret:
    print("ERROR: creation of bu.000 using linking failed.")

