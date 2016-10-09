#!/usr/bin/env python3

# file: ignore.py

"""
This script prints to STDOUT the contents of 
    .gitignore  and
    .git/info/exclude.
"""
files2ignore = ['.gitignore', '.git/info/exclude']
for file2ignore in files2ignore:
    print("=======  {}  ==========".format(file2ignore))
    with open(file2ignore, "r") as f:
        for line in f:
            line = line.strip()
            if line and line[0]!='#':
                print('\t' + line)
