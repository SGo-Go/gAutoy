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
@file         PatternHandleMeta.py
@author       Sergiy Gogolenko
@copyright    Copyright 2015 by Sergiy Gogolenko.
@license      GPLv3

Class that provides TraceClient functionality access via COM
######################################################################
"""
from __future__ import print_function
import re

from gautoy.core.config import get_option


def handler(pattern, *args, **kwargs):
    # import functools
    from gautoy.log.pattern.compile import compile
    def wrap(funcobj):
        funcobj.__handlepattern__ = compile(pattern, *args, **kwargs)  \
                                    if isinstance(pattern, basestring) \
                                       else pattern
        return funcobj
    return wrap

def patternic(cls):
    """Class decorator for creating a class with PatternicMeta metaclass."""
    orig_vars = cls.__dict__.copy()
    orig_vars.pop('__dict__', None)
    orig_vars.pop('__weakref__', None)
    for slots_var in orig_vars.get('__slots__', ()):
        orig_vars.pop(slots_var)
    return PatternicMeta(cls.__name__, cls.__bases__, orig_vars)

class PatternicMeta(type):
    def __new__(mcls, name, bases, namespace):

        # Fix bases (make _Patternic if object)
        if not any(issubclass(base, _Patternic) for base in bases):
            if object in bases:
                bases = tuple([_Patternic if base is object else base
                               for base in bases])
            else:
                bases = bases + (_Patternic,)
        
        cls = super(PatternicMeta, mcls).__new__(mcls, name, bases, namespace)

        # Gether patternic methods from original class
        functions = dict( ( name, value.__handlepattern__) for name, value in namespace.items() \
                          if getattr(value, "__handlepattern__", False) )

        # Collect patternic methods from base classes
        for base in bases:
            for pat_id, patobj_pair in getattr(base, "__gautoy_patternmethods__", {}).items():
                pat, names = patobj_pair
                for name in names:
                    if not (name in functions): # if new "patternic" method 
                        patobj = getattr( getattr(cls, name, None), # get funcobj
                                          "__handlepattern__", False )
                        if patobj: functions[name] = patobj

        # Register patternmethods in class type
        patternmethods = {}
        if len(functions) > 0:
            for name, pat in functions.items():
                pat_id = id(pat)
                if pat_id in patternmethods:
                    patternmethods[pat_id][1].append(name)
                else:
                    patternmethods[pat_id] = pat, [name]

            from MessagePatternSet import MessagePatternSet
            patterns = MessagePatternSet(*(pat_set[0] for pat_id, pat_set in patternmethods.items()))
            cls.__gautoy_patternset__ = patterns


        cls.__gautoy_patternmethods__ = patternmethods

        return cls

class _Patternic(object):
    # def __new__(cls, *args, **kwds):
    #     is_patternic = cls.__dict__.get("__gautoy_patternmethods__")
    #     if is_patternic: print('Patternic class {0}'.format(cls.__name__))
    #     return super(_Patternic, cls).__new__(cls, *args, **kwds)

    def walk(self, log_frame, pos = 0, endpos = None, log_files = None, log_file = None, **kwargs):
        patterns = getattr(type(self), '__gautoy_patternset__' , None)
        if patterns:
            files = [None]
            if log_files:
                if isinstance(log_files, basestring):
                    import glob
                    files = glob.glob(log_files)
                else: files = log_files
            elif log_file and isinstance(log_file, basestring): files = [log_file]
            for filename in files:
                if filename: log_frame.load(filename)
                for r in patterns.finditer(log_frame, pos = pos, endpos = endpos, **kwargs):
                    pat_id = id(r.pattern)
                    for funcname in self.__gautoy_patternmethods__[pat_id][1]:
                        getattr(self, funcname)(r)
                    # self.__dict__[funcname](self, r)
        return self

