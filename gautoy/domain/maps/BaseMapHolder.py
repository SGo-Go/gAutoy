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
@file         GoogleMaps.py
@author       Sergiy Gogolenko
@license      GPLv3

Setup script for targetAssist.
You can install targetAssist with 'python setup.py install'
######################################################################
"""
from __future__ import print_function

import os, sys, subprocess
import time

from gautoy.core.config import get_option

class MapInfoObject(object):

    def __init__(self, name ='', description = ''):
        self._name        = name
        self._description = description
        self._info        = self.info_html()

    @property
    def name(self): return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, basestring):
            self._name        = name
            self._info        = self.info_html()

    @property
    def description(self): return self._description
        
    @description.setter
    def description(self, descr):
        if isinstance(descr, basestring):
            self._description = descr
            self._info        = self.info_html()
    
    @property
    def info(self): return self._info.replace('\n','').replace('\r','')
    
    def info_html(self):
        if get_option('domain.map.info_text_format') == 'markdown':
            import markdown2
            return markdown2.markdown("### {0.name} \n{0.description}".format(self),
                                      extras=["code-friendly", "tables", "break-on-newline"])
        else: return r"<h3>{0.name}</h3><p>{0.description}</p>".format(self)

class MapLabel(MapInfoObject):

    icon_map = {
        'screenshot' : r'https://raw.githubusercontent.com/SGo-Go/gAutoy/master/gautoy/domain/maps/icons/black-screenshot-16.png',
        # 'screenshot' : 'http://findicons.com/files/icons/2673/social_media_icons/32/instagram.png',
        # 'screenshot' : 'http://findicons.com/files/icons/2344/faenza/32/gnome_screenshot.png',
        'turnaround' : r'http://icons.iconarchive.com/icons/fatcow/farm-fresh/32/routing-turnaround-right-icon.png',
        'circle'     : r'https://raw.githubusercontent.com/SGo-Go/gAutoy/master/gautoy/domain/maps/icons/{0}-circle-16.png',
    }

    def __init__(self, position, name ='', description = '', color = None, icon = None):
        super(MapLabel, self).__init__(name = name, description = description)
        self.position    = position
        self.color       = color
        self.icon        = icon

    @property
    def icon_url(self):
        if   self.icon : return self.icon_map.get(self.icon, self.icon).format(self.color or 'red')
        elif self.color: return r'http://maps.google.com/mapfiles/ms/icons/{0}-dot.png'.format(self.color or 'red')
        else:            return r'http://maps.google.com/mapfiles/ms/icons/red-dot.png'

    def __repr__(self):
        return r'label(lat={0.position[1]}, lon={0.position[1]}, name="{0.name}")'.format(self)

    def _repr_html_(self):
        return """<code style="color:{0.color}">
        label(lat=<it>{0.position[1]}</it>,lon=<it>{0.position[1]}</it>,name="<it>{0.name}</it>")
        </code>""".format(self)

class MapPolyline(MapInfoObject):

    def __init__(self, path, name ='', description = '', color = 'black', opacity = 0.7, weight = 1, directed = False):
        super(MapPolyline, self).__init__(name = name, description = description)
        self.path        = path
        self.color       = color
        self.opacity     = opacity
        self.weight      = weight

    def append(self, coo):
        self.path.append(coo)
        
    def __len__(self):
        return self.path.__len__()
        
    def __repr__(self):
        return r'path(len={1} name="{0.name}")'.format(self, len(self.path))

    def _repr_html_(self):
        return """<code style="color:{0.color}">
        path(len=<it>{1}</it>,name="<it>{0.name}</it>")
        </code>""".format(self,len(self.path))

class BaseMapHolder(object):

    def __init__(self, default_output = None):
        self.labels = []
        self.paths  = []
        self.default_output = default_output

    def new_label(self, position, *args, **kwargs):
        self.labels.append(MapLabel(position, *args, **kwargs))
        return self.labels[-1]

    def new_path(self, path, *args, **kwargs):
        self.paths.append(MapPolyline(path, *args, **kwargs))
        return self.paths[-1]

    def _repr_html_(self):
        output = 'track.html'

        from jinja2   import Template
        from tempfile import NamedTemporaryFile
        import os
        # from gmap-v3-all import gmap-v3-all
        # os.path.dirname(os.path.realpath(__file__))
        output_file = open(self.default_output, 'w') if self.default_output else\
                      NamedTemporaryFile(delete=False, dir = os.getcwd(), suffix='.html')
        temp = os.path.join(get_option('domain.map.template_folder'), get_option('domain.map.template'))
        template = Template(open(temp, "r").read())
        output_file.write(template.render(map=self))
        output_file.close()
        return (r"""<div>
  <a href="{0}" target="_blank" 
     style="text-decoration: none;color:lightgray;background-color: gray;border:1px solid black;text-align:center;border-radius: 0.2em;box-shadow: -1px 2px 5px 1px rgba(0, 0, 0, 0.7);margin: 0.2em;padding: 0.2em; position:absolute; left: 120px; top: 1em;">Full Window Map</a><br>
  <iframe src="{0}" width="{1}" height="{2}"></iframe>
</div>""" if get_option('domain.map.inline') else \
"""<div>
  <a href="{0}" target="_blank" 
     style="text-decoration: none;color:lightgray;background-color: gray;border:1px solid black;text-align:center;border-radius: 0.2em;box-shadow: -1px 2px 5px 1px rgba(0, 0, 0, 0.7);margin: 0.2em;padding: 0.2em;">Full Window Map</a><br>
</div>""").\
            format( os.path.basename(output_file.name),
                    get_option('domain.map.width'), 
                    get_option('domain.map.height') )
