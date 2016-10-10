#!/bin/bash

# file: destroy2params.sh

# Removes all content of the required two directory parameters.

# See also BackUp/tests/scripts/destroy.sh which is 'hard wired'
# to destoy the content of the the source and dest file heirarchies
# used for testing.

rm -rf ${1}/*
rm -rf ${1}/*

