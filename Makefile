#################################################################
# Project  gAutoy
# gAutoy Copyright (C) 2015 SGogolenko
# All rights reserved
#
# This file is part of gAutoy.
#
# gAutoy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# gAutoy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with gAutoy.  If not, see <http://www.gnu.org/licenses/>.
# 
#################################################################
# @package      gAutoy
# @file         makelib.bat
# @author       Sergiy Gogolenko
# @license      GPLv3
#
# Creates Win32/64 installer for gAutoy package
#
#    You can install gAutoy with 'python setup.py install' 
#    github from sources
#################################################################

SPHINXOPTS    =
PAPER         =
BUILDDIR      = _build

PYTHON        = python
SPHINXAPIDOC  = sphinx-apidoc
# NBCONVERT     = ipython nbconvert
NBCONVERT     = jupyter nbconvert
MAKE          = make
DOCSDIR       = docs

COOKBOOK_NB = 
COOKBOOK_RST=$(addprefix $(DOCSDIR)/notebooks/cookbook/, gAutoy-cookbook-config.rst gAutoy-cookbook-logger.rst gAutoy-cookbook-cbm.rst gAutoy-cookbook-magics.rst gAutoy-cookbook-target.rst gAutoy-cookbook-pattern.rst gAutoy-cookbook-domain-most.rst gAutoy-cookbook-domain-map.rst)

clean:
	rm -rf $(COOKBOOK_RST)
	rm -rf *~ *.pyc

install: 
	$(PYTHON) setup.py install
uninstall: 
	pip install gautoy

docs: $(COOKBOOK_RST)
	$(MAKE) -C $(DOCSDIR) html

%.rst : %.ipynb
	$(NBCONVERT)  $<  --to rst --stdout >> $@

extra:
	$(PYTHON) setup.py --install-data=python/data
