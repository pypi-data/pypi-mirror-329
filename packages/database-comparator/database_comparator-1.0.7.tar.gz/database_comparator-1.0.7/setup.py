from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

VERSION = '1.0.7'
DESCRIPTION = 'Bioinformatics tool for compering large sequence files'
LONG_DESCRIPTION = 'Bioinformatics tool for compering large sequence files with exact matching, sequence alignment, BLAST searches,and calculating Hamming distances between sequences.'

# Setting up
setup(
    name="database_comparator",  # Changed from "Database_comparator" to comply with PEP 625
    version=VERSION,
    author="preislet (Tomáš Preisler)",
    author_email="<tomas.preisler1@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)

