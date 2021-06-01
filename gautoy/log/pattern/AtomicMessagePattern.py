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
@file         AtomicMessagePattern.py
@author       Sergiy Gogolenko
@copyright    Copyright 2015 by Sergiy Gogolenko.
@license      GPLv3

Class that provides TraceClient functionality access via COM
######################################################################
"""
from __future__ import print_function
import re

from gautoy.core.config import get_option
from BaseMessagePattern import BaseMessagePattern,BaseMessagePattern_Match

class BaseAtomicMessagePattern(BaseMessagePattern):
    def __init__(self, *args, **kwargs):
        # regroup_dict = lambda d: dict(map(lambda kv_pair: (self.groupindexid(kv_pair[0]),kv_pair[1]), d.items()))
        # self._formatters = regroup_dict(formatters)
        # self._parsers    = regroup_dict(parsers)
        super(BaseAtomicMessagePattern, self).__init__(*args, **kwargs)

    @classmethod
    def compile(cls, pattern, *args, **kwargs):
        return cls(pattern, *args, **kwargs)

    # def formatter(self, group):
    #     return self._formatters.get(self.groupindexid( group),str)

    # def parser(self, group):
    #     return self._parsers.get(self.groupindexid(group), lambda x:x)

    @property
    def list(self):
        return [self]

    def wait(self, log_frame, timeout):
        """Blocks script until the pattern has been found/awaited in the 
        in the data stream of the logger or the ``timeout`` has lapsed.

        :param pattern:         contains logger supported re which is awaited
        :param timeout:         timeout specified in milliseconds
        :returns:               ``int`` if expected trace string has been received
                                otherwise ``None``
        :return endpos:         the line after the one that contains the message awaited
        """
        endpos = log_frame._wait_re(self.logger_pattern(log_frame), timeout)
        if endpos is None:
            raise RuntimeError('Pattern waiting timeout is lapsed') # TimeoutError
        return endpos

    def __repr__(self):
        return r"pattern(r'{0}')".format(self.pattern)

class BaseMessagePattern_MessageMatch(object):

    def __init__(self, msg_match, match):
        self._match     = msg_match

    @property
    def string(self):
        return self._match.string

    @property
    def lastgroup(self):
        return self._match.lastgroup

    @property
    def lastindex(self):
        return self._match.lastindex

    @property
    def endpos(self):
        return self._match.endpos

    def end(self):
        return self._match.end()

    def start(self):
        return self._match.start()

    def span(self):
        return self._match.span()

    def group(self, idx):
        return self._match.group(idx)

    def __getitem__(self, idx):
        return self.pattern.parser(idx)(self.group(idx))

    def __len__(self, idx):
        return len(self.string)

    def groups(self):
        return self._match.groups()

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

    def _repr_html_(self, line = True):
        from gautoy.core.output import i,b
        s = self.string
        bs, es = self.span()
        return i(s[:bs])+b(s[bs:es])+i(s[es:])

from MessageLine import BaseMessageLine
class BaseAtomicMessagePattern_Match(BaseMessageLine, BaseMessagePattern_Match):
    _message_match_text_type = BaseMessagePattern_MessageMatch

    def __init__(self, pattern, log_frame, line_no, msg_match, flags = 0):
        self._pattern   = pattern
        super(BaseAtomicMessagePattern_Match, self).__init__(line_no, log_frame = log_frame,
                                                             Message = self._message_match_text_type(msg_match, self))

    @property
    def Comment(self):
        return self._pattern._comment_func(self)

    @property
    def list(self):
        return [self]
    
    @property
    def pattern(self):
        return self._pattern

    def __getitem__(self, idx):
        return self.pattern.parser(idx)(self.Message.group(idx))

    def __str__(self):
        return self.Message.string

    def __repr__(self):
        return r"match(pos={0},msg='{1}')".format(self.pos, self.Message.string)

    @property
    def pos(self):
        return self.line

    @property
    def endpos(self):
        return self.line + 1

    # def __len__(self, idx):
    #     return self._message.groups()
