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
from IPython.core.magic import register_cell_magic,register_line_magic

from gautoy.core.config import get_option

import argparse
class MagicArgumentParser(argparse.ArgumentParser):
    def add_target(self):
        super(MagicArgumentParser, self).add_argument('-l', '--login',
                                                          type=str, default = get_option('target.login'),
                                                          help = r'Target login')
        super(MagicArgumentParser, self).add_argument('-p', '--password',
                                                          type=str, default = get_option('target.password'),
                                                          help = r'Target password')
        super(MagicArgumentParser, self).add_argument('host', nargs='?', default = get_option('target.ip'))


    def parse_args(self, *args, **kwargs):
        try:
            args = super(MagicArgumentParser, self).parse_args(*args, **kwargs)
        except SystemExit:
            return None
        except:
            super(MagicArgumentParser, self).print_help()
            raise(ValueError('Unrecognized options in magic'))

        import re
        host = re.match(r'^((?P<login>[a-zA-Z]+)@)?(?P<ip>[1-2]?\d?[1-9](\.([1-2]?\d{1,2})){3,3})$', args.host)
        if not host:
            super(MagicArgumentParser, self).print_help()
            raise(ValueError('Check host name for being a valid ip {0}'.format(line)))
        args.host = host.group('ip')
        if host.group('login'): args.login = host.group('login')
        return args


@register_cell_magic
def gautoy_bash(line, cell):
    """Magic for non-interacve scripting on targets (access via Telnet).
       Ends with exit.

       Use: ``%%gautoy_bash -h`` to get usage info
    """

    import telnetlib
    newline = '\r\n'

    # Parse magic options
    parser = MagicArgumentParser()
    parser.add_target()
    parser.add_argument('-w', '--wait', type=float, default = 1, 
                        help = r"Time to wait [in sec] before closing connection")
    parser.add_argument('-i', '--no-exit', action='store_true',
                        help = r"Skip auto-exit (caution: exit must be done explicitely in last cell's line)")
    parser.add_argument('--prompt', type=str, default = get_option('target.prompt'),
                        help = r'Regex for target shell prompts [use for correct syntax highlight]')
    parser.add_argument('-s', '--style', type=str, default = get_option('display.nb.code_highlight'),
                        help = r'Output style schema')
    parser.add_argument('-n', '--lineno', action='store_true',
                        help = r'Display line number')
    parser.add_argument('-v', '--verbose', type=int, default = 1, 
                        help = r"Verbose level [0 - no output; 1 - `sh` output]")
    parser.set_defaults(lineno=False)

    args = parser.parse_args(line.split())
    if not args: return

    # Connection
    try:
        tn = telnetlib.Telnet(args.host, 23, 5)
    except:
        raise(RuntimeError('Cannot connect to {0}@{1}'.format(args.login, args.host)))
    tn.read_until('login:',2)
    tn.write((str(args.login) + newline).encode('ascii'))
    
    tn.read_until('Password: ',2)
    tn.write((str(args.password) + newline).encode('ascii'))

    cmd_lines = cell.encode('ascii').split('\n')
    for cmd in (cmd_lines[:-1] if args.no_exit else cmd_lines):
        if len(cmd) > 0: tn.write(cmd + newline)

    tn.write(r"exit" + newline)

    import re
    def filter_output(s):
        # return '' if args.verbose == 0 else \
        #     re.sub(r'{0}.*'.format(args.prompt), '', s) \
        #     if args.verbose == 1 else s
        cmd = re.compile(r'^({0}|> ).*'.format(args.prompt))
        return '' if args.verbose == 0 else \
            '\n'.join(filter(lambda l: not cmd.match(l), s.split('\n'))) \
            if args.verbose == 1 else s
    try:
        output = filter_output(tn.read_all())
    except:
        import time
        if get_option('display.nb.repr_html'):
            from gautoy.core.output import warning,i
            warning('Output is unreliable: ' + i('check whether your script has iteractive parts'))
        else:
            print('Caution! Output is unreliable '
                  '[check whether your script has iteractive parts].')
        time.sleep(args.wait)
        output = filter_output(tn.read_very_eager())

    tn.close

    # Reconnect and do the last command (workaround to call tn.read_all successfully)
    if args.no_exit:
        tn = telnetlib.Telnet(args.host, 23, 5)
        tn.read_until('login:',2)
        tn.write((args.login + newline).encode('ascii'))
    
        tn.read_until('Password: ',2)
        tn.write((args.password + newline).encode('ascii'))
        tn.write(cmd_lines[-1] + newline)
        import time
        time.sleep(args.wait)
        output += filter_output(tn.read_very_eager())
        tn.close

    if args.style != 'none' and get_option('display.nb.repr_html'):
        from IPython.display import HTML
        from pygments import highlight
        from pygments.lexers import BashSessionLexer
        from pygments.formatters import HtmlFormatter
        return HTML(highlight(re.sub(args.prompt, '#> ', output),
                              #r'[{0}@{1} ~]# '.format(args.login, args.host), 
                              BashSessionLexer(), 
                              HtmlFormatter(linenos=args.lineno, style=args.style, noclasses=True)))
    else:
        print(output)

