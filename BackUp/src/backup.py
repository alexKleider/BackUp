#!./venv/bin/python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :
#
# file: 'main.py'
# Part of ___, ____.

# Copyright 2016 Alex Kleider
# See COPYING.txt distributed with this file.
"""
Put your docstring here.
"""

import configparser

CONFIG_FILE = './config'  # The default configuration file.

def get_config_file_name():
    """
    Place holder for a function to check for config file in various
    locations: cwd, ~/.ripple.conf, /usr/local/etc/ripple.conf in that
    order unless specified by a parameter to the command line
    -f, --file CONFIGURATION_FILE option.
    """
    return CONFIG_FILE

def get_section_specifics(section=None):
    """Get the required data from the config file.
    """
    pass

if __name__ == '__main__':  # code block to run the application
    pass
    print("Running Python3 script: 'main.py'.......")
#   print('"""', end=''),
#   print(__doc__, end=''),
#   print('"""')


