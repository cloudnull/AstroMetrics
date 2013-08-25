#!/usr/bin/env python
# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================

import setuptools
import sys

from astrometrics import info


REQUIRES = ['libcloud', 'prettytable']


if sys.version_info < (2, 6, 0):
    sys.stderr.write("AstroMetrics Presently requires Python 2.6.0 or greater \n")
    sys.exit('\nUpgrade python because you version of it is VERY deprecated\n')
elif sys.version_info < (2, 7, 0):
    REQUIRES.append('argparse')

with open('README') as r_file:
    LDINFO = r_file.read()

setuptools.setup(
    name=info.__appname__,
    version=info.__version__,
    author=info.__author__,
    author_email=info.__email__,
    description=info.__description__,
    long_description=LDINFO,
    license='GNU General Public License v3 or later (GPLv3+)',
    packages=['astrometrics',
              'astrometrics.arguments',
              'astrometrics.cloud_connect',
              'astrometrics.logger'],
    url=info.__url__,
    install_requires=REQUIRES,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        ('License :: OSI Approved :: GNU General Public License v3 or later'
         ' (GPLv3+)'),
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    entry_points={
        "console_scripts": ["astro = astrometrics.executable:executable"]})
