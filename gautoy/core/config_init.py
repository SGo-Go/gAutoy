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
@file         config.py
@author       Sergiy Gogolenko
@license      GPLv3

core.config options

If you need to make sure options are available even before a certain
module is imported, register them here rather then in the module.
######################################################################
"""

import config
from   config import (is_int, is_bool, is_text, is_float,
                      is_instance_factory, is_one_of_factory,
                      get_default_val)

styles = ['none']
try:
    from pygments.styles import get_all_styles
    styles.extend(list(get_all_styles()))
    # print '\n'.join(map(lambda i: ' '.join(styles[i::4]),xrange(4)))
except:pass

with config.config_prefix (r'display'):
    config.register_option(r'large_repr', 'truncate', '<not implemented>',
                           validator=is_one_of_factory(['truncate', 'info']))
    config.register_option(r'format', 'none', 'Output format (not valid if "display.nb.active")',
                           validator=is_one_of_factory(['html', 'md', 'none', 'latex']))

with config.config_prefix (r'display.nb'):
    config.register_option(r'active', True, 'Activates notebook mode',
                           validator=is_bool)
    config.register_option(r'repr_html', True, 'use html representation in IPython notebook',
                           validator=is_bool)
    config.register_option(r'code_highlight',
                           'default' if 'default' in styles else styles[0],
                           'highlighting code output in IPython notebook with one of available styles: {0}'.format('|'.join(styles)),
                           validator=is_one_of_factory(styles))

with config.config_prefix (r'log'):
    config.register_option(r'message_fields', 'TimeStamp Message',
                           'list of fields stored in logger message lines by default (note: DO NOT put "line" in the list)',
                           validator=is_text)

with config.config_prefix (r'display.log'):
    config.register_option(r'output', 'line TimeStamp Message ',
                           'list of displayable output fields (note: field "line" is reserved for line no)',
                           validator=is_text)


with config.config_prefix (r'target'):
    config.register_option(r'ip', r'127.0.0.1', 'Target ip',
                           validator=is_text)
    config.register_option(r'host', get_default_val('target.ip'), 'Target ip',
                           validator=is_text)
    config.register_option(r'password', r'some_password', 'Target password',
                           validator=is_text)
    config.register_option(r'login', r'root', 'Target login',
                           validator=is_text)
    config.register_option(r'prompt', r'hu-omap:(\/([a-zA-Z])+)+> ', 'regex for target shell prompts',
                           validator=is_text)
config.deprecate_option('target.host', msg='', rkey='target.ip')

from backend_selectors import _logger_backends,_target_backends,_cbm_backends
with config.config_prefix (r'backend'):
    config.register_option( r'target', 'paramiko',
                            'Back-end for target: {0}'.format(_target_backends),
                            validator=is_one_of_factory(_target_backends) )
    config.register_option( r'log', 'traceclient',
                            'Back-end for logger: {0}'.format(_logger_backends),
                            validator=is_one_of_factory(_logger_backends) )
    config.register_option( r'cbm', 'traceclient',
                            'Back-end for callback manager: {0}'.format(_cbm_backends),
                            validator=is_one_of_factory(_cbm_backends) )

with config.config_prefix (r'domain.map'):
    config.register_option( r'template_folder', r'd:/dev/github/gAutoy/gautoy/domain/maps/jinja2',
                            'Folder with templates for rendeting map holders',
                            validator=is_text )
    config.register_option( r'template', r'gmap-v3-all.html',
                            'Template for rendeting map holders',
                            validator=is_text )
    config.register_option( r'templatizer', 'jinja2',
                            'Templatizer for rendeting map holders',
                            validator=is_one_of_factory(['jinja2']) )
    config.register_option( r'info_text_format', 'markdown',
                            'Format of input descriptions for map info windows',
                            validator=is_one_of_factory(['markdown', 'text', 'html']) )
    config.register_option( r'height', r'640',
                            'Hight of the map in the notebook output',
                            validator=is_text )
    config.register_option( r'width', r'100%',
                            'Width of the map in the notebook output',
                            validator=is_text )
    config.register_option(r'inline', True, 'Embed map into notebook',
                           validator=is_bool)

del styles
