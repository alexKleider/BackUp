# Still a work in progress.

# file: setup.py


from distutils.core import setup
setup(
    name = "Backup",
    packages = ["Backup"],
    version = "0.0.0-dev",
    description = "A snapshot, incremental back up utility",
    author = "Alex Kleider",
    author_email = "alex@kleider.ca",
    url = "http://Backup/kleider.ca/",
    download_url =
"https://github.com/alexKleider/Backup.git",
    keywords = ["backup", "incremental", "snapshot"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 0 - Dev",
        "Environment :: Other Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Recovery Tools",
        "Topic :: Utilities",
        ],
    long_description = (
"""Command line incremental backup utility.""")
)

