#!/bin/bash

# file: makedirstruct.sh

# Creates a directory hierarchy for testing.

# 'Hard wired' to create the hierarchy in
# BackUp/tests/data/source/.

# See also BackUp/tests/scripts/createdirstruct.sh which 
# requires a parameter to specify the directory beneath
# which to place the new hierarchy.

mkdir BackUp/tests/data/source/Dir{A..C}
mkdir BackUp/tests/data/source/Dir{A..C}/SubDir_{a..b}
touch BackUp/tests/data/source/Dir{A..C}/file{1..3}
touch BackUp/tests/data/source/Dir{A..C}/SubDir_{a..b}/f{1..3}
