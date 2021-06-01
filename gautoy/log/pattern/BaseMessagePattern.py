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

class BaseMessageSearchStructure(object):

    @property
    def list(self):
        """Return simple patterns from searcheable structure as a patterns list

        :returns:       List of patterns
        :rtype:         list
        """
        raise NotImplementedError("Pattern of type {0} does not support this method".format(type(self)))

    def len(self):
        return len(self.list)

    def wait(self, log_frame, timeout):
        """Blocks script until the pattern has been found/awaited in the 
        in the data stream of the logger or the ``timeout`` has lapsed.

        :param pattern:         contains logger supported re which is awaited
        :param timeout:         timeout specified in milliseconds
        :returns:               ``int`` if expected trace string has been received
                                otherwise ``None``
        :return endpos:         the line after the one that contains the message awaited
        """
        raise NotImplementedError('Pattern of type {0} does not support wait method'.format(type(self)))

    def finditer(self, log_frame, pos = 0, endpos = None):
        """Return an iterator yielding MatchObject instances over all matches for the pattern in ``log_frame``. 
        The ``log_frame`` is scanned top-to-down, and matches are returned in the order found. 

        :param log_frame: 
        :param pos: 
        :param endpos: 
        :returns: 
        :rtype: 
        """
        raise NotImplementedError("Pattern of type {0} does not support this method".format(type(self)))

    def findall(self, log_frame, pos = 0, endpos = None):
        """Return all matches of pattern in ``log_frame``, as a list of matches. 
        The ``log_frame`` is scanned top-to-down, 
        and matches are returned in the order found.

        :param log_frame: 
        :param pos: 
        :param endpos: 
        :returns: 
        :rtype: 
        """
        from MessageLine import MessageLineList
        ret_list = MessageLineList()
        for r in self.finditer(log_frame, pos = pos, endpos = endpos):
            ret_list.append(r)
        return ret_list

    def match(self, log_frame, pos = 0, endpos = None):
        """If message at the line ``pos`` in ``log_frame`` matches pattern, 
        return a corresponding MatchObject instance. 
        Return None if the message does not match the pattern.

        :param log_frame: 
        :param pos: 
        :param endpos: 
        :returns: 
        :rtype: 
        """
        try:
            match = next(self.finditer(log_frame, pos = pos, endpos = endpos))
            if(pos == match.pos): return match
        except StopIteration: return

    def search(self, log_frame, pos = 0, endpos = None):
        """Scan through ``log_frame`` looking for the first location 
        where the pattern produces a match, 
        and return a corresponding MatchObject instance. 
        Return None if no position in the string matches the pattern.

        :param log_frame: 
        :param pos: 
        :param endpos: 
        :returns: 
        :rtype: 
        """
        try:   return next(self.finditer(log_frame, pos = pos, endpos = endpos))
        except StopIteration: return
        
    def walk(self, log_frame, pos = 0, endpos = None, **kwargs):
        """Walk through the ``log_frame`` and 
        launch pattern's callback (with match as input) for each pattern match.

        :param log_frame: 
        :param pos: 
        :param endpos: 
        :returns: 
        :rtype: 
        """
        for r in self.finditer(log_frame, pos = pos, endpos = endpos, **kwargs):
            r.pattern._callback(r)


    def __call__(self, *args, **kwargs):
        """
        Computes pattern where specified regex groups are replaced by input values.

        Input: 
                <group_0>, <value_0>, ..., <group_k-1>, <value_k-1>, 
                <group_k> = <value_k>, ..., <group_n> = <value_n>
        :returns:       specialized pattern
        :rtype:         BaseMessagePattern
        """
        return self.specialize(*args, **kwargs)

    def specialize(self, *args, **kwargs):
        """
        Computes pattern where specified regex groups are replaced by input values.

        Input: 
                <group_0>, <value_0>, ..., <group_k-1>, <value_k-1>, 
                <group_k>= <value_k>, ..., <group_n-1>= <value_n-1>
        :returns:       specialized pattern
        :rtype:         BaseMessagePattern
        """
        raise NotImplementedError("Pattern of type {0} does not support this method".format(type(self)))

    @property
    def groupnames(self):
        l = self.list
        if len(l) > 1:
            s = l[0].groupnames
            for pat in l[1:]: s |= pat.groupnames
            return s
        else:
            raise NotImplementedError("Pattern of type {0} does not support groupnames method".format(type(self)))
            
    def __or__(self, pattern):
        from MessagePatternSet import MessagePatternSet
        from AtomicMessagePattern import BaseAtomicMessagePattern
        from MultilineMessagePattern import BaseMultilineMessagePattern
        if   isinstance(pattern, MessagePatternSet):
            args = [self] + pattern.list
        elif isinstance(pattern, (BaseAtomicMessagePattern, BaseMultilineMessagePattern)):
            args = [self, pattern]
        return MessagePatternSet(*args)

    def __ior__(self, pattern):
        raise NotImplementedError("Pattern of type {0} does not support this method".format(type(self)))

    def __add__(self, pattern):
        return self.__or__(pattern)

    def __iadd__(self, pattern):
        return self.__ior__(pattern)

    def __and__(self, pattern):
        raise NotImplementedError("Pattern of type {0} does not support this method".format(type(self)))

    def __iand__(self, pattern):
        raise NotImplementedError("Pattern of type {0} does not support this method".format(type(self)))

    def __mul__(self, pattern):
        return self.__and__(pattern)

    def __imul__(self, pattern):
        return self.__iand__(pattern)

    def __pow__(self, pattern):
        raise NotImplementedError("Pattern of type {0} does not support this method".format(type(self)))

    def __ipow__(self, pattern):
        raise NotImplementedError("Pattern of type {0} does not support this method".format(type(self)))

    def __repr__(self):
        raise NotImplementedError("Pattern of type {0} does not support this method".format(type(self)))

