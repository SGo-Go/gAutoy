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
@file         CallableProcess.py
@author       Sergiy Gogolenko
@license      GPLv3

CallableProcess class
######################################################################
"""
from __future__ import print_function
# import sys
import time
from gautoy.core.backend_selectors import get_callback_manager

class CallableProcess(object):
    def __init__(self, name, cbm = None):
        self.name       = str(name)
        self.cbm        = cbm or get_callback_manager()
        self.disconnect = False

    def __enter__(self):
        if not self.cbm.is_connected:
            self.cbm.connect(auto_close = False)
            self.disconnect = True
        self.cbm.set_process(self.name)
        p = getattr(self.cbm.processes, self.name)
        p._append_callbacks()
        return p

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.disconnect: self.cbm.disconnect()
