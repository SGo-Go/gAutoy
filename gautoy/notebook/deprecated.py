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
@file         magic.py
@author       Sergiy Gogolenko
@copyright    Copyright 2015 by Sergiy Gogolenko.
@license      GPLv3

Magics for convenience of IPython/Jupyter Notebook use
######################################################################
"""

from __future__ import print_function
from IPython.core.magic import register_cell_magic

from gautoy.core.config import get_option

@register_cell_magic
def bash_target(line, cell):
    """Magic for non-interacve scripting on targets (access via Telnet).
       Ends with exit.

       usage: -c [-h] [-w WAIT] [-i] [-l LOGIN] [-p PASSWORD] [--prompt PROMPT]
                 [-s STYLE] [-n]
                 [host]

       positional arguments:
         host

       optional arguments:
         -h, --help            show this help message and exit
         -w WAIT, --wait WAIT  Time to wait [in sec] before closing connection
         -i, --no-exit         Skip auto-exit (caution: exit must be done explicitely
                               in last cell's line)
         -l LOGIN, --login LOGIN
                               Target login
         -p PASSWORD, --password PASSWORD
                               Target password
         --prompt PROMPT       Regex for target shell prompts
         -s STYLE, --style STYLE
                               Output style schema
         -n, --lineno          Display line number
    """

    newline = '\r\n'
    import telnetlib,re,argparse

    # Parse magic options
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wait', type=float, default = 0, 
                        help = r"Time to wait [in sec] before closing connection")
    parser.add_argument('-i', '--no-exit', action='store_true',
                        help = r"Skip auto-exit (caution: exit must be done explicitely in last cell's line)")
    parser.add_argument('-l', '--login', type=str, default = get_option('target.login'),
                        help = r'Target login')
    parser.add_argument('-p', '--password', type=str, default = get_option('target.password'),
                        help = r'Target password')
    parser.add_argument('--prompt', type=str, default = get_option('target.prompt'),
                        help = r'Regex for target shell prompts')
    parser.add_argument('-s', '--style', type=str, default = get_option('display.nb.code_highlight'),
                        help = r'Output style schema')
    parser.add_argument('-n', '--lineno', action='store_true',
                        help = r'Display line number')
    parser.set_defaults(lineno=False)
    parser.add_argument('host', nargs='?', default = get_option('target.ip'))
    try:
        args = parser.parse_args(line.split())
    except:
        parser.print_help()
        raise(ValueError('Unrecognized options in magic'))

    host = re.match(r'^(?P<ip>[1-2]?\d?[1-9](\.([1-2]?\d{1,2})){3,3})$', args.host)
    if not host:
        raise(ValueError('Incorrect ip {0}'.format(line)))

    host        = host.group('ip')
    user        = args.login
    password    = args.password

    # Connection
    tn = telnetlib.Telnet(host, 23, 5)
    tn.read_until('login:',2)
    tn.write((user + newline).encode('ascii'))
    
    tn.read_until('Password: ',2)
    tn.write((password + newline).encode('ascii'))

    cmd_lines = cell.encode('ascii').split('\n')
    for cmd in (cmd_lines[:-1] if args.no_exit else cmd_lines):
        if len(cmd) > 0:
            tn.write(cmd + newline)

    tn.write(r"exit" + newline)
    import time
    # time.sleep(1)
    # output = tn.read_very_eager()
    output = tn.read_all()
    tn.close

    # Reconnect and do the last command (workaround to call tn.read_all successfully)
    if args.no_exit:
        tn = telnetlib.Telnet(host, 23, 5)
        tn.read_until('login:',2)
        tn.write((user + newline).encode('ascii'))
    
        tn.read_until('Password: ',2)
        tn.write((password + newline).encode('ascii'))
        tn.write(cmd_lines[-1] + newline)
        import time
        time.sleep(args.wait)
        tn.close

    if args.style != 'none' and get_option('display.nb.repr_html'):
        from IPython.display import HTML
        from pygments import highlight
        from pygments.lexers import BashSessionLexer #BashLexer#
        from pygments.formatters import HtmlFormatter
        return HTML(highlight(re.sub(args.prompt, '#> ', output),
                              #r'[{0}@{1} ~]# '.format(user, host), 
                              BashSessionLexer(), #BashLexer(), #
                              HtmlFormatter(linenos=args.lineno, style=args.style, noclasses=True)))
    else:
        print(output)
