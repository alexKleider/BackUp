#!/usr/bin/env python3

# file: ripple.py

"""
Usage:
    ripple.py TARGET [BACKUP_NAME [SUFFIX_LENGTH]]

Requires at least one positional argument: a target directory.
Optional positional parameters:
    first is the backup_name- defaults to 'bu'.
    second is the suffix_length- defaults to 3.
    The optional parameters are provided in case the
defaults in 'config' are not used.  Because this script
is to be run on the backup server, we can't use DRY!

Assumes target is populated by directory files the names of
which are of the form 'bu.nnn' where 'nnn' are suffix_length
string representations of a sequence of numbers.

This script renames these files so the number componenet of
each is incremented by one.
i.e. we start with bu.000, bu.001, bu.002 
and end up with bu.001, bu.002, bu.003.

Only names are changed, and only those conforming to the pattern.
"""

import os
import sys
import shutil

# Set up globals:

_args = sys.argv
_l = len(_args)

if _l > 1:
    target = _args[1]
else:
    print("Running ripple.py but no parameter provided. Aborting!")
    sys.exit(1)

if _l > 2:
    backup_name = _args[2]
else:
    backup_name = 'bu'

prefix_length = len(backup_name)
if _l > 3:
    suffix_length = int(_args[3])
else:
    suffix_length = 3

bu_dir_length = len(backup_name) + 1 + suffix_length


def is_a_backup(directory, target=target):
    """
    A filter helper function: returns a Boolean.
    The required parameter is a directory name- not a path.
    The named parameter relies on the script's command line argument.

     b u . 0 0 0
        ^ ^ ^ ^
        | | | `-- -1
        | | `---- -2
        | `------ -3 ([-3:] == -suffix_length)
         `-------  2 (prefix_length)
         
    """
    full_path = os.path.join(target, directory)
    if (os.path.isdir(full_path)
    and len(directory)==bu_dir_length
    and directory[:prefix_length]==backup_name
    and directory[prefix_length] == '.'
    and directory[-suffix_length:].isdigit()
        ):
#       print("'{}' is a backup.".format(full_path))
        return True
    else:
#       print("'{}' is NOT a backup.".format(full_path))
        return False

def rename(directory):
    new_dir_name = backup_name + '.' + "{:03n}".format(1 +
                            int(directory[-suffix_length:]))
#   print("Trying to 'mv {} {}'.".format(directory, new_dir_name))
    ret = shutil.move(os.path.join(target, directory),
                    os.path.join(target, new_dir_name))
    return ret

def main():
    if os.path.isdir(target):
#       print("You've given me an existing directory.")
#       print("'{}' contains:".format(target))
        dir_listing = os.listdir(target)
        for item in dir_listing:
            print('\t' + item)
        backups_listing = sorted(filter(is_a_backup, dir_listing),
                                    reverse=True)
#       print("After filtration:")
        for item in backups_listing:
#           print("\t'" + item + "' renamed '{}'".format(
            rename(item)
            ))


if __name__ == "__main__":
    main()

