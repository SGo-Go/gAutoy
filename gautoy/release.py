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
@file         release.py
@author       Sergiy Gogolenko
@license      GPLv3

Release data for gAutoy.
######################################################################
"""

from __future__ import absolute_import

import os
import sys
import time
import datetime
import subprocess

basedir = os.path.abspath(os.path.split(__file__)[0])

def write_versionfile():
    """Creates a static file containing version information."""
    versionfile = os.path.join(basedir, 'version.py')

    text = '''"""
Version information for gAutoy, created during installation.

Do not add this file to the repository.

"""

import datetime

version = %(version)r
date = %(date)r

# Was gAutoy built from a development version? If so, remember that the major
# and minor versions reference the "target" (rather than "current") release.
dev = %(dev)r

# Format: (name, major, min, revision)
version_info = %(version_info)r

# Format: a 'datetime.datetime' instance
date_info = %(date_info)r

# Format: (vcs, vcs_tuple)
vcs_info = %(vcs_info)r

'''

    # Try to update all information
    date, date_info, version, version_info, vcs_info = get_info(dynamic=True)

    def writefile():
        fh = open(versionfile, 'w')
        subs = {
            'dev' : dev,
            'version': version,
            'version_info': version_info,
            'date': date,
            'date_info': date_info,
            'vcs_info': vcs_info
        }
        fh.write(text % subs)
        fh.close()

    if vcs_info[0] == 'mercurial':
        # Then, we want to update version.py.
        writefile()
    else:
        if os.path.isfile(versionfile):
            # This is *good*, and the most likely place users will be when
            # running setup.py. We do not want to overwrite version.py.
            # Grab the version so that setup can use it.
            sys.path.insert(0, basedir)
            from version import version
            del sys.path[0]
        else:
            # This is *bad*. It means the user might have a tarball that
            # does not include version.py. Let this error raise so we can
            # fix the tarball.
            ##raise Exception('version.py not found!')

            # We no longer require that prepared tarballs include a version.py
            # So we use the possibly trunctated value from get_info()
            # Then we write a new file.
            writefile()

    return version

def get_revision():
    """Returns revision and vcs information, dynamically obtained."""
    vcs, revision, tag = None, None, None

    hgdir = os.path.join(basedir, '..', '.hg')
    gitdir = os.path.join(basedir, '..', '.git')

    if os.path.isdir(hgdir):
        vcs = 'mercurial'
        try:
            p = subprocess.Popen(['hg', 'id'],
                                 cwd=basedir,
                                 stdout=subprocess.PIPE)
        except OSError:
            # Could not run hg, even though this is a mercurial repository.
            pass
        else:
            stdout = p.communicate()[0]
            # Force strings instead of unicode.
            x = list(map(str, stdout.decode().strip().split()))

            if len(x) == 0:
                # Somehow stdout was empty. This can happen, for example,
                # if you're running in a terminal which has redirected stdout.
                # In this case, we do not use any revision/tag info.
                pass
            elif len(x) == 1:
                # We don't have 'tip' or anything similar...so no tag.
                revision = str(x[0])
            else:
                revision = str(x[0])
                tag = str(x[1])

    elif os.path.isdir(gitdir):
        vcs = 'git'
        # For now, we are not bothering with revision and tag.

    vcs_info = (vcs, (revision, tag))

    return revision, vcs_info

def get_info(dynamic=True):
    ## Date information
    date_info = datetime.datetime.now()
    date = time.asctime(date_info.timetuple())

    revision, version, version_info, vcs_info = None, None, None, None

    import_failed = False
    dynamic_failed = False

    if dynamic:
        revision, vcs_info = get_revision()
        if revision is None:
            dynamic_failed = True

    if dynamic_failed or not dynamic:
        # This is where most final releases of gAutoy will be.
        # All info should come from version.py. If it does not exist, then
        # no vcs information will be provided.
        sys.path.insert(0, basedir)
        try:
            from version import date, date_info, version, version_info, vcs_info
        except ImportError:
            import_failed = True
            vcs_info = (None, (None, None))
        else:
            revision = vcs_info[1][0]
        del sys.path[0]

    if import_failed or (dynamic and not dynamic_failed):
        # We are here if:
        # we failed to determine static versioning info, or
        # we successfully obtained dynamic revision info
        version = ''.join([str(major), '.', str(minor)])
        if dev:
            version += '.dev_' + date_info.strftime("%Y%m%d%H%M%S")
        version_info = (name, major, minor, revision)

    return date, date_info, version, version_info, vcs_info

## Version information
name = 'gAutoy'
major = "0"
minor = "1"

## Declare current release as a development release.
## Change to False before tagging a release; then change back.
dev = True

description = "Python package for creating and manipulating UML class diagrams"

long_description = \
"""
gAutoy is a Python package for convenient scripting 
related to tools used by CPM BMW Navi Luxoft Odessa team.
"""
license = 'GPLv3'
authors = {'Gogolenko' : ('Sergiy Gogolenko','sgogolenko@luxoft.com')}
maintainer = "gAutoy Developers"
maintainer_email = authors['Gogolenko'][1]
platforms = ['Linux','Mac OSX','Windows','Unix']
keywords = ['Target', 'TraceClient',]
url = "@TODO"
download_url = "@TODO"
classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: UML Generators',
        'Topic :: Software Development :: C++ Parsing',]

date, date_info, version, version_info, vcs_info = get_info()

if __name__ == '__main__':
    write_versionfile()
