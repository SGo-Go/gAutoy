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
@file         output.py
@author       Sergiy Gogolenko
@license      GPLv3

######################################################################
"""
from __future__ import print_function

import re
from formatters import _newline_none,_span_none,_table_none,_th_none,_tr_none,_td_none,\
    _rm_none,_em_none,_sout_none,_u_none,_i_none,_b_none

newline = _newline_none
span    = _span_none
table   = _table_none
th      = _th_none
tr      = _tr_none
td      = _td_none
rm      = _rm_none
em      = _em_none
sout    = _sout_none
u       = _u_none
i       = _i_none
b       = _b_none

from formatters import _pprint_none,_warning_none,_error_none
pprint  = _pprint_none
warning = _warning_none
error   = _error_none

# text  = _text_none

def init_printing(formatter = None):
    global newline,span,table,th,tr,td,rm,em,sout,u,i,b,\
        pprint,warning,error

    from gautoy.core.config import get_option
    # from formatters import _pprint_nb,_warning_nb,_error_nb
    import gautoy.core.formatters
    if get_option(r'display.nb.active') and get_option(r'display.nb.repr_html'):
        formatters_type = 'html'
        pprint  = gautoy.core.formatters._pprint_nb
        warning = gautoy.core.formatters._warning_nb
        error   = gautoy.core.formatters._error_nb
        # text    = _text_none
    else:
        formatters_type = formatter or get_option(r'display.format')
        pprint  = gautoy.core.formatters._pprint_nb
        warning = gautoy.core.formatters._warning_nb
        error   = gautoy.core.formatters._error_nb

    for name in ('newline','span','table','th','tr','td','rm','em','sout','u','i','b'):
        exec('gautoy.core.output.{0} = gautoy.core.formatters._{0}_{1}'.format(name,formatters_type))

def in_ipynb():
    try:
        print('start check')
        cfg = get_ipython().config 
        if cfg['IPKernelApp']['parent_appname'] == 'ipython-notebook':
            return True
        else:
            return False
    except NameError:
        return False
