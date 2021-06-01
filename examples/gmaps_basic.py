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
@file         gmaps_basic.py
@author       Sergiy Gogolenko
@license      GPLv3

Example of GoogleMaps use
######################################################################
"""
import sys, os
from gautoy import GoogleMaps

googleMaps = GoogleMaps()
print(googleMaps.address_to_latlng('Krasni Liman'))
print(googleMaps.address_to_latlng('Munchen'))


if  len(sys.argv) == 1  or sys.argv[1] == '0':
    googleMaps.move_to(address = 'Krasni Liman')
    googleMaps.show(zoom=11,new=1, type='satellite')
elif len(sys.argv) == 2 and sys.argv[1] == '1':
    googleMaps.move_to(48, 11.5)
    googleMaps.direction_to(48.131903, 11.570050)
    googleMaps.show(zoom=11,new=1, type='satellite')
elif len(sys.argv) == 2 and sys.argv[1] == '2':
    googleMaps.move_to(address = 'Cologne')
    googleMaps.directions([(48.131943, 11.569981),(48.133131, 11.566762),(48.129537, 11.558458), (48.128033, 11.564273), (48.125154, 11.561999)])
    googleMaps.show(zoom=15,new=1,language='en')
elif len(sys.argv) == 2 and sys.argv[1] == '3':    
    googleMaps.directions([(48.773459, 9.179749),(48.775726, 9.183343),(48.774391, 9.185407), (48.771317, 9.182464), (48.766252, 9.179137),(48.767537, 9.182961) ])
    googleMaps.show(zoom=15,new=1,language='ua')
    # doflg=
    # msa=