@register_line_magic
def gautoy_screenshot(line):
    """Magic for taking screenshot on targets.

       Use: ``%gautoy_screenshot -h`` to get usage info
    """

    import time,re
    from gautoy.target import Target

    # Parse magic options
    parser = MagicArgumentParser()
    parser.add_target()
    parser.add_argument('-ne', '--no-embed', action='store_true',
                        help = r'Embed image to notebook')
    parser.add_argument('-c', '--close-traceclient', action='store_true',
                        help = r'Close TraceClient after callback that takes screenshot')
    parser.add_argument('-o', '--output', type=str, default = '.',
                        help = r'Output folder')
    parser.set_defaults(no_embed=False, close_traceclient=False)

    args = parser.parse_args(line.split())
    if not args: return

    # Connect to TraceClient
    from gautoy.tools.traceclient.TraceClientAPI import TraceClientAPI
    from gautoy.tools.traceclient.TraceClientCBM import TraceClientCallbackManager
    # from gautoy.core.backend_selectors import __traceclient_cbm,
    #traceClient = __traceclient_cbm or TraceClient()
    api = TraceClientAPI()
    traceClient = TraceClientCallbackManager(api)

    disconnect = False
    if not traceClient.is_connected:
        traceClient.connect(auto_close=args.close_traceclient)
        disconnect = True
    # Callback to take screenshot
    traceClient.set_process("NBTCarHU", max_attempts = 10, timeOut = 1000)
    traceClient.call("CScreenshotControllerBase_CallBack_doScreenShot", 1)

    if disconnect: traceClient.disconnect()
    
    # from gautoy import get_callback_manager
    # from gautoy.cbm import CallableProcess
    # cbm = get_callback_manager(backend='traceclient')
    # with CallableProcess("NBTCarHU", cbm) as cb:
    #     cb.CScreenshotControllerBase_CallBack_doScreenShot(1)
    
    # Create target instance and connect to target
    target = Target(args.host, uid = args.login, pwd = args.password)
    time.sleep(0.2) # short delay to ensure callback is done and screenshot is stored in target FS
    
    # Get screenshot to the given folder
    screenFolder = r'/mnt/quota/sys/trace'  # Target folder where the screenshots are stored (the standard one)
    patternScreenshots = re.compile(r'^screenshot.+HU.*\.png$')     # Pattern for screenshot names (regex)
    screenshots = []
    for path in target.listdir(screenFolder, onlyFiles = True):
        if patternScreenshots.match(path):
            target.get( target.path.join(screenFolder, path), args.output ) # Download file from target
            screenshots.append(path)

    if not args.no_embed:
        if get_option('display.nb.repr_html'):
            from IPython.display import Image,display
            import os
            display(Image(filename=os.path.join(args.output, screenshots[0])))
        else:
            print('Put [{1}] in {0}'.format(output, ' '.join(screenshots)))
    return screenshots
