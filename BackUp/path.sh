# This script adds the current working directory to the PYTHONPATH.
# It must be sourced, not run as a command!

export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}/$(pwd)"

