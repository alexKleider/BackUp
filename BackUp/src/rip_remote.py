#!/usr/bin/env python3

# File: rip_remote.py

# This is the rippling script that expects itself to reside on the
# target host in the target directory.  It checks for the presence
# of a 'params' file in the same directory and if found, uses it to
# over-ride the values of the two parameters it requires:
#    buckup_prefix
#    suffix_length

# It is called from the source host using the following command:
# ssh -p22 alex@10.10.10.10 ${target}/rip_remote.py

import os
import shutil

param_filename = 'params'

backup_prefix = 'bu'
suffix_length = 3
# the following are how they are declared in the config file:
#  backup_name = 'bu'
#  suffix_length = 3

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


print("SANITY CHECK:")    
print("  target is {}.".format(target))
print("  backup_prefix is '{}'.".format(backup_prefix))
print("  suffix_length is '{}'.".format(suffix_length))

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
        print("'{}' is a backup.".format(full_path))
        return True
    else:
        print("'{}' is NOT a backup.".format(full_path))
        return False

def rename(directory):
    new_dir_name = backup_prefix + '.' + "{:03n}".format(1 +
                            int(directory[-suffix_length:]))
#   print("Trying to 'mv {} {}'.".format(directory, new_dir_name))
    ret = shutil.move(os.path.join(target, directory),
                    os.path.join(target, new_dir_name))
    return ret

def main():
    """
    Assumes access to the following:
        target
        is_a_backup()
        rename()
    """
    if os.path.isdir(target):
        print("You've given me an existing directory.")
        print("'{}' contains:".format(target))
        dir_listing = os.listdir(target)
        for item in dir_listing:
            print('\t' + item)
        unsorted_backups_listing = [
          listing for listing in dir_listing if is_a_backup(listing)]
        sorted_backups_listing = sorted(unsorted_backups_listing,
                                    reverse=True)
        print("Contents of sorted_backups_listing:")
        for item in sorted_backups_listing:
            print('\t' + item)
        print("Now for the renaming:")
        for item in sorted_backups_listing:
            new_name = rename(item)
            print("\t '{}' renamed '{}'.".format(item, new_name))


if __name__ == "__main__":
    main()
