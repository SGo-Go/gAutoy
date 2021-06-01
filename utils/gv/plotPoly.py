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
@file         plotPoly.py
@author       Sergiy Gogolenko
@license      GPLv3

Plots Ic/HUD vector graphics
######################################################################
"""

import time, re, sys

"polygon chunk (TargetInstanceType:HG/LG/MiMa) - fillColor (RGBA): c0c0c0ff, numPoints 6, (eleInfo: W=100, H=150, ElementType=906189666)"

from matplotlib.pyplot import *
from matplotlib.path import Path
import matplotlib.patches as patches

verts = [
    (0.0, 82.8),
    (0.0, 0.0),
    (13.8, 0.0),
    (34.0, 20.8),
    (15.0, 20.8),
    (15.0, 82.8),]

topLeft = 125, 58
shiftPoint = lambda pt: (pt[0]+topLeft[0],pt[1]+topLeft[1])
shiftPoint = lambda pt: (pt[0],pt[1])

verts = map(shiftPoint, verts)

# verts = [
#     (67,39),
#     (67,18),
#     (58,18),
#     (72,0),
#     (72,0),
#     (86,18),
#     (77,18),
#     (77,39),
# ]

def Polygon(verts):
    #verts.append(verts[-1])
    v = verts + [verts[-1]]
    codes = [Path.MOVETO] + [Path.LINETO]*(len(v) - 2) + [Path.CLOSEPOLY]
    path  = Path(v, codes)
    return patches.PathPatch(path, facecolor='orange', lw=2)

fig = figure(figsize=(6,6))
ax  = fig.add_subplot(111)

ax.add_patch(Polygon(verts))

diameter = 50
center   = shiftPoint((0, -44))

circle = patches.Circle(center, diameter/2., facecolor='orange', lw=2)
ax.add_patch(circle)

ax.set_xlim(-100,100)
ax.set_ylim(-100,100)
# ax.set_xlim(-00,100)
# ax.set_ylim(-00,100)
ax.invert_yaxis()
#show()
savefig('DRA.png')


# prefix = "IcHudCommandParser: "
# "{prefix}point ([0-9]+): tmpX ([0-9]+)/tmpY ([0-9]+)"
# "element info chunk - elementType: 906189666, styleRef: 0, flags: 6, topLeft 125/58 (x/y), width: 100, height: 150"

