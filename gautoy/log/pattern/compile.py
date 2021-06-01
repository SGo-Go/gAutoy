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
@file         compile.py
@author       Sergiy Gogolenko
@copyright    Copyright 2015 by Sergiy Gogolenko.
@license      GPLv3

Compilation routines for gAutoy patterns 
######################################################################
"""
from __future__ import print_function

def compile(pattern, *args, **kwargs):
    if len(args) > 0 and isinstance(args[0], (list, tuple)) and not isinstance(args[0], basestring):
        import CFormatMessagePattern
        return CFormatMessagePattern.CFormatMessagePattern(pattern, *args, **kwargs)
    else:
        import REMessagePattern
        return REMessagePattern.SREMessagePattern(pattern, *args, **kwargs)

def get_log_and_pattern(pattern, *args, **kwargs):
    if len(args) >= 2 and isinstance(args[0], (list, tuple)):
        import CFormatMessagePattern
        return args[1], CFormatMessagePattern.CFormatMessagePattern(pattern, args[0], *args[2:], **kwargs)
    else:
        import REMessagePattern
        return args[0], REMessagePattern.SREMessagePattern(pattern, *args[1:], **kwargs)

def search(pattern, *args, **kwargs):
    log, pat = get_log_and_pattern(pattern, *args, **kwargs)
    return pat.search(log)

def match(pattern, *args, **kwargs):
    log, pat = get_log_and_pattern(pattern, *args, **kwargs)
    return pat.match(log)

def findall(pattern, *args, **kwargs):
    log, pat = get_log_and_pattern(pattern, *args, **kwargs)
    return pat.findall(log)

def finditer(pattern, *args, **kwargs):
    log, pat = get_log_and_pattern(pattern, *args, **kwargs)
    return pat.finditer(log)
