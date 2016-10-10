#!/bin/bash

# file: createdirstruct.sh

# Creates a directory hierarchy for testing.

# Relies on the first parameter to determin where.

# See also BackUp/tests/scripts/makedirstruct.sh which is 
# 'hard wired' to create the same hierarchy in
# BackUp/tests/data/source/.

mkdir ${1}/Dir{A..C}
mkdir ${1}/Dir{A..C}/SubDir_{a..b}
touch ${1}/Dir{A..C}/file{1..3}
touch ${1}/Dir{A..C}/SubDir_{a..b}/f{1..3}
