#!/usr/bin/env python3

# File: BackUp/tests/driver.py

import os
import sys
import subprocess
import BackUp.src.backup as backup

def pause(text=None):
    """ Use to pause execution, leave an optional message,
    and give the user the choice of continuing or aborting.
    """
    if not text is None: print(text)
    response = input("System halts OR 'y' <--' to continue: ")
    if response and response[:1] in "yY": return
    else: sys.exit()

sections = (   # Sections set up for testing in BackUp/config.
    "test_local",
    "test_remote_pi",
#   "test_remote_indi",
    )

# Assume that testing of all test sections will use the same source.
# Get the testing args to acquire the testing source:
args = backup.get_section_specifics(sections[0])
# Delete existing source...
path2source = args["source"]
if path2source[-1:] == '/':
    path2source = path2source[:-1]
path, source = os.path.split(path2source)
cmd = (
    "./BackUp/tests/source_setup.sh",
    path,
    source,
    )
pause("Command to run is {}".format(' '.join(cmd)))
ret = subprocess.call(cmd)
# and populate a fresh one:
ret = subprocess.call(cmd)

for section in sections:
    # Get section info:
    args = backup.get_section_specifics(section)
    args["debug"] = True
    print(backup.show_args(args,
        "Args for section {}.".format(section)))

    if args["host"] == "localhost":
        # Zero out target directory:
        cmd_args = (
                    'rm',
                    '-rf',
                    os.path.join(args['target'], '*'),
                    )
        pause("About to run 'rm' as follows:\n{}"
                .format(" ".join(cmd_args)))
        ret = subprocess.call(" ".join(cmd_args), shell=True)
        if ret:
            pause("WARNING: 'rm' command failed.")
    else:
        pause("Have you zeroed out the target directory?")

    # Run the 1st backup:
    backup.rsync(args)
    # We can test if target is on local machine.
    if args["host"] == "localhost":
        destination = os.path.join(args["target"], 
                                args["bu0"])
        diff_cmd = (
                    "diff",
                    '-r',
                    args["source"],
                    destination,
                    )
        pause("About to run diff as follows:\n{}"
                .format(" ".join(diff_cmd)))
        diff = None
        diff = subprocess.getstatusoutput(" ".join(diff_cmd))
#       try:
#       except subprocess.CalledProcessError:
#           pause("Call to 'diff' command failed.")
#       diff = diff.strip()  # White space doesn't count.
        if not diff is None and diff:
            pause(
            "Call to diff returned exit code '{}' ...\n{}" 
                                .format(diff[0], diff[1]))
    else:  # Target is on a foreign host:
        pass 
    
    # Send params & run the ripling and linking routines:
    backup.create_and_send_params_file(args)
    backup.send_and_run(args)

    # 

forgetabouttherest = """


# ROUND ZERO-

# STEP 0: Assume a version of source not yet backed up.
cmd = 
../Test/setup.sh  # To delete the previous source.
../Test/setup.sh  # To create a source directory.
# Also zero out the target (/home/alex/BU) directory
# on the backup host.

# STEP 1: From the source machine (making it trivial)
# do the BACKUP:
rsync -avz --delete /home/alex/Py/BackUp/Sandbox/Source/ 10.10.10.10:/home/alex/BU/bu.000

# Next we must ripple and link:
# To do so, we need the params file and the remotely.py file to be on
# the backup host in its target directory:
#
# Attempts to run local scripts with local params on target host
# failed so now plan is to copy scripts and a params file to target
# and use run_remotely.py to call ssh and run them there.
#
# Make sure both scripts are in the target directory:
./run_remotely.py params,remote.py /home/alex/BU 10.10.10.10 alex 22

# ROUND ONE-
# MODIFY content in Source:
echo First mod, adding a line to DirA/fileA1 >> /home/alex/Py/BackUp/Sandbox/Source/DirA/fileA1
# BACKUP
rsync -avz --delete /home/alex/Py/BackUp/Sandbox/Source/ 10.10.10.10:/home/alex/BU/bu.000
# Then again:
./run_remotely.py params,remote.py /home/alex/BU 10.10.10.10 alex 22

# ROUND TWO-
# MODIFY
echo Second mod: Create DirB/fileNew /w this text > /home/alex/Py/BackUp/Sandbox/Source/DirB/fileNew
# BACKUP
rsync -avz --delete /home/alex/Py/BackUp/Sandbox/Source/ 10.10.10.10:/home/alex/BU/bu.000
# Then again:
./run_remotely.py params,remote.py /home/alex/BU 10.10.10.10 alex 22

# ROUND THREE-
# Modify content again:
echo Third mod: Add another line >> /home/alex/Py/BackUp/Sandbox/Source/DirB/fileNew
# BACKUP
rsync -avz --delete /home/alex/Py/BackUp/Sandbox/Source/ 10.10.10.10:/home/alex/BU/bu.000
# Then again:
./run_remotely.py params,remote.py /home/alex/BU 10.10.10.10 alex 22

# Round FOUR-
# Modify content yet again:
echo 1 of 2 mods this FOURth time: > /home/alex/Py/BackUp/Sandbox/Source/DirA/fileNewA1
echo Create DirA/fileNewA1 and add this text > /home/alex/Py/BackUp/Sandbox/Source/DirA/fileNewA1
echo 2 of 2 mods this FOURth time: >>  /home/alex/Py/BackUp/Sandbox/Source/DirB/fileNew
echo Fourth modification >>  /home/alex/Py/BackUp/Sandbox/Source/DirB/fileNew
# BACKUP
rsync -avz --delete /home/alex/Py/BackUp/Sandbox/Source/ 10.10.10.10:/home/alex/BU/bu.000
# Then again:
./run_remotely.py params,remote.py /home/alex/BU 10.10.10.10 alex 22

"""
