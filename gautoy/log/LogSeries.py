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
@file         LogSeries.py
@author       Sergiy Gogolenko
@license      GPLv3

Class that provides access to the entries of TraceClient log attribute
######################################################################
"""
from __future__ import print_function

class LogSeries(object):
    """
    Class that provides access to the entries of TraceClient 
    log attribute
    """
    def __init__(self, name, log_frame, converter=None):
        self.__name     = name
        self.__logFrame = log_frame
        self.to_dtype = converter

    @property
    def name(self):
        return self.__name

    def __len__(self):
        return self.__logFrame.__len__()

    def __getitem__(self, line_no):
        """Get message attribute value

        :param line_no: index of the message to select
        :returns:       the attribute value
        :rtype:         str

        """
        value = self.__logFrame.get(self.__len__() + line_no if line_no < 0 else line_no, self.__name)
        return value if self.to_dtype is None else self.to_dtype(value)

    def __getslice__(self, line_from, line_to):
        """Get message attribute slice as ``pandas`` series
        """
        from pandas import Series
        values = self.__logFrame.attribute(self.__name, line_from, line_to)
        return Series(values if self.to_dtype is None else map(self.to_dtype, values),
                      index=range(line_from, line_to))

    def __repr__(self):
        return "{1} LogSeries([...], Name: {0}, dtype: str)".format(self.name, self.__logFrame.backend)

    def _repr_html_(self):
        return "<code>{1} LogSeries([...], Name:<i>{0}</i>, dtype:<i>str</i>)</code>".format(self.name, self.__logFrame.backend)
