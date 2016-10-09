######
BACKUP
######

``BackUp`` is a project which provides **backup.py**, a command
line utility (written in Python 3) for providing snapshot backups.

************
Installation
************

The following is a suggested way of getting up and running.
Choose an existing directory to serve as a parent for the project
directory; your home directory (``~``) is suggested.
Be sure it is your working directory and then clone the repository
thus creating the project directory structure.  Make that your current
working directory.  The following commands will do the above::
    
    cd ~
    git pull https://github.com/alexKleider/BackUp.git
    cd BackUp

To run the test suite, descend into the deeper ``BackUp`` directory::
    
    cd Backup
    ./Tests/test1.py

Customize the ``config`` file to suit your own needs. 
For the time being, the config file is hard coded as ``config`` but
will eventually it will have to be specified as follows:

When ``backup.py`` is run it requires a single parameter which must
match an entry in either the default ``config`` file or a file
specified using the ``-c file.conf`` | ``--conf=file.conf`` option.
``config`` is extensively commented and pretty well self
explanatory.  Edit it to suit your needs.


