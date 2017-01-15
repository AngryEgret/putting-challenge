# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

from putting_challenge import __version__

__docformat__ = 'reStructuredText'


packages = find_packages()

# we only want to put production dependencies in our egg manifest
install_requires = []
tests_require = []
with open('requirements.txt') as fh:
    capture = install_requires
    for line in fh.readlines():
        if line.startswith('#'):
            if 'tests' in line.lower():
                capture = tests_require
            continue
        capture.append(line.strip())

setup(
    name='putting_challenge',
    version=__version__,
    packages=packages,
    description='',
    package_data={
        str(''): ['*.json', '*.txt', '*.rst', '*.yml']
    },
    entry_points={
        'console_scripts': []
    },
    install_requires=install_requires,
    url='',
    zip_safe=True,
)
