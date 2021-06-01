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
@file         setup.py
@author       Sergiy Gogolenko
@license      GPLv3

Setup script for making executable ``targetAssist``.
######################################################################
"""

from distutils.core import setup
import py2exe
setup(windows=[{
            "script":"app.py",
            "icon_resources": [(1, "targetAssist.ico")]
            }], 
      options={
        "py2exe":{
            'bundle_files': 1, 
            'compressed': True,
            
            "includes":["sip"],
            "dll_excludes": ["MSVCP90.dll", "HID.DLL", "w9xpopen.exe"],
            }
        },
      zipfile = None,
      )

# from distutils.core import setup
# import py2exe
# setup(windows=[{"script" : "app.py"}], options={"py2exe" : {"includes" : ["sip", "PyQt4"]}})
