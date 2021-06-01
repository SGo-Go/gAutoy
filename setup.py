#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project gAutoy
gAutoy Copyright (C) 2015 SGogolenko
All rights reserved

This file is part of gAutoy.

gAutoy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

gAutoy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gAutoy.  If not, see <http://www.gnu.org/licenses/>.

######################################################################
@package      gAutoy
@file         setup.py
@author       Sergiy Gogolenko
@license      GPLv3

Setup script for gAutoy package.
You can install gAutoy package with 'python setup.py install'
######################################################################
"""
from glob import glob
import os, sys

from setuptools import setup
# from distutils.core import setup
# import py2exe

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")
    print()

if sys.version_info[:2] < (2, 7):
    print("gAutoy requires Python 2.7 or later (%d.%d detected)." %
          sys.version_info[:2])
    sys.exit(-1)

# Write the version information.
sys.path.insert(0, 'gAutoy')
import release
version = release.write_versionfile()
sys.path.pop(0)

packages=[ "gautoy",
           "gautoy.core",
           "gautoy.cbm",
           "gautoy.log",
           "gautoy.log.pattern",
           "gautoy.target",
           "gautoy.tools",
           "gautoy.tools.traceclient",
           "gautoy.domain",
           "gautoy.domain.maps",
           "gautoy.domain.most",
           "gautoy.notebook" ]

# # add the tests
# package_data = {
#     'gAutoy': ['tests/*.py'],
#     }

package_data = {
    'gAutoy': ['gautoy/domain/maps/jinja2/*.html'],
    }

install_requires = ['markdown2',] #'paramiko >= 1.12.0', 'posixpath','win32com'

if __name__ == "__main__":

    setup(
        name            = release.name,
        version         = version,
        description     = release.description,
        long_description= release.long_description,
        author          = release.authors['Gogolenko'][0],
        author_email    = release.authors['Gogolenko'][1],
        license         = release.license,
        url             = release.url,
        packages        = packages,
        
        package_data    = package_data,
        # include_package_data = True,
        
        platforms       = release.platforms,
        download_url    = release.download_url,
        install_requires= install_requires,
        
        keywords        = release.keywords,
        classifiers     = release.classifiers,
        zip_safe        = False,
    )
