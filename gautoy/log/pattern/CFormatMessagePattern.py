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
@file         CFormatMessagePattern.py
@author       Sergiy Gogolenko
@copyright    Copyright 2015 by Sergiy Gogolenko.
@license      GPLv3

Classes that implement CFormat patterns for log-search
######################################################################
"""
from __future__ import print_function
import REMessagePattern

class CFormatMessagePattern(REMessagePattern.SREMessagePattern):
    def __init__(self, pattern, names, flags = 0, **kwargs):
        import re
        reCFormatter = re.compile(r'(^|[^\%])(?P<formatter>\%(\+|\-| |#|0)?\d*\.?\d*(s|d|i|u|x|X|f|F|e|E|g|G|p))')
        self.cpattern = pattern

        cpattern = pattern
        for ch in list(r'\[]().{}?-+'):
            cpattern = cpattern.replace(ch, r"\{0}".format(ch))

        patternRE = ''
        cformatStrings = []
        start_pos = 0
        for i, name in zip(xrange(len(names)), names):
            m = reCFormatter.search(cpattern, start_pos)
            if m:
                formatter = m.group('formatter')
                formatter = {'p': m.group('formatter')[:-1] + 'x'}.get(m.group('formatter')[-1], formatter)
                
                cformatStrings.append(formatter)
                # {'d':r'(\+|\-)?\d+', 'i':r'(\+|\-)?\d+',
                #  'x':r'(\+|\-)?[0-9a-f]+','X':r'(\+|\-)?[0-9A-F]+'}.
                patternRE += r'{0}(?P<{1}>{2})'.format(
                    cpattern[start_pos:m.end()-len(formatter)], name,
                    {'d':r'\-?\d+', 'i':r'\-?\d+',
                     'x':r'\-?[0-9a-f]+','X':r'\-?[0-9A-F]+'}.
                    get(formatter[-1], r'.*'))
                start_pos = m.end()
            else:
                if i + 1 != len(names):
                    raise ValueError(r'CFormat string has {0} formatters, but {1} names are given'.format(i+1, len(names)))
                break
        if reCFormatter.search(cpattern, start_pos):
            raise ValueError(r'Need more names to cover CFormat("{0}")'.format(cpattern[start_pos:]))
        patternRE += cpattern[start_pos:]

        super(CFormatMessagePattern, self).__init__(patternRE, flags = flags,
                                                    parsers     = dict(zip(names, map(lambda f: {'d': int, 'i':int,
                                                                                                 'x': lambda x:int(x,16), 'X': lambda x:int(x,16),
                                                                                                 'f':float, 'f':float,
                                                                                                 'e':float, 'E':float}.get(f[-1], str), cformatStrings))),
                                                    formatters  = dict(zip(names, map(lambda f: lambda x: f % x, cformatStrings))),
                                                    **kwargs)
