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

class GoogleMaps(object):

    googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'
    patternLocation  = r'https://www.google.com.ua/maps/@{location[0]},{location[1]},{{zoom}}z?hl=en'
    #patternDirection  = r'http://maps.google.com/maps?z={{zoom}}&t={{type}}&q=loc:{location[0]}+{location[1]}&hl=ru'
    patternLocation  = r'http://maps.google.com/maps?z={{zoom}}&t={{type}}&hl={{language}}&ll={location[0]},{location[1]}&hl={{language}}'
    patternDirection = r'http://maps.google.com/maps?z={{zoom}}&t={{type}}&hl={{language}}&saddr={location[0]},{location[1]}&daddr={destination[0]},{destination[1]}'
    patternDirections= r'http://maps.google.com/maps?z={{zoom}}&t={{type}}&hl={{language}}&saddr={location[0]},{location[1]}&daddr={destination}'

    def __init__(self):
        self.__url = "http://maps.google.com/"
        self.__location = 48.1768304, 11.5590966
        self.__destination = None

    @classmethod
    def address_to_latlng(cls, query, sensor=False):
        import urllib
        import simplejson

        query = query.encode('utf-8')
        params = {
            'address': query,
            'sensor': "true" if sensor else "false"
        }
        url = cls.googleGeocodeUrl + urllib.urlencode(params)
        json_response = urllib.urlopen(url)
        response = simplejson.loads(json_response.read())
        if response['results']:
            location = response['results'][0]['geometry']['location']
            latitude, longitude = location['lat'], location['lng']
            print(query, latitude, longitude)
        else:
            latitude, longitude = None, None
            raise Exception("Failed to complete query `{0}'".format(query))
        return latitude, longitude


    def _repr_html_(self):
        url = self.__url.format(zoom = 15, language = 'en',
                                type={'normal':'m','satellite':'k','hybrid':'h','terrain':'p'}.get('h', 'm'))
        # return r'<a href="{0}">GoogleMap</a>'.format(url)
        return """
        <iframe class="map" 
           src="{0}&output=embed" 
           width="100%" height="640" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" style="border:0" allowfullscreen>
        </iframe>""".format(url)

    def show(self, zoom = 15, type = 'normal', language = 'en', new = 2, browser='windows-default'):
        url = self.__url.format(zoom = zoom, language = language,
                                type={'normal':'m','satellite':'k','hybrid':'h','terrain':'p'}.get(type, 'm'))
        import webbrowser
        webbrowser.get(browser).open(url,new=new)

    def move_to(self, lat = None, lon = None, location = None, address = None):
        if address is not None:
            self.__location = self.address_to_latlng(address)
        elif location is not None:
            self.__location = map(float, location)
        elif lon is not None and lat is not None:
            self.__location = float(lat), float(lon)
        elif lon is None and lat is None:
            self.__location = 48.1768304, 11.5590966
        else:
            raise IOError("Wrong position to go")
        self.__url = self.patternLocation.format(location = self.location)

    def direction_to(self, lat = None, lon = None, location = None, address = None):
        if address is not None:
            self.__destination = self.address_to_latlng(address)
        elif location is not None:
            self.__destination = map(float, location)
        elif lon is not None and lat is not None:
            self.__destination = float(lat), float(lon)
        elif lon is None and lat is None:
            self.__destination = 48.1768304, 11.5590966
        else:
            raise IOError("Wrong position to go")
        self.__url = self.patternDirection.format(location = self.location, destination = self.__destination)

    def directions(self, points):
        self.__url = self.patternDirections.format(location = points[0], destination = '%20to:'.join(map(lambda x: '{0},{1}'.format(*x), points[1:])))
        # self.__url += '&via=Neuberg,+Germany'
        
    @property
    def location(self):
        return self.__location
