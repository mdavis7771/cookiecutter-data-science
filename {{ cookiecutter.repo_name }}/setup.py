# -*- coding: utf-8 -*-
import os
import sys
import re
import ast
from setuptools import setup, find_packages
from m2r import convert

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('src/_version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        str(f.read().decode('utf-8'))).group(1)))


# Utility function to read the README.md file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README.md file and 2) it converts markdown to RST
def read_markdown(fname):
    return convert(open(os.path.join(os.path.dirname(__file__), fname)).read())


# This is a private package, don't let anyone accidentally upload it to PyPi
def forbid_publish():
    argv = sys.argv
    blacklist = ['register', 'upload']

    for command in blacklist:
        if command in argv:
            values = {'command': command}
            print('Command "%(command)s" has been blacklisted, exiting...' %
                  values)
            sys.exit(2)


forbid_publish()

setup(
    name='{{ cookiecutter.repo_name }}',
    version=version,
    packages=find_packages(),
    description='{{ cookiecutter.description }}',
    author='{{ cookiecutter.author_name }}',
    license='{% if cookiecutter.open_source_license == 'MIT' %}MIT{% elif cookiecutter.open_source_license == 'BSD-3-Clause' %}BSD-3{% endif %}',
    keywords="ctthreat",
    url="",
    zip_safe=False,
    platforms='any',
    include_package_data=True,
    long_description=read_markdown('README.md'),
    install_requires=[
        "Sphinx",
        "pathlib2",
        "coverage",
        "awscli",
        "flake8",
        "flask-restful",
        "python-dotenv>=0.5.1",
        "numpy",
        "matplotlib",
        "scipy",
        "scikit-learn",
        "jupyter",
        "requests",
        "pandas",
        "seaborn",
        "click",
        "openpyxl",
        "watermark",
        "engarde",
        "scikit-plot",
        "tqdm",
        "sumatra",
        "boto3",
        "botocore",
        "flask_restful"
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 2.7'
        'License :: Other/Proprietary License',
    ],
)
