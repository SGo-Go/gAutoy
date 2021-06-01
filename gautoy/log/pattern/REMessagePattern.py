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
@file         BaseMessagePattern.py
@author       Sergiy Gogolenko
@copyright    Copyright 2015 by Sergiy Gogolenko.
@license      GPLv3

Class that provides TraceClient functionality access via COM
######################################################################
"""
from __future__ import print_function
import re

from gautoy.core.config import get_option

from AtomicMessagePattern import BaseAtomicMessagePattern,BaseAtomicMessagePattern_Match
class SREMessagePattern(BaseAtomicMessagePattern):
    _message_match_type = BaseAtomicMessagePattern_Match

    def __init__( self, pattern, flags = 0,
                  parsers = {}, formatters = {}, comment_func =  lambda match: r'' ):
        # print(pattern)
        self._re         = re.compile(pattern, flags)
        self.flags       = flags

        regroup_dict = lambda d: dict(map(lambda kv_pair: (self.groupindexid(kv_pair[0]),kv_pair[1]), d.items()))
        self._formatters = regroup_dict(formatters)
        self._parsers    = regroup_dict(parsers)
        # print 
        self._comment_func = comment_func
        super(SREMessagePattern, self).__init__()#(parsers = parsers, formatters = formatters)

    def formatter(self, group):
        return self._formatters.get(self.groupindexid( group),str)

    def parser(self, group):
        return self._parsers.get(self.groupindexid(group), lambda x:x)

    def specialize(self, *args, **kwargs):
        """
        Computes pattern where specified regex groups are replaced by input values.

        Input: 
                <group_0>, <value_0>, ..., <group_k-1>, <value_k-1>, 
                <group_k>= <value_k>, ..., <group_n-1>= <value_n-1>
        :returns:       specialized pattern
        :rtype:         BaseMessagePattern

        """
        if len(args) % 2 != 0:
            raise ValueError(r'Odd number of arguments: expect input with: <group-name>, <value>')

        group_no = lambda group: ( group if isinstance( group, (int, long) ) else self.groupindex[group]) - 1

        # Cast input parameters to array
        params = [None]*self.groups
        for group, value in zip(args[::2], args[1::2]) + kwargs.items():
            params[group_no(group)] = value

        s = self._re.pattern
        for group_no in xrange(self.groups-1,-1,-1):
            if params[group_no] is not None:
                m = re.match(r'(?P<beg>^[^\(]*([^\(]*(\\\()*\(){{{0}}})(?P<rest>.*)$'.format(group_no+1), s)
                beg = m.group('beg')#[:-1]
                end = m.group('rest')
                if len(beg) >= 2 and beg[-2] == '\\' and len(end) > 0: # @didry hack
                    beg = beg + end[0]
                    end = end[1:]
                num_braces, idx = 0, 0
                while num_braces >= 0:
                    if   end[idx] == '(': num_braces += 1
                    elif end[idx] == ')': num_braces -= 1
                    idx += 1
                    if idx > len(end):
                        raise ValueError('Incompatible request')
                s  = beg
                if end[0] == '?' and end[1] == 'P' and end[2] == '<': # insert group name if have one
                    k = end.find('>')
                    s += end[:k+1]
                s += self.formatter(group_no + 1)(params[group_no])
                s += end[idx-1:]
        # print(s)
        return SREMessagePattern.compile(s, flags = 0,
                                         # parsers        = self._parsers,
                                         # formatters     = self._formatters,
                                         comment_func   = self._comment_func) 
    
    @property
    def pattern(self):
        return self._re.pattern

    @property
    def re(self):
        return self._re.pattern

    def logger_pattern(self, log_frame):
        return log_frame.to_supported_re(self._re)

    @property
    def groups(self):
        return self._re.groups

    @property
    def groupnames(self):
        import sets
        return sets.Set(self.groupindex.keys())

    @property
    def groupindex(self):
        return self._re.groupindex

    def groupindexid(self, key):
        return self._re.groupindex.get(key,key)

    def finditer(self, log_frame, pos = 0, endpos = None):
        pattern = self.logger_pattern(log_frame)

        ret_val = log_frame._find_first_by_RE(pattern, start_line = pos, wait_all = False)
        _endpos = endpos or len(log_frame) + 1
        if ret_val and ret_val[0] < _endpos:
            line_no, msg = ret_val
            match = self._re.search(msg)
            if match: yield(self._message_match_type(self, log_frame, line_no, match))
            while ret_val:
                ret_val = log_frame._find_next_by_RE(pattern, wait_all = False)
                if ret_val and line_no < _endpos:
                    line_no, msg = ret_val
                    match = self._re.search(msg)
                    if match: yield(self._message_match_type(self, log_frame, line_no, match))
                else: break
