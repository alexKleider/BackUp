#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :
#
# file: 'tests/testA.py'
# Part of ___, ____.

# Copyright 2016 Alex Kleider
# See COPYING.txt distributed with this file.
#"""
#Part of backup utility test suite.
#Begin by testing setup of testing directory structure.
#"""
import os
# print(os.getcwd())
import sys
# print(sys.path)
import unittest
import subprocess as sub
sys.path.append(os.getcwd())
import BackUp.src.backup as bu



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

def get_dict(dict_like_object):
    """
    Solves the problem that configparser provides a dictionary like
    object but it isn't of type dict.
    """
    real_dict = dict()
    for key in dict_like_object:
        real_dict[key] = dict_like_object[key]
    return real_dict

def get_directory_and_file_sets(parent):
    """Helper function- tested by client: MoveFiles.test_dir_setup().
    """
    print("ENTERING create_file_heirarchy_in")
    print("Planning to os.walk {}.".format(os.path.abspath(parent)))
    dirset = set()
    fileset = set()
    for root, dirs, files in (
                    os.walk(os.path.abspath(parent))):
        print("root, dirs == {}, {}".format(root, dirs))
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

    header = "First addition to files"
    if lastchar:
        header = ("First addition to files ending in '{}'"
                            .format(lastchar))
    for file_name in fileset:
        if (lastchar is None) or (file_name[-1] == lastchar): 
            with open(file_name, 'a') as f:
                f.write("{}:\n\t{}\n"
                            .format(file_name))

def check(prompt):
    """Stops execution providing an opportunity to check status.
    """
    _ = input(
    "{}- then <--|".format(prompt))

class ShowArgs(unittest.TestCase):
    """
    Tests BackUp.src.backup.show_args().
    """
    header = "Arguments"
    a_list = ['Kelly', 'Tanya', 'June', 'Alex']
    a_dict = dict(
        Kelly='youngest',
        Tanya='oldest',
        June='matriarch',
        Alex='patriarch',
        )
    expected_4list = """{} are ...
  Kelly
  Tanya
  June
  Alex
  ... end of report.
""".format(header)
    expected_4dict = """{} are ...
  Alex: patriarch
  June: matriarch
  Kelly: youngest
  Tanya: oldest
  ... end of report.
""".format(header)

    def test_show_args_w_list(self):
        self.assertEqual(bu.show_args(self.a_list, self.header),
                        self.expected_4list)

    def test_show_args_w_dict(self):
        self.assertEqual(bu.show_args(self.a_dict, self.header),
                        self.expected_4dict)


class GetConfiguration(unittest.TestCase):
    
    DEFAULT = dict(
        comment= 'default comment line',
        source= '/path/to/source/directory/',
        destination_dir= '/path/to/destination/directory/',
        destination_host= 'localhost',
        destination_port= '22',
        destination_user= '',
        backup_name= 'bu',
        suffix_length= '3',
        exclude_file= '',
        rippler= 'BackUp/src/ripple.py',
        # The following is calculated, not found in CONFIG:
        max_number_of_snapshots= 999,
        )

    test_local = dict(
        comment = 'for testing: local host both ends.',
        source = 'tests/data/source/',
        destination_dir = 'tests/data/dest',
        destination_host= 'localhost',
        destination_port= '22',
        destination_user= '',
        backup_name= 'bu',
        suffix_length= '3',
        exclude_file = 'tests/data/rip_exclude',
        rippler= 'BackUp/src/ripple.py',
        max_number_of_snapshots= 999,
        )
 
    test_remote = dict(
        comment = 'for testing: bu on remote host.',
        source = 'tests/data/source/',
        destination_dir = '/mnt/BU/Sandbox',
        destination_host= 'indi303.net',
        destination_port= '5322',
        destination_user= 'alex',
        backup_name= 'bu',
        suffix_length= '3',
        exclude_file = 'tests/data/rip_exclude',
        rippler= 'BackUp/src/ripple.py',
        max_number_of_snapshots= 999,
)

    def test_get_DEFAULT_section_specifics(self):
        default = get_dict(bu.get_section_specifics('DEFAULT'))
        self.assertEqual(default,
                        self.DEFAULT)

    def test_get_test_local_section_specifics(self):
        test = get_dict(bu.get_section_specifics('test_local'))
        self.assertEqual(test,
                        self.test_local)

    def test_get_test_remote_section_specifics(self):
        test = get_dict(bu.get_section_specifics('test_remote'))
        self.assertEqual(test,
                        self.test_remote)

if __name__ == '__main__':  # code block to run the application
    unittest.main()
