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

init-file for ``target`` subpackage.
######################################################################
"""

from __future__ import absolute_import


import gautoy.core.config
from   gautoy.core.config import (is_int, is_bool, is_text, is_float,
                                  is_instance_factory, is_one_of_factory,
                                  get_default_val)

with gautoy.core.config.config_prefix (r'target.ssh'):
    gautoy.core.config.register_option(r'client', r'kitty.exe', 'SSH console',
                           validator=is_text)
    gautoy.core.config.register_option(r'shell', r'plink.exe -ssh', 'Console utility for running remote commands via SSH',
                           validator=is_text)
    gautoy.core.config.register_option(r'max_local_get_file_size', 20000, 'Upper bound for file size downloadable without need to invoke SSH utility',
                           validator=is_int)
    gautoy.core.config.register_option(r'max_local_put_file_size',  4096, 'Upper bound for file size uploadable without need to invoke SSH utility',
                           validator=is_int)

from gautoy.target.Target      import PUTTYTarget
try:
    import paramiko
    from gautoy.target.Target  import PUTTYTarget,ParamikoTarget
    from gautoy.target.Target  import ParamikoTarget as Target
except ImportError:
    from gautoy.target.Target  import PUTTYTarget as Target
