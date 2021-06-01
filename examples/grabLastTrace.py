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
@file         grabLastTrace.py
@author       Sergiy Gogolenko
@license      GPLv3

Grabs last trace from CNLogger

Example of use::

   python ./grabLastTrace.py [file_name]

######################################################################
"""

import gautoy,os,sys
logger = gAutoy.traceclient.CNLogger()
logger.grab_trace( sys.argv[1] if len(sys.argv) > 1 else os.getcwd() )
