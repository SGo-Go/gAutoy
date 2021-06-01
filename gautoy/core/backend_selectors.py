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
@file         backend_selectors.py
@author       Sergiy Gogolenko
@license      GPLv3

API to select tools specified in config
######################################################################
"""

import config

__target        = None
_target_backends= ['paramiko', 'putty']

def new_target(*args, **kwargs):
    global __target
    _backend = kwargs.pop('backend',None) or config.get_option('backend.target')
    if   _backend == 'paramiko':
        from gautoy.target import ParamikoTarget
        return ParamikoTarget(*args, **kwargs)
    elif _backend == 'putty':
        from gautoy.target import PUTTYTarget
        return PUTTYTarget(*args, **kwargs)
    else:
        raise(ValueError(r'Unknown target backed "{0}"').format(_backend))

def get_target():
    global __target
    if not __target: __target = new_target()
    elif ( __target.ip != config.get_option('target.ip') or 
           __target.pwd != config.get_option('target.password') or 
           __target.uid != config.get_option('target.login') ):
        __target = new_target()
    return __target


__traceclient_api   = None

__traceclient_log   = None
_logger_backends= ['traceclient']

def get_logger(backend = None):
    global __traceclient_api,__traceclient_log
    _backend = backend or config.get_option('backend.log')
    if   _backend == 'traceclient':
        from gautoy.tools.traceclient import TraceClientAPI,TraceClientLogFrame
        if not __traceclient_api: __traceclient_api = TraceClientAPI()
        if not __traceclient_log: __traceclient_log = TraceClientLogFrame(__traceclient_api)
        return __traceclient_log
    else:
        raise(ValueError(r'Unknown logger backed "{0}"').format(_backend))

__traceclient_cbm   = None
_cbm_backends= ['traceclient']

def get_callback_manager(backend = None):
    global __traceclient_api,__traceclient_cbm
    _backend = backend or config.get_option('backend.cbm')
    if   _backend == 'traceclient':
        from gautoy.tools.traceclient import TraceClientAPI,TraceClientCallbackManager
        if not __traceclient_api: __traceclient_api = TraceClientAPI()
        if not __traceclient_cbm: __traceclient_cbm = TraceClientCallbackManager(__traceclient_api)
        return __traceclient_cbm
    else:
        raise(ValueError(r'Unknown callback manager backed "{0}"').format(_backend))

def reset_callback_manager(backend = None):
    pass

def get_callbacks(process_name, cbm = None):
    from gautoy.cbm import CallableProcess
    return CallableProcess( process_name,
                            get_callback_manager(backend = cbm)
                            if isinstance(cbm, basestring) else cbm )
