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
@file         formatters.py
@author       Sergiy Gogolenko
@license      GPLv3

######################################################################
"""
from __future__ import print_function

def _format_html_attribs(**kwargs):
    return (' ' + ' '.join(map(
        lambda x: r'{0}="{1}"'.format(x[0], x[1]), kwargs.items()))) \
        if kwargs else ''

def _b_latex(s, **kwargs): return r'{{\bf {0}}}'.format(s)
def _b_html(s, **kwargs):  return r'<b>{0}</b>'.format(s)
def _b_md(s, **kwargs):    return r'**{0}**'.format(s)
def _b_none(s, **kwargs):  return str(s)

def _i_latex(s, **kwargs): return r'{{\it {0}}}'.format(s)
def _i_html(s, **kwargs):  return r'<i>{0}</i>'.format(s)
def _i_md(s, **kwargs):    return r'*{0}*'.format(s)
def _i_none(s, **kwargs):  return str(s)

def _u_latex(s, **kwargs): return r'\underline{{{0}}}'.format(s)
def _u_html(s, **kwargs):  return r'<u>{0}</u>'.format(s)
def _u_md(s, **kwargs):    return r'_{0}_'.format(s)
def _u_none(s, **kwargs):  return str(s)

def _sout_latex(s, **kwargs): return r'\sout{{{0}}}'.format(s)
def _sout_html(s, **kwargs):  return r'<strike>{0}</strike>'.format(s)
def _sout_md(s, **kwargs):    return r'~~{0}~~'.format(s)
def _sout_none(s, **kwargs):  return str(s)

def _em_latex(s, **kwargs): return r'\emph{{{0}}}'.format(s)
def _em_html(s, **kwargs):  return 
def _em_md(s, **kwargs):    return r'_'+s+r'_'
def _em_none(s, **kwargs):  return str(s)

def _rm_latex(s, **kwargs): return r'\sout{{{0}}}'.format(s)
def _rm_html(s, **kwargs):  return r'<del>{0}</del>'.format(s)
def _rm_md(s, **kwargs):    return '_{0}_'.format(s)
def _rm_none(s, **kwargs):  return str(s)

def _td_latex(s, **kwargs): return str(s)
def _td_html(s, **kwargs):  return r'<td{1}>{0}</td>'.format(s, _format_html_attribs(**kwargs))
def _td_md(s, **kwargs):    return '|{0}'.format(s)
def _td_none(s, **kwargs):  return '{0} '.format(s)

def _tr_latex(s, **kwargs): return str(s)
def _tr_html(s, **kwargs):  return r'<tr{1}>{0}</tr>'.format(s, _format_html_attribs(**kwargs))
def _tr_md(s, **kwargs):    return '{0}|\n'.format(s)
def _tr_none(s, **kwargs):  return '{0}\n'.format(s)

def _th_latex(s, **kwargs): return str(s)
def _th_html(s, **kwargs):  return r'<th{1}>{0}</th>'.format(s, _format_html_atthibs(**kwargs))
def _th_md(s, **kwargs):    return r'|{0}'.format(s)
def _th_none(s, **kwargs):  return s+' '

def _table_latex(s, **kwargs): return s
def _table_html(s, **kwargs):  return r'<table{1}>{0}</table>'.format(s, _format_html_attribs(**kwargs))
def _table_md(s, **kwargs):    return r'{0}|'.format(s)
def _table_none(s, **kwargs):  return str(s)

def _span_latex(s, **kwargs): return str(s)
def _span_html(s, **kwargs):  return r'<span{1}>{0}</span>'.format(s, _format_html_attribs(**kwargs))
def _span_md(s, **kwargs):    return str(s)
def _span_none(s, **kwargs):  return str(s)

_newline_latex  = r'\newline'
_newline_html   = '<br>'
_newline_md     = '\n\n'
_newline_none   = '\n'

def _pprint_nb(text):
    from IPython.display import HTML,display
    display(HTML('<code>'+ text._repr_html_() if hasattr(text, '_repr_html_')  else repr(text)+ r'</code>'))
def _pprint_none(text):
    print(text)

def _error_nb(text, note='Caution: '):
    from output import span,b
    _pprint_nb(span(b(note) + text, style=r"background-color: pink; color: red"))
def _error_none(text):
    import sys
    print(text, file=sys.stderr)

def _warning_nb(text, note='Caution: '):
    from output import span,b
    _pprint_nb(span(b(note) + text, style=r"background-color: pink; color: red"))
def _warning_none(text):
    import sys
    print(text, file=sys.stderr)


def _text_nb(text):
    from IPython.display import HTML,display
    return HTML('<code>'+ text._repr_html_() if hasattr(text, '_repr_html_')  else repr(text)+ r'</code>')

def _text_none(text):
    print(text)
