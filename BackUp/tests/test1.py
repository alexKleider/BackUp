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

class MoveFiles(unittest.TestCase):
    """
    Indirectly tests the makedirstruct.sh script.

    """
    maxDiff = None

    def setUp(self):
        script_file = os.path.abspath(
            'BackUp/tests/scripts/makedirstruct.sh')
        error_code = sub.call([script_file, ])
        if error_code:
            print(
                "#!#! Couldn't set up directory hierarchy. #!#!")
            sys.exit(error_code)

    
    def test_dir_setup(self):
        parent = './Backup/tests/data/source'
        dirset, fileset = get_directory_and_file_sets(parent)
        populate_files_with_text(fileset)
#       check("Check first entry")
        modify_files(fileset, "1")
#       check("Check second entry (to '1' files)")
        print("Set sizes are {} | {} and {} | {}"
            .format(len(fileset), len(FILESET),
                    len(dirset), len(DIRSET)))
        self.assertEqual((fileset, dirset), (FILESET, DIRSET))

    def tearDown(self):
        sub.call(['./BackUp/tests/scripts/destroy.sh'])

class GetConfiguration(unittest.TestCase):

    DEFAULT = dict(
        comment= 'default comment line',
        source= '/path/directory',
        destination_dir= '/path/directory/',
        destination_host= 'localhost',
        destination_port= '22',
        destination_user= '',
        destination_tmp_dir= '/tmp',
        backup_name= 'bu.',
        suffix_length= '3',
        exclude_file= '',
        rippler= 'rip_bu.py',
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
        destination_tmp_dir= '/tmp',
        backup_name= 'bu.',
        suffix_length= '3',
        max_number_of_snapshots= 999,
        exclude_file = 'tests/data/rip_exclude',
        rippler= 'rip_bu.py',
        )
    
    commands_local = dict(
        rsync= 'rsync -a --delete  ' +
            '--exclude-from=tests/data/rip_exclude ' +
            'tests/data/source ' +
            '/tests/data/dest',

        scp_conf= '',
        scp_script= '',
        chmod= '',
        ripple= './rip_bu.py',
          )
 
    test_remote = dict(
        comment = 'for testing: local host both ends.',
        source = 'tests/data/source/',
        destination_dir = 'tests/data/dest',
        destination_host= 'pat.lan',
        destination_port= '22',
        destination_user= 'pi',
        destination_tmp_dir= '/tmp',
        backup_name= 'bu.',
        suffix_length= '3',
        max_number_of_snapshots= 999,
        exclude_file = 'tests/data/rip_exclude',
        )

    commands_remote = dict(
        rsync= 'rsync -az --delete -e "ssh -p22 pi" ' +
            '--exclude-from=tests/data/rip_exclude ' +
            'tests/data/source ' +
            'pat.lan:/var/BU/',

        scp_conf= 'scp -p 22 Temp_File dest',
        scp_script= 'scp -p 22 rip_bu.py dest',
        chmod=
    'ssh -oPort=22 -oUser=pi pat chmod 755 rip_bu.py',
        ripple= 
    'ssh -oPort=22 -oUser=pi pat.lan rip_bu.py',
        )

    def test_get_config_file_name(self):
        self.assertEqual(bu.get_config_file_name(),
                        bu.CONFIG_FILE)

"""
    def test_get_DEFAULT_section_specifics(self):
        default = get_dict(bu.get_section_specifics('DEFAULT'))
        self.assertEqual(default,
                        self.DEFAULT)

    def test_get_test_local_section_specifics(self):
        test = get_dict(bu.get_section_specifics('test_local'))
        self.assertEqual(test,
                        self.test_local)

    def test_get_commands_local(self):
        commands = bu.get_commands(self.test_local)
        with open('debug.txt', 'w') as f:
            print(show_args(commands, 'test_local_cmds'),
                                                file=f)
            print(show_args(self.commands_local, 'assumed_cmds'),
                                                file=f)
        self.assertEqual(commands,
                        self.commands_local)

    def test_get_commands_remote(self):
        commands = bu.get_commands(self.test_remote)
        with open('debug.txt', 'a') as f:
            print(show_args(commands, 'test_remote_cmds'),
                                                file=f)
            print(show_args(self.commands_remote, 'assumed_cmds'),
                                                file=f)
        self.assertEqual(commands,
                        self.commands_remote)


"""


"""
The info for each section provides for the following 5 commands:
Traceback (most recent call last):
  File "./tests/test1.py", line 211, in test_get_commands_remote
      commands = bu.get_commands(self.test_remote)
      AttributeError: 'GetConfiguration' object has no attribute
      'test_remote'

"""

if __name__ == '__main__':  # code block to run the application
    unittest.main()
