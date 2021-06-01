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
@file         MultilineMessagePattern.py
@author       Sergiy Gogolenko
@copyright    Copyright 2015 by Sergiy Gogolenko.
@license      GPLv3

MultilineMessagePattern
######################################################################
"""
from __future__ import print_function
import re

import BaseMessagePattern 
from   gautoy.core.config import get_option
from   BaseMessagePattern import BaseMessageSearchStructure

class MessagePatternSet(BaseMessageSearchStructure):
    def __init__(self, *args, **kwargs):
        self._patterns = list(args)

    @property
    def list(self):
        return self._patterns

    def specialize(self, *args, **kwargs):
        """
        Computes pattern where specified regex groups are replaced by input values.

        Input: 
                <group_0>= <value_0>, ..., <group_n-1>= <value_n-1>
        :returns:       specialized pattern
        :rtype:         BaseMessagePattern
        """
        if len(args):
            raise NotImplementedError("BaseMultilineMessagePattern does not support specialization with no-name args")
        import sets
        all_keys = sets.Set(kwargs.keys())
        patternSet = []
        for pat in self.list:
            keys = all_keys & pat.groupnames
            patternSet.append( pat.specialize(**{k: kwargs[k] for k in keys}) \
                               if len(keys) > 0 else pat )
        return MessagePatternSet(*patternSet)


    def wait(self, log_frame, timeout):
        """Blocks script until the pattern has been found/awaited in the 
        in the data stream of the logger or the ``timeout`` has lapsed.

        :param pattern:         contains logger supported re which is awaited
        :param timeout:         timeout specified in milliseconds
        :returns:               ``int`` if expected trace string has been received
                                otherwise ``None``
        :return endpos:         the line after the one that contains the message awaited
        """
        endpos = log_frame._wait_multi_re([pattern.logger_pattern(log_frame) for pattern in self.list],
                                          timeout, wait_all = False)
        if endpos is None:
            raise RuntimeError('Pattern waiting timeout is lapsed') # TimeoutError
        return endpos

    def finditer(self, log_frame, pos = 0, endpos = None):
        import heapq
        matches = [None]*len(self._patterns)
        pattern_iters = []
        search_front  = [] # heap with pairs (pos-next-search, pattern-no)
        for i, pattern in enumerate(self._patterns):
            pattern_iters.append(pattern.finditer(log_frame, pos = pos, endpos = endpos))
            try:
                matches[i] = next(pattern_iters[i])
                heapq.heappush(search_front, (matches[i].endpos, i))
            except StopIteration: pass
        while len(search_front) > 0:
            pos, pattern_no = heapq.heappop(search_front)
            yield(matches[pattern_no])
            try:
                log_frame.start_line = pos
                matches[pattern_no] = next(pattern_iters[pattern_no])
                heapq.heappush(search_front, (matches[pattern_no].endpos, pattern_no))
            except StopIteration: pass

    def __repr__(self):
        return " | \n".join(map(repr,self._patterns))

    def __ior__(self, pattern):
        from MessagePatternSet import MessagePatternSet
        from AtomicMessagePattern import BaseAtomicMessagePattern
        from MultilineMessagePattern import BaseMultilineMessagePattern
        if   isinstance(pattern, MessagePatternSet):
            self._patterns.extend(pattern._patterns)
        elif isinstance(pattern, (BaseAtomicMessagePattern, BaseMultilineMessagePattern)):
            self._patterns.append(pattern)
        return self

    def __and__(self, pattern):
        ret  = MessagePatternSet(*self.list)
        ret &= pattern
        return ret

    def __iand__(self, pattern):
        import copy
        from MessagePatternSet import MessagePatternSet
        from AtomicMessagePattern import BaseAtomicMessagePattern
        from MultilineMessagePattern import BaseMultilineMessagePattern
        if   isinstance(pattern, MessagePatternSet):
            ret = MessagePatternSet()
            for pat in pattern.list:
                ret |= MessagePatternSet(*self.list) & pat
            patterns = ret.list
        elif isinstance(pattern, (BaseAtomicMessagePattern, BaseMultilineMessagePattern)):
            patterns = []
            for pat in self._patterns:
                new_pat  = BaseMultilineMessagePattern(pat.list)
                new_pat &= pattern
                patterns.append(new_pat)
        self._patterns = patterns
        return self
