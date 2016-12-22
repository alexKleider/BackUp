#!/bin/bash

# File: source_setup.sh

# Accepts an optional parameter: a directory.
# Can also accept a second optional parameter:
# ..the name of the source directory to create
# in the specified directory.
# Defaults are provided for unspecified parameters.

dir=/home/alex/Py/BackUp/Sandbox
src=Source

# If such a source directory already exists,
# you are given the option of deleting it but you'll
# have to re-run the script to create a new one.

echo '##############################################'

if [[ !  -z  $1  ]]  # Not zero (double negative.)
then
    echo dir is being set to $1
    dir=$1
    if [[ ! -z $2 ]]
    then
        echo Source is being set to $2
        src=$2
    else
        echo No source specified: using the default..
        echo "  which is: ${src}."
    fi
else
    echo "No parameter passed; dir remains the default.."
    echo "  which is: ${dir}."
fi

if [ -d ${dir} ]
then
    echo The specified \(parent\) directory exists.
    if [ -d ${dir}/${src} ]
    then
        echo It already contains a $src directory.
        echo Do you want to delete it?
        read -r -n1 c
        if [ "$c" = "y" ]
        then
            echo "  Then it will be deleted."
            echo You will have to run the script again
            echo in order to create a new one.
            ### Deleting code goes here:
            if rm -fr ${dir}/${src}
            then
                echo SUCCESS: Deleted old source directory.
            else
                echo ERROR: Deletion did not succeed.
            fi
            ### ... end of deleting code.
        else
            echo "  OK then, we will terminate leaving it alone."
        fi
    else
        echo It does NOT contain a $src directory.
        echo Should we create one?
        read -r -n1 c
        if [ "$c" = "y" ]
        then
            echo "  Then it will be created."
            ### Creation code goes here:
            if  mkdir ${dir}/${src} &&\
                mkdir ${dir}/${src}/DirA &&\
                mkdir ${dir}/${src}/DirB &&\
                mkdir ${dir}/${src}/.HiddenDirA &&\
                touch ${dir}/${src}/.HiddenDirA/fileInHiddenDir &&\
                touch ${dir}/${src}/DirA/.hiddenFileInDirA &&\
                touch ${dir}/${src}/DirA/fileA1 &&\
                touch ${dir}/${src}/DirA/fileA2 &&\
                touch ${dir}/${src}/DirB/fileB1
            then
                echo "SUCCESS: Created NEW SOURCE DIRECTORY HIERARCHY."
            else
                echo ERROR: Commands DID NOT COMPLETE successfully.
            fi
            ### ... end of creation code.
        else
            echo "  OK then, we will terminate: NOTHING DONE."
        fi

    fi
else
    echo A $dir directory does NOT exist.
fi

