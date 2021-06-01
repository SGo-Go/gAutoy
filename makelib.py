#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project  gAutoy
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
@file         makelib.py
@author       Sergiy Gogolenko
@license      GPLv3

Creates Win32/64 installer for gAutoy package

.. note::

   You can install gAutoy with 'python setup.py install' 
   github from sources
######################################################################
"""

import os,shutil,re
os.system('python setup.py bdist_wininst')

patternScreenshots = re.compile(r'^gAutoy-(.+).dev-[0-9]+.win32.exe$')
for filename in os.listdir('dist'):
    if patternScreenshots.match(filename):
        os.rename(os.path.join('dist', filename), os.path.join('dist', 'gAutoy.win32.exe'))

shutil.rmtree('build')
shutil.rmtree('gAutoy.egg-info')