class BaseMessagePattern(BaseMessageSearchStructure):

    def call(self, callback):
        """
        Assigns callback to pattern
        """
        import copy
        pat = copy.copy(self)
        pat._callback = callback
        return pat

    def logger_pattern(self, log_frame):
        raise NotImplementedError("Pattern of type {0} does not support this method".format(type(self)))

    def __and__(self, pattern):
        from MessagePatternSet import MessagePatternSet
        from AtomicMessagePattern import BaseAtomicMessagePattern
        from MultilineMessagePattern import BaseMultilineMessagePattern
        if   isinstance(pattern, MessagePatternSet):
            return MessagePatternSet(*[BaseMultilineMessagePattern(*(self.list + pat.list)) for pat in pattern.list])
        elif isinstance(pattern, (BaseAtomicMessagePattern, BaseMultilineMessagePattern)):
            return BaseMultilineMessagePattern(*(self.list + pattern.list))

    def __pow__(self, p):
        if isinstance(p, (int,long)) and p > 0:
            if isinstance(self, BaseMessagePattern):
                from MultilineMessagePattern import BaseMultilineMessagePattern
                return BaseMultilineMessagePattern(*(self.list*p))
            else:
                raise NotImplementedError( "Cannot raise {0} to powers".format(type(self)) )
        else:
            raise NotImplementedError( "{0} patterns can be raisen only in "\
                                       "positive integer powers".format(type(self)) )

class BaseMessagePattern_Match(object):

    @property
    def pattern(self):
        raise NotImplementedError()

    def __getitem__(self, idx):
        raise NotImplementedError()

    def __getattr__(self, idx):
        return self.__getitem__(idx)

    @property
    def pos(self):
        raise NotImplementedError()

    @property
    def endpos(self):
        raise NotImplementedError()

    # def to_html_row(self):
    #     raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return r'match(pos={0},endpos={1})'.format(self.pos, self.endpos)

    def _repr_html_(self):
        raise NotImplementedError()
