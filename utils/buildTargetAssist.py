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
@file         buildTargetAssist.py
@author       Sergiy Gogolenko
@license      GPLv3

Build targetAssist.
######################################################################
"""

import os,shutil,re

dest_dir = os.path.join(os.pardir, os.pardir, 'dist')

os.chdir('targetAssist')
os.system('python setup.py install')
os.system('python setup.py py2exe')

if not os.path.exists(dest_dir): os.makedirs(dest_dir)
if os.path.exists(os.path.join(dest_dir, 'TargetAssist.exe')):
    os.remove(os.path.join(dest_dir, 'TargetAssist.exe'))
os.rename(os.path.join('dist', 'app.exe'), os.path.join(dest_dir, 'TargetAssist.exe'))
shutil.rmtree('build')
shutil.rmtree('dist')

if not os.path.exists(os.path.join(dest_dir, 'targetAssist.json')): 
    shutil.copy('targetAssist.json', dest_dir)

# shutil.copytree(os.path.join(os.pardir, os.pardir, 'third-party'), dest_dir)
