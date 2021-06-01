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
@file         __init__.py
@author       Sergiy Gogolenko
@license      GPLv3

init-file for ``notebook`` subpackage.
######################################################################
"""

# from __future__ import absolute_import

try:
    __IPYTHON__

    import IPython
    if IPython.version_info[0] >= 3 and IPython.version_info[1] >=2 and IPython.version_info[3] >= 1:
        js = "IPython.CodeCell.config_defaults.highlight_modes['bash'] = {'reg':[/^%%gautoy_bash/]};"
        IPython.core.display.display_javascript(js, raw=True)

    import IPython.core.magic
    from gautoy.notebook.magic  import gautoy_screenshot, gautoy_bash
except: # ImportError,NameError
    pass
