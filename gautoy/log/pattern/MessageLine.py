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
@file         MessageLine.py
@author       Sergiy Gogolenko
@copyright    Copyright 2015 by Sergiy Gogolenko.
@license      GPLv3


######################################################################
"""
from __future__ import print_function
import re

from gautoy.core.config import get_option

class BaseMessageLine(object):
    def __init__(self, line_no, log_frame = None, **kwargs):
        self._line = line_no
        for key, val in kwargs.items():
            setattr(self, key, val)
        if log_frame:
            for attr in get_option('log.message_fields').split():
                if attr not in (kwargs.keys() + ['Comment']): # dirty hack: treat comments as special fields
                    setattr(self, attr, getattr(log_frame, attr)[self.line])
                    
    @property
    def line(self):
        return self._line - 1 # @fix for line no, check!

    def __str__(self):
        return str(self.Message)

    def __repr__(self):
        return r"{0} {1}".format(self.line, str(self.Message))

    def to_html_row(self):
        out = ''
        try:
            from gautoy.core.output import td,tr
            html_f = get_ipython().display_formatter.formatters['text/html']
            for attr in get_option('display.log.output').split():
                val = getattr(self, attr)
                out += td(html_f(val) or val,
                          style=r'color:#888;border:1px solid #EEE;' 
                          if attr in ('line', 'TimeStamp')
                          else r'border:1px solid #EEE;')

        except:
            raise RuntimeError('WTF')
        return tr(out)

    def _repr_html_(self, line = True):
        from gautoy.core.output import table
        return r'<small>{0}</small>'.format(table(self.to_html_row(), style="width:100%"))


class MessageLineList(list):
    def __init__(self, *args, **kwargs):
        super(MessageLineList, self).__init__(*args, **kwargs)

    def _repr_html_(self):
        from gautoy.core.output import table
        out = ''
        for x in self: out += x.to_html_row()
        return r'<small>{0}</small>'.format(table(out, style="width:100%"))

    def append(self, x):
        from MultilineMessagePattern import BaseMultilineMessagePattern_Match
        super(MessageLineList, self).extend(x.list)


try:
    __html_f = get_ipython().display_formatter.formatters['text/html']

    def __html_list(lst):
        if isinstance(lst, (list)) and all(isinstance(x, BaseMessageLine) for x in lst): #, tuple
            from gautoy.core.output import table
            out = ''
            for x in lst: out += x.to_html_row()
            return r'<small>{0}</small>'.format(table(out, style="width:100%"))
        else: return repr(lst)
    __html_f.for_type(list, __html_list)
    # html_f.for_type(tuple, __html_list)
except:
    pass
