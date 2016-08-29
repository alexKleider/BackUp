#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :
#
# file: 'tests/test1.py'
# Part of ___, ____.

# Copyright 2016 Alex Kleider
# See COPYING.txt distributed with this file.
#"""
#Part of backup utility test suite.
#Begin by testing setup of testing directory structure.
#"""
import unittest
import os
import subprocess as sub
import src.backup as bu

DIRSET = {
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirA',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirA/SubDir_a',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirA/SubDir_b',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirB',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirB/SubDir_a',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirB/SubDir_b',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirC',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirC/SubDir_b',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirC/SubDir_a',
}
FILESET = {
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirA/file1',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirA/file2',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirA/file3',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirA/SubDir_a/f1',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirA/SubDir_a/f2',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirA/SubDir_a/f3',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirA/SubDir_b/f1',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirA/SubDir_b/f2',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirA/SubDir_b/f3',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirB/file1',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirB/file2',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirB/file3',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirB/SubDir_a/f1',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirB/SubDir_a/f2',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirB/SubDir_a/f3',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirB/SubDir_b/f1',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirB/SubDir_b/f2',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirB/SubDir_b/f3',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirC/file1',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirC/file2',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirC/file3',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirC/SubDir_a/f1',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirC/SubDir_a/f2',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirC/SubDir_a/f3',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirC/SubDir_b/f1',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirC/SubDir_b/f2',
'/home/alex/Py/BackUp/BackUp/tests/data/source/DirC/SubDir_b/f3',
}

def create_file_hierarchy_in(parent):
    """Helper function- tested by client: MoveFiles.test_dir_setup().
    """
    dirset = set()
    fileset = set()
    for root, dirs, files in (
                    os.walk(os.path.abspath(parent))):
        for d in dirs:
            dirset.add(os.path.join(root, d))
        for f in files:
            fileset.add(os.path.join(root, f))
    return dirset, fileset

def populate_files_with_text(fileset):
    for file_name in fileset:
        with open(file_name, 'w') as f:
            f.write("Initial entry in text file:\n{}\n"
                        .format(file_name))

def modify_files(fileset, lastchar=None):
    """Modifies files in <fileset>.
    By default all are modified.
    If <lastchar> is set, only files who's last character matches are
    modified.
    """

    for file_name in fileset:
        if (lastchar is None) or (file_name[-1] == lastchar): 
            with open(file_name, 'a') as f:
                f.write("First addition to 1 files:\n{}\n"
                            .format(file_name))

def check(prompt):
    """Stops execution providing an opportunity to check status.
    """
    _ = input(
    "{}- then <--|".format(prompt))

class MoveFiles(unittest.TestCase):
    """
    """
    maxDiff = None

    def setUp(self):
        sub.call(['./tests/scripts/makedirstruct.sh'])
    
    def test_dir_setup(self):
        parent = 'tests/data/source'
        dirset, fileset = create_file_hierarchy_in(parent)
        populate_files_with_text(fileset)
#       check("Check first entry")
        modify_files(fileset, "1")
#       check("Check second entry (to '1' files)")
        self.assertEqual((fileset, dirset), (FILESET, DIRSET))

    def tearDown(self):
        sub.call(['./tests/scripts/destroy.sh'])

class GetConfiguration(unittest.TestCase):

    DEFAULT = dict(
        comment='default comment line',
        source='/path/directory',
        destination_dir='/path/directory/',
        destination_host='localhost',
        destination_user='',
        backup_name='bu.',
        suffix_length='3',
        max_number_of_Snapshots='100',
        exclude_file='/home/alex/Python/Bu/rip_exclude',
        )

    def test_get_config_file_name(self):
        self.assertEqual(bu.get_config_file_name(),
                        bu.CONFIG_FILE)

    def test_get_DEFAULT_section_specifics(self):
        config_file = dict()
        conf = bu.get_section_specifics('DEFAULT')
        if isinstance(conf, dict):
            self.assertEqual(conf['DEFAULT'],
                            DEFAULT)
        else:
            self.assertIsInstance(conf,dict)

if __name__ == '__main__':  # code block to run the application
    unittest.main()
