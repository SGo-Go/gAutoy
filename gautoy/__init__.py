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
@file         __init__.py
@author       Sergiy Gogolenko
@license      GPLv3

Root init-file.
######################################################################
"""

from __future__ import absolute_import

import sys
if sys.version_info[:2] < (2, 7):
    m = "Python 2.7 or later is required for gAutoy (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

# Release data
from gautoy import release

__author__  = '%s <%s>\n' % (release.authors['Gogolenko'])
__license__ = release.license
__date__    = release.date
__version__ = release.version

# Start with init-time option registration
import gautoy.core.config_init
from   gautoy.core              import converter
from   gautoy.core.backend_selectors import new_target,get_target,\
    get_logger,get_callback_manager,get_callbacks
from   gautoy.core.output       import init_printing #,pprint,warning,error
# import gautoy.core.output.pprint  as pprint
# import gautoy.core.output.warning as warning
# import gautoy.core.output.error as error

import gautoy.target

import gautoy.log
from   gautoy.log               import pattern

import gautoy.cbm
from   gautoy.cbm               import CallableProcess

import gautoy.tools.traceclient

import gautoy.domain.maps
from   gautoy.domain.maps       import GoogleMaps

import gautoy.notebook 
#from   gautoy.notebook          import gautoy_bash,gautoy_screenshot
