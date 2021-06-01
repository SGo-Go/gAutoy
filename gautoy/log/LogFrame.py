#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
..
   ###################################################################

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

   ###################################################################
   @package      gAutoy
   @file         LogFrame.py
   @author       Sergiy Gogolenko
   @license      GPLv3

Classes that provide wraps to TraceClient API that work with logs
######################################################################
"""
from __future__ import print_function

import datetime
import numpy
import pandas

# from abc import ABCMeta,abstractmethod,abstractproperty

class LogFrame(object):
    """
    Class that customizes access to logger
    """
    # __metaclass__ = ABCMeta

    @classmethod
    def normalize_attribute_name(cls, name):
        if name == '?': return 'Type'
        else:
            return name.replace(' ', '')
    
    # @abstractmethod
    def __call__(self, logfile, scopefile = None):
        """Load the specified log file.

        :param scopefile: optional Scope-File
        """
        self.load(logfile, scopefile)
        return self

    # @abstractmethod
    def __len__(self):
        """number of messages in log
        """

    # @abstractmethod
    def wait(self, pattern, timeout, #line_no, remaining,
             regexp = True, wait_all = False):
        """After the function call, the test script is blocked 
        until the specified string ``pattern`` has been found 
        in the data stream of the TraceClient or the ``timeout`` has lapsed.
        ``WaitForTraceMsg()`` is a simple form of the function ``WaitForMultipleObjects()``.
        The function is identical except that 
        the single function just waits for one TraceString. 

        :param pattern:     contains the Trace String which is awaited
        :param timeout:         timeout specified in milliseconds
        :param regexp:          specifies whether a regular expression is awaited
        :param wait_all:        specifies whether the receipt of one or all strings is awaited
        :returns:               ``True`` if expected Trace String has been received
                                otherwise timeout
        :rtype:                 ``bool``, ``int``, ``str``
        :return line_no:        the line number that contains the Trace output, 
                                which has triggered the event.
        :return remaining:      next line break is returned to the script

        """

    def finditer(self, traceString, start_line = 0, regexp = True, find_all = False, timeout = 100):
        self.start_line = start_line
        ret_val = True
        while ret_val:
            ret_val, line_no, remaining = self.wait(traceString, timeout = timeout, regexp = True, wait_all = find_all)
            if ret_val: yield(line_no, remaining)

    # @abstractproperty
    def line(self):
        """current line in logger
        """

    # @abstractmethod
    def reset_start_line(self):
        """Set the end line for the backwards search to the current line. 
        Use this function to avoid that your wait() searches traces 
        not belong to your test simulation.
        """

    @property
    def start_line(self):
        """current line in logger (same to line)
        """
        return self.line
        
    # @abstractmethod
    def start_line(self, value):
        """Set the start line to the given line number for the search to start with.

        :param value:  start line
        """


    # @abstractmethod
    def __getitem__(self, lineno):
        """Get message attribute value
        
        :param idx:     idx = lineNo
                        Index of the message, to select the message.
                        The column you want to get. 
                        (Column names: "?", "TimeStamp", "Host", 
                        "Receiving Time"/"Logger Receiving Time", "Thread", 
                        "Process", "Scope", "Console", "Message")
        :returns:       the attribute value to return
        :rtype:         str
        
        """

    # @abstractmethod
    def attribute(self, attribute, line_from, line_to = None, step = None):
        """Get message attribute value

        :param attribute: the column you want to get
                          (Column names: "?", "TimeStamp", "Host", 
                          "Receiving Time"/"Logger Receiving Time", "Thread", 
                          "Process", "Scope", "Console", "Message")
        :param line_from: line number of the first message to select
        :param line_to:   line number of the last message to select
        :returns:         the attribute value to return
        :rtype:           str

        """

    # @abstractproperty
    def is_loading_scopes(self):
        """scopes load is available
        """
        

    # @abstractmethod
    def load(self, logfile, scopefile = None):
        """
        Load the specified Log file using an additional, optional Scope-File.

        :param scopefile: optional Scope-File
        """

    # @abstractmethod
    def save(self, filename, version = 1):
        """
        Stores the Trace outputs persistently in a file.

        :param version: version number for the Trace file format (allowed values are: 1, 2, 3; default: 1)
        :returns: specifies whether the file was successfully saved

        """

    # @abstractmethod
    def clear(self):
        """
        Clear the display area of the TraceClient.
        """

    # @abstractmethod
    def comment(self, comment_string):
        """
        Inserts a comment into the Trace output
        """

    # @abstractmethod
    def clear_filters(self):
        """
        Clear all column filters.
        """

    # @abstractmethod
    def save_scope(self, filename, version = 0x00010100):
        """
        Save the scopes under the given filename.

        :param version: File version:
        VERSION_1_0_0 = 0x00010000L
        VERSION_1_1_0 = 0x00010100L
        """

    # @abstractmethod
    def load_scope(self, filename, version = 0x00010100):
        """
        Load the scopes from the given filename.
        """

    # @abstractmethod
    def scope_count(self, processname):
        """
        Return the scope count for the given process.
        """

    # @abstractmethod
    def to_pandas(self):
        """Get recent TraceClient logs as ``pandas`` ``DataFrame``
        
        :returns:         ``pandas`` ``DataFrame``
        :rtype:           DataFrame
        
        .. note:: 
        
            This is a dirty hack rather than a precise implementation. 
            It gets data from clipboard.
            Should be replaced in the future.

        """

    @property
    def backend(self):
        return '.'.join(self.__module__.split('.')[2:-1])
        
    def __repr__(self):
        return "{0} logger".format(self.backend)

    def _repr_html_(self):
        return "<code>{1} <b>logger</b> (lines:<i>{0}</i>)</code>".format(self.line, self.backend)


    def __getitem__(self, lineno):
        """Get message attribute value
        
        :param idx:     idx = lineNo
                        Index of the message, to select the message.
                        The column you want to get. 
                        (Column names: "?", "TimeStamp", "Host", 
                        "Receiving Time"/"Logger Receiving Time", "Thread", 
                        "Process", "Scope", "Console", "Message")
        :returns:       the attribute value to return
        :rtype:         str
        
        """
        msg = []
        for attribute in map(lambda attr:getattr(self, attr).name, self._attributes):
            val = self.get_attr(lineno, attribute)
            if val is None:
                raise IndexError("Cannot get attribute '{1}' in line {0}".format(lineno, "Message"))
            else:
                msg.append(val)
        return tuple(msg)

    def __getitem__(self, lineno):
        """Get message with all attributes
        
        :param idx:     idx = lineNo
                        Index of the message, to select the message.
                        The column you want to get. 
                        (Column names: "?", "TimeStamp", "Host", 
                        "Receiving Time"/"Logger Receiving Time", "Thread", 
                        "Process", "Scope", "Console", "Message")
        :returns:       the attribute value to return
        :rtype:         str
        
        """
        msg = []
        for attribute in map(lambda attr:getattr(self, attr).name, self._attributes):
            val = self.get(lineno, attribute)
            if val is None:
                raise IndexError("Cannot get attribute '{1}' in line {0}".format(lineno, "Message"))
            else:
                msg.append(val)
        return tuple(msg)

    # @abstractmethod
    def get(self, line_no, attribute, default = None):
        """Get message attribute value

        :param attribute: the column you want to get
                          (Column names: "?", "TimeStamp", "Host", 
                          "Receiving Time"/"Logger Receiving Time", "Thread", 
                          "Process", "Scope", "Console", "Message")
        :param line_no:   line number
        :returns:         the attribute value to return
        :rtype:           str

        """
        raise NotImplementedError('Logger {0} does not support attribute access'.format(type(self)))

    def attribute(self, attribute, line_from, line_to = None, step = None):
        """Get message attribute value

        :param attribute: the column you want to get
                          (Column names: "?", "TimeStamp", "Host", 
                           "Receiving Time"/"Logger Receiving Time", "Thread", 
                           "Process", "Scope", "Console", "Message")
        :param line_from: line number of the first message to select
        :param line_to:   line number of the last message to select
        :returns:         the attribute value to return
        :rtype:           str

        """
        if line_to is None:
            val = self.get(line_to, attribute)
            if val is None:
                raise IndexError("Cannot get attribute '{1}' in line {0}".format(line_from, attribute))
        else:
            result = []
            for lineNo in xrange(line_from, line_to):
                val = self.get(lineNo, attribute)
                if val is None:
                    raise IndexError("Cannot get attribute '{1}' in line {0}".format(lineNo, attribute))
                else: result.append(val)
        return result

    # @abstractmethod
    def _find_first_by_RE(self, pattern, start_line = 0, wait_all = False):
        """API for pattern search: finds first pattern match

        :param pattern:         pattern regexp
        :param wait_all: 
        :returns: 
        :rtype: 

        """
        raise NotImplementedError('Logger {0} does not support pattern search'.format(type(self)))

    # @abstractmethod
    def _find_next_by_RE(self, pattern, wait_all = False):
        """API for pattern search: finds next pattern match after current logger line

        :param pattern:         pattern regexp
        :param wait_all: 
        :returns: 
        :rtype: 

        """
        raise NotImplementedError('Logger {0} does not support pattern search'.format(type(self)))

    # @abstractmethod
    def _find_first_multi_by_RE(self, patterns, start_line = 0):
        """API for pattern search: finds first multi-line pattern match

        :param pattern:         pattern regexp
        :returns: 
        :rtype: 
        """
        self.start_line = start_line
        return self._find_next_multi_by_RE(patterns)


    # @abstractmethod
    def _find_next_multi_by_RE(self, patterns):
        """API for pattern search: finds next multi-line pattern match after current logger line

        :param pattern:         pattern regexp
        :returns: 
        :rtype: 
        """
        ret_val = self._find_next_by_RE(patterns[0])
        if ret_val:
            first_match = [ret_val]
            for i in xrange(1,len(patterns)):
                pattern_prev, pattern_next = patterns[i-1], patterns[i]
                ret_val = self._find_next_by_RE(pattern_next)
                if not ret_val: return
                first_match.append(ret_val)
            return first_match
            match = [first_match[-1]]
            for i in xrange(len(patterns)-2,-1,-1):
                prev_match_line = match[-1][0]
                this_match = first_match[i]
                self.start_line = this_match[0]
                while this_match and this_match[0] < prev_match_line:
                    ret_val = self._find_next_by_RE(patterns[i])
                    if ret_val and ret_val[0] < prev_match_line:
                        this_match = ret_val
                    else: break
                match.append(this_match)
            return list(reversed(match))

    # @abstractmethod
    def to_supported_re(cls, regex):
        """Convert the input Python regular expression to 
           the one which is supported by this logger

        :param cls:     Logger class
        :param regex:   compiled Python regular expression
        :returns:       the closest to the `regex` regular expression supported by the logger
        :rtype:         str
        """
        raise NotImplementedError('Logger {0} does not support regexps'.format(type(self)))

    # @abstractmethod
    def _wait_re(self, pattern, timeout):
        """After the function call, the test script is blocked 
        until the specified string ``pattern`` has been found 
        in the data stream of the logger or the ``timeout`` has lapsed.
        ``_wait_re()`` is a simple form of the function ``WaitForMultipleObjects()``.

        :param pattern:         contains logger supported re which is awaited
        :param timeout:         timeout specified in milliseconds
        :returns:               ``int`` if expected trace string has been received
                                otherwise ``None``
        :return endpos:         the line after the one that contains the message awaited
        """
        raise NotImplementedError('Logger {0} does not specify wait functionality'.format(type(self)))

    # @abstractmethod
    def _wait_multi_re(self, patterns, timeout, wait_all=True):
        """After the function call, the test script is blocked 
        until the specified string ``pattern`` has been found 
        in the data stream of the logger or the ``timeout`` has lapsed.
        ``_wait_re()`` is a simple form of the function ``WaitForMultipleObjects()``.

        :param patterns:        contains list of logger supported re which is awaited
        :param timeout:         timeout specified in milliseconds
        :param wait_all:        specifies whether the receipt of any or all strings is awaited
        :returns:               ``int`` if expected trace string has been received
                                otherwise ``None``
        :return endpos:         the line after the one that contains the message awaited
        """
        if wait_all:    # wait all patterns
            # @caution timeout is invalid in this handling
            line = None
            import time
            start = time.time()
            timeout_left = timeout
            for pattern in patterns:
                start = end
                line = self._wait_re(pattern, timeout_left)
                end = time.time()
                timeout_left -= end - start
                if timeout_left < 0: return 
            return line
        else:           # wait any of patterns
            return self._wait_re('|'.join(patterns))
