#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project  gAutoy
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
@file         FuncCatalog.py
@author       Sergiy Gogolenko
@license      GPLv3

Wraps for MOST function catalogs
######################################################################
"""
class MOSTFunctionCall(object):

    def __init__(self, mostFunc, *args, **kwargs):
        self._func    = mostFunc
        self._args    = args
        self._kwargs  = kwargs

    @property
    def function(self): return self._func

    @property
    def data(self):
        if len(self._args) == 0:
            return ''
        elif len(self._args) == 1:
            if isinstance(self._args[0], basestring): return self._args[0]
            else: return '{0:02X}'.format(self._args[0])
        else: return ''.join('{0:02X}'.format(a) for a in self._args)

class MOSTDescriptor(object):
    _repr_html_formatting_ = r"""<code>[{0}] <b>{1}</b><br><i>{2}</i></code>"""
    
    def __init__(self, id, name, descr = '', owner = None, **kwargs):
        self._id   = id
        self._name = name 
        self._description = descr
        self._owner = owner

    def __hex__(self):
        return '0x{0:03X}'.format(self._id)

    def __int__(self):
        return self._id

    def __str__(self):
        return self._name

    def __repr__(self):
        return r'[{0}] {1}'.format(hex(self), self._name)

    def _repr_html_(self):
        return self._repr_html_formatting_.format( hex(self)[2:], self._name, self._description )

class MOSTDescriptorList(MOSTDescriptor):
    _item_type = MOSTDescriptor

    def __init__(self, id, name, **kwargs):
        self._keys = {}
        super(MOSTDescriptorList, self).__init__(id, name, **kwargs)

    def __call__(self, id, name, **kwargs):
        new_item = self._item_type(id, name, owner = self, **kwargs)
        self._keys[id] = new_item
        setattr( self, name, new_item)
        return new_item

    def __getitem__(self, id):
        return self._keys[id]

    def __len__(self):
        return self._keys.__len__()

class MOSTFunction(MOSTDescriptor):
    # def __init__(self, id, name, descr = '', owner = None):
    #     self.fblock = owner
    #     super(MOSTFunction, self).__init__(id, name, owner = owner, descr = descr)

    @property
    def fblock(self):
        return self._owner

    def __call__(self, *args, **kwargs):
        return MOSTFunctionCall(self, *args, **kwargs)
    
    def _repr_html_(self):
        code, name = hex(self)[2:], self._name
        if isinstance(self.fblock, MOSTFunctionBlock):
            code, name = hex(self.fblock)[2:] + ' ' + code, self.fblock._name + '.' + name
        return self._repr_html_formatting_.format( code, name, self._description )

class MOSTFunctionBlock(MOSTDescriptorList):
    _item_type = MOSTFunction

    def __hex__(self):
        return '0x{0:02X}'.format(self._id)

    @property
    def catalog(self):
        return self._owner
    
class MOSTFuncCatalog(MOSTDescriptorList):
    _item_type = MOSTFunctionBlock

    def __hex__(self):
        return 'len={0}'.format(self._id)

    def __init__(self):
        super(MOSTFuncCatalog, self).__init__(0, 'MOSTFuncCatalog', descr='')

    def load_hbfc(self, filename):
        import sys
        import xml.etree.ElementTree
        root = xml.etree.ElementTree.parse(filename).getroot()
        for blocks in root.findall('FBlock'):  
            s = blocks.findall('FBlockDescription')[0].text
            fblock = self.__call__( int(blocks.findall('FBlockID')[0].text, 16),
                                    str(blocks.findall('FBlockName')[0].text), 
                                    descr = s.encode(sys.stdout.encoding, errors='replace') if s else '' ) 
            for func in blocks.findall('Function'):
                s = func.findall('FunctionDescription')[0].text
                fblock.__call__( int(func.findall('FunctionID')[0].text, 16),
                                 str(func.findall('FunctionName')[0].text), 
                                 descr  = s.encode(sys.stdout.encoding, errors='replace') if s else '' )
        self._id += 1
        self._description += '\n' + filename
        return self
