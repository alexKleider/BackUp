#!/usr/bin/env python3

# file: unripple.py

"""
This script reverses what is done by ripple.py
and is only used for testing purposes.
See the docstring for ripple.py

Requires at least one positional argument: a target directory.
Optional positional parameters:
    first is the backup_name- defaults to 'bu'.
    second is the suffix_length- defaults to 3.
    The optional parameters are provided in case the
defaults in 'config' are not used.  Because this script
is to be run on the backup server, we can't use DRY!

Assumes target is populated by directory files the names of
which are of the form 'bu.nnn' where 'nnn' are suffix_length
string representations of a sequence of numbers.  Decriments
each 'nnn' by one.
"""

import os
import sys
import shutil

# Set up globals:

args = sys.argv
l = len(args)

if l > 1:
    target = args[1]
else:
    print("No parameter provided. Aborting!")
    sys.exit(1)

if l > 2:
    backup_name = args[2]
else:
    backup_name = 'bu'

prefix_length = len(backup_name)
if l > 3:
    suffix_length = args[3]
else:
    suffix_length = 3

bu_dir_length = len(backup_name) + 1 + suffix_length


def is_a_backup(directory):
    """
    A filter helper function: returns a Boolean.

     b u . 0 0 0
        ^ ^ ^ ^
        | | | `-- -1
        | | `---- -2
        | `------ -3 ([-3:] == -suffix_length)
         `-------  2 (prefix_length)
         
    """
    if (os.path.isdir(os.path.join(target, directory))
    and len(directory)==bu_dir_length
    and directory[:prefix_length]==backup_name
    and directory[prefix_length] == '.'
    and directory[-suffix_length:].isdigit()
        ):
        return True
    else:
        return False

def decrementing_rename(directory):
    new_dir_name = backup_name + '.' + "{:03n}".format(-1 +
                            int(directory[-suffix_length:]))
    print("Trying to 'mv {} {}'.".format(directory, new_dir_name))
    ret = shutil.move(os.path.join(target, directory),
                    os.path.join(target, new_dir_name))
    return ret

def main():
    if os.path.isdir(target):
        print("You've given me an existing directory.")
        print("'{}' contains:".format(target))
        dir_listing = os.listdir(target)
        for item in dir_listing:
            print('\t' + item)
        backups_listing = sorted(filter(is_a_backup, dir_listing))
        print("After filtration:")
        for item in backups_listing:
            print('\t' + item + "Becomes {}".format(
            decrementing_rename(item)
            ))


if __name__ == "__main__":
    main()
