#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :

# file: 'Backup/tests/test1.py'
# Part of ___, ____.

# Copyright 2016 Alex Kleider
# See COPYING.txt distributed with this file.
"""
Test suite for backup utility.
"""
import unittest
import os
import sys
import subprocess
cwd = os.getcwd()
if not (cwd in sys.path):
    sys.path.insert(0, cwd)
import BackUp.src.backup as bu


def check(prompt):
    """
    Stops execution providing an opportunity
    for mannual checks.
    """
    _ = input(
    "{}- then <--|".format(prompt))

def get_dict(dict_like_object):
    """
    Solves the problem that configparser provides a dictionary like
    object but it isn't of type dict.
    """
    real_dict = dict()
    for key in dict_like_object:
        real_dict[key] = dict_like_object[key]
    return real_dict

def create_file_hierarchy_in(
            existing_dir="Backup/tests/data/source"):
    """
    Creates a testing directory hierarchy.
    """
#   check("ENTERING create_file_heirarchy_in('{}')."
#               .format(existing_dir))
    target = os.path.abspath(existing_dir)
    return subprocess.call([
        "BackUp/tests/scripts/createdirstruct.sh",
        target])

def destroy_test_content(
            dir1="Backup/tests/data/source",
            dir2="Backup/tests/data/dest"):
    d1 = os.path.abspath(dir1)
    d2 = os.path.abspath(dir2)
    return subprocess.call([
        "BackUp/tests/scripts/destroy2params.sh",
        d1, d2])

def populate_files_with_text(fileset):
    for file_name in fileset:
        with open(file_name, 'w') as f:
            f.write("Initial entry in text file:\n{}\n"
                        .format(file_name))

def modify_files(fileset, lastchar=None):
    """Modifies files in <fileset>.
    By default all are modified.
    If <lastchar> is set, the only files modified are
    those with a last character that matches <lastchar>.
    """
    header = "First addition to files"
    if lastchar:
        header = ("First addition to files ending in '{}'"
                            .format(lastchar))
    for file_name in fileset:
        if (lastchar is None) or (file_name[-1] == lastchar): 
            with open(file_name, 'a') as f:
                f.write("{}:\n\t{}\n"
                            .format(header, file_name))

def get_directory_and_file_sets(containing_directory):
    """Helper function- tested by client: MoveFiles.test_dir_setup().
    """
    directory = os.path.abspath(containing_directory)
#   check("Planning to os.walk {}.".format(directory))
    dirset = set()
    fileset = set()
#   check("Is the containing_directory populated?")
    for root, dirs, files in os.walk(directory):
#       print("root, dirs == {}, {}".format(root, dirs))
        for d in dirs:
            dirset.add(os.path.join(root, d))
        for f in files:
            fileset.add(os.path.join(root, f))
#   print("Sets being returned are:")
#   print("Directories: {}".format(dirset))
#   print("Files: {}".format(fileset))
    return dirset, fileset

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

class GetSuffix(unittest.TestCase):

    def test_get_suffix(self):
        test_data = (# number, length, returned
                        (0, 0, None), 
                        (1, 0, None),
                        (0, 1, "0"),
                        (10, 1, None),
                        (999, 3, "999"),
                        (111, 2, None),
                        (4389, 5, "04389"),
                        (9, 3, "009"),
            
        )
        for number, length, returned in test_data:
            with self.subTest(number=number,
                                length=length,
                                returned=returned):
                self.assertEqual(bu.get_suffix(number, length),
                                returned)

