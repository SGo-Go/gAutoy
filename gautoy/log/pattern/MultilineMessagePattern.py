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

from gautoy.core.config import get_option
from BaseMessagePattern import BaseMessagePattern,BaseMessagePattern_Match

class BaseMultilineMessagePattern(BaseMessagePattern):
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
        return BaseMultilineMessagePattern(*patternSet)

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
                                          timeout, wait_all = True)
        if endpos is None:
            raise RuntimeError('Pattern waiting timeout is lapsed') # TimeoutError
        return endpos

    def finditer(self, log_frame, pos = 0, endpos = None):
        if len(self._patterns) < 1: return

        # Compute pattern iterators and initial matches
        pattern_iters = [self._patterns[0].finditer(log_frame, pos = pos, endpos = endpos)]
        try:
            matches_front = [next(pattern_iters[0])]
        except StopIteration: return
        for pattern in self._patterns[1:]:
            # if not matches_front[-1]: return
            pattern_iter = pattern.finditer(log_frame, pos = matches_front[-1].endpos, endpos = endpos)
            pattern_iters.append(pattern_iter)
            try:
                matches_front.append(next(pattern_iter))
            except StopIteration: return
        # if not matches_front[-1]: return

        # Loop over matches
        validFront = True
        from gautoy.core.output import pprint
        while validFront:
            # Tune match to the nearest neighbours
            matches_yeild = [matches_front[-1]]
            for i in xrange(len(pattern_iters)-2,-1,-1):
                prev_match_pos = matches_yeild[0].pos

                pattern_iter = pattern_iters[i]
                next_match   = matches_front[i]
                match        = matches_front[i]
                log_frame.start_line = match.endpos
                while next_match and next_match.endpos <= prev_match_pos:
                    try:                        
                        new_match = next(pattern_iter)
                        # pprint(new_match)
                    except StopIteration:
                        validFront = False
                        match = next_match
                        break
                    match, next_match = next_match, new_match
                matches_front[i] = next_match
                matches_yeild.insert(0, match)

            # Return result
            yield(BaseMultilineMessagePattern_Match(self, matches_yeild))
            # Prepare new match front
            if validFront:
                for i, pattern_iter in enumerate(pattern_iters[1:], 1):
                    if matches_front[i].pos <= matches_front[i-1].endpos:
                        log_frame.start_line = matches_front[i-1].endpos
                        try:
                            matches_front[i] = next(pattern_iter)
                            # pprint(matches_front[i])
                        except StopIteration: return
                        
    def __repr__(self):
        return r"&".join(map(repr,self._patterns))

    def __iand__(self, pattern):
        from MessagePatternSet import MessagePatternSet
        from AtomicMessagePattern import BaseAtomicMessagePattern
        from MultilineMessagePattern import BaseMultilineMessagePattern
        if   isinstance(pattern, MessagePatternSet):
            raise TypeError(r'Cannot convert type {0} to pattern set: need it if do &= and *= operations'.format(type(self)))
        elif isinstance(pattern, (BaseAtomicMessagePattern, BaseMultilineMessagePattern)):
            self._patterns.extend(pattern.list)
        return self

class BaseMultilineMessagePattern_Match(BaseMessagePattern_Match):
    def __init__(self, pattern, lst = None):
        self._pattern   = pattern
        self._matches = lst or []
        super(BaseMessagePattern_Match, self).__init__()


    @property
    def pattern(self):
        return self._pattern

    @property
    def list(self):
        return self._matches

    def __iter__(self):
        for x in self._matches: yield(x)

    @property
    def endpos(self):
        return self.list[-1].line + 1

    @property
    def pos(self):
        return self.list[0].line

    # def __len__(self, idx):
    #     return self._message.groups()

    def to_html_row(self):
        out = ''
        for x in self.list: out += x.to_html_row()
        return out

    def __getitem__(self, idx):
        if isinstance(idx, basestring):
            for match in self.list:
                if idx in match.pattern.groupindex.keys():
                    return match[idx]
            raise IndexError( r'No group {0} in match'.format(idx) )
        elif isinstance(idx, (tuple, list)) and len(idx) == 2:
            row, key = idx
            return self.list[row][key]
        elif isinstance(idx, (int, long)):
            return self.list[idx]
        else:
            raise IndexError( r'Unexpected index type {0}'.format(type(idx)) )
    
    def _repr_html_(self):
        from gautoy.core.output import table
        return r'<small>{0}</small>'.format(table(self.to_html_row(), style="width:100%"))

    def __str__(self):
        return self[0].Message.string

    def __repr__(self):
        return r"match(pos={0},msg='{1}')".format(self.pos, self[0].Message.string)
