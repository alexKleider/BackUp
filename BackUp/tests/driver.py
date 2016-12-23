#!/usr/bin/env python3

# File: BackUp/tests/driver.py

import os
import sys
import subprocess
import BackUp.src.backup as backup

def pause(text=None, ignore=False):
    """ Use to pause execution, leave an optional message,
    and give the user the choice of continuing or aborting.
    Set ignore to True to forge ahead with no pause.)
    """
    if ignore: return
    if not text is None: print(text)
    response = input("System halts OR 'y' <--' to continue: ")
    if response and response[:1] in "yY": return
    else: sys.exit()

sections = (   # Sections set up for testing in BackUp/config.
    "test_local",
    "test_remote_pi",
#   "test_remote_indi",
    )

# Assume all test sections use the same source-
# ... acquire the testing source (2 components:)
args = backup.get_section_specifics(sections[0])
path2source = args["source"]
if path2source[-1:] == '/':
    path2source = path2source[:-1]
path, source = os.path.split(path2source)

# Test each section in turn:
for section in sections:
    # Assume source exists from previous run-
    # Delete existing source...
    cmd = (
        "./BackUp/tests/source_setup.sh",
        path,
        source,
        )
    pause("Command to create source is:\n{}"
                .format(' '.join(cmd)), True)
    ret = subprocess.call(cmd)
    # ... and populate a fresh one:
    ret = subprocess.call(cmd)
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
                .format(" ".join(cmd_args)), True)
        ret = subprocess.call(" ".join(cmd_args), shell=True)
        if ret:
            pause("WARNING: 'rm' command failed.")
    else:
        pause("Have you zeroed out the target directory?")
        # Might add code to zero out on a foreign target host.

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
            pause("\n".join((
            "Expect diff to report the dot files-",
            "Call to diff returned exit code '{}' ...\n{}" 
                                .format(diff[0], diff[1]))))
    else:  # Target is on a foreign host:
        pass 
    
    # Send params & run the ripling and linking routines:
    backup.create_and_send_params_file(args)
    backup.send_and_run(args)

    pause(
    "End of 1st backup. NEXT: modify source & then backup again...")
    # MODIFY-
    file2modify = os.path.join(args["source"], "DirA/filesA1")
    with open(file2modify, "a") as f:
        f.write("First mod, adding a line to DirA/fileA1")
    # This time all of backup can be a single command..."
    backup.backup(args)

    pause(
    "End of 2nd backup. NEXT: modify source & then backup again...")
    # MODIFY-
    file2add = os.path.join(args["source"], "DirB/fileNew")
    with open(file2add, "w") as f:
        f.write("Second mod: Create DirB/fileNew /w this text")
    # Again do all of backup as a single command..."
    backup.backup(args)

    pause(
    "End of 3rd backup. NEXT: modify source & then backup again...")
    # MODIFY-
    file2modify = os.path.join(args["source"], "DirB/fileNew")
    with open(file2modify, "a") as f:
        f.write("Third mod: Add another line to DirB/fileNew")
    # Again do all of backup as a single command..."
    backup.backup(args)

    pause(
    "End of 4th backup. NEXT: Two mods this time...")
    # MODIFY-
    file2add = os.path.join(args["source"], "DirA/fileNewA1")
    with open(file2add, "w") as f:
        f.write("1 of 2 mods this 4th time: create DirA/fileNewA1")
    file2modify = os.path.join(args["source"], "DirB/fileNew")
    with open(file2modify, "a") as f:
        f.write("2 of 2 mods this 4th time: add to DirB/fileNew")
    # Again do all of backup as a single command..."
    backup.backup(args)