class GetConfiguration(unittest.TestCase):
    
    DEFAULT = dict(
        comment= 'default comment line',
        source= '/path/to/source/directory/',
        target= '/path/to/directory/holding/snapshots',
        host= 'localhost',
        port= '22',
        user= 'alex',
        backup_name= 'bu',
        suffix_length= '3',
        exclude_file= '',
        rippler= 'BackUp/src/ripple.py',
        # The following is calculated, not found in CONFIG:
        max_number_of_snapshots= 999,
        bu0= "bu.000",
        bu1= "bu.001",
        bu2= "bu.002",
        )

    test_local = dict(
        comment = 'for testing: local host both ends.',
        source = 'tests/data/source/',
        target = 'tests/data/dest',
        host= 'localhost',
        port= '22',
        user= 'alex',
        backup_name= 'bu',
        suffix_length= '3',
        exclude_file = 'tests/data/rip_exclude',
        rippler= 'BackUp/src/ripple.py',
        max_number_of_snapshots= 999,
        bu0= "bu.000",
        bu1= "bu.001",
        bu2= "bu.002",
        )
 
    test_remote_indi = dict(
        comment = 'for testing: bu on remote host indi303.net.',
        source = 'tests/data/source/',
        target = '/mnt/BU/Sandbox',
        host= 'indi303.net',
        port= '5322',
        user= 'alex',
        backup_name= 'bu',
        suffix_length= '3',
        exclude_file = 'tests/data/rip_exclude',
        rippler= 'BackUp/src/ripple.py',
        max_number_of_snapshots= 999,
        bu0= "bu.000",
        bu1= "bu.001",
        bu2= "bu.002",
)
 
    test_remote_pi = dict(
        comment = 'for testing: bu on remote host 10.10.10.10.',
        source = 'tests/data/source/',
        target = '/home/alex/BU',
        host= '10.10.10.10',
        port= '22',
        user= 'alex',
        backup_name= 'bu',
        suffix_length= '3',
        exclude_file = 'tests/data/rip_exclude',
        rippler= 'BackUp/src/ripple.py',
        max_number_of_snapshots= 999,
        bu0= "bu.000",
        bu1= "bu.001",
        bu2= "bu.002",
)

    def test_get_DEFAULT_section_specifics(self):
        default = get_dict(bu.get_section_specifics('DEFAULT'))
        self.assertEqual(default,
                        self.DEFAULT)

    def test_get_test_local_section_specifics(self):
        test = get_dict(bu.get_section_specifics('test_local'))
        self.assertEqual(test,
                        self.test_local)

    def test_get_test_remote_section_specifics_indi(self):
        test = get_dict(bu.get_section_specifics('test_remote_indi'))
        self.assertEqual(test,
                        self.test_remote_indi)

    def test_get_test_remote_section_specifics_pi(self):
        test = get_dict(bu.get_section_specifics('test_remote_pi'))
        self.assertEqual(test,
                        self.test_remote_pi)

class MoveFiles(unittest.TestCase):
    """
    Indirectly tests the makedirstruct.sh script.
    """
    maxDiff = None

    def setUp(self):
        # Just in case clean up failed during a previous run:
        subprocess.call(['./BackUp/tests/scripts/destroy.sh'])

        script_file = os.path.abspath(
            'BackUp/tests/scripts/makedirstruct.sh')
        error_code = subprocess.call([script_file, ])
#       check("Check that source dir hierarchy has been set up.")
        if error_code:
            print(
                "#!#! Couldn't set up directory hierarchy. #!#!")
            sys.exit(error_code)

    
    def test_dir_setup(self):
        parent = 'BackUp/tests/data/source'
#       check("Calling get_dir...({})".format(parent))
        dirset, fileset = get_directory_and_file_sets(parent)
        populate_files_with_text(fileset)
#       check("Check first entry")
        modify_files(fileset, "1")
#       check("Check second entry (to '1' files)")
#       check("Set sizes are {} | {} and {} | {}"
#           .format(len(fileset), len(FILESET),
#                   len(dirset), len(DIRSET)))
        self.assertEqual((fileset, dirset), (FILESET, DIRSET))

    def tearDown(self):
        subprocess.call(['./BackUp/tests/scripts/destroy.sh'])

if __name__ == '__main__':  # code block to run the application
    unittest.main()
