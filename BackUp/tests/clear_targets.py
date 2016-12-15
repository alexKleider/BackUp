#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :

# file: 'Backup/tests/clear_targets.py'
# Part of ___, ____.

# Copyright 2016 Alex Kleider
# See COPYING.txt distributed with this file.
"""
Test suite for backup utility.
"""
import os
import sys

cwd = os.getcwd()
if not (cwd in sys.path):
    sys.path.insert(0, cwd)
import BackUp.src.backup as bu

bu.clear_testing_targets()
