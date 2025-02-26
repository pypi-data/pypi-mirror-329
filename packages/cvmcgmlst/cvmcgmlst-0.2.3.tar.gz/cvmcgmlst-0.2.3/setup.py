#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Jake Cui
# Mail: cqp@cau.edu.cn
# Created Time:  2022-11-16 14:49:41
#############################################

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


requirements = [
    'Bio',
    'pandas',
    'setuptools',
    'cvmcore >= 0.2.2',
    'cvmblaster >= 0.4.8',
    'tabulate'
]


about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'cvmcgmlst', '__init__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)


# Get the long description from the relevant file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="cvmcgmlst",
    version=about['__version__'],
    keywords=["wgs", "cgmlst"],
    description="cgMLST analysis tool",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT Licence",
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=find_packages(),
    include_package_data=True,  # Ensure package data is included
    platforms="any",
    install_requires=requirements,
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 4 - Beta',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'console_scripts': [
            'cvmcgmlst=cvmcgmlst.cvmcgmlst:main',
        ],
    },
)
