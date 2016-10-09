#!/bin/bash

# file: makedirstruct.sh

# Creates a directory hierarchy for testing.
mkdir BackUp/tests/data/source/Dir{A..C}
mkdir BackUp/tests/data/source/Dir{A..C}/SubDir_{a..b}
touch BackUp/tests/data/source/Dir{A..C}/file{1..3}
touch BackUp/tests/data/source/Dir{A..C}/SubDir_{a..b}/f{1..3}
