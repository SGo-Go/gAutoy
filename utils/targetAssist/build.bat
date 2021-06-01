::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Project  gAutoy
:: gAutoy Copyright (C) 2015 SGogolenko
:: All rights reserved
::
:: This file is part of gAutoy.
::
:: gAutoy is free software: you can redistribute it and/or modify
:: it under the terms of the GNU General Public License as published by
::  the Free Software Foundation, either version 3 of the License, or
:: (at your option) any later version.
:: 
:: gAutoy is distributed in the hope that it will be useful,
:: but WITHOUT ANY WARRANTY; without even the implied warranty of
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
:: GNU General Public License for more details.
:: 
:: You should have received a copy of the GNU General Public License
:: along with gAutoy.  If not, see <http://www.gnu.org/licenses/>.
:: 
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: @package      gAutoy
:: @file         build.bat
:: @author       Sergiy Gogolenko
:: @license      GPLv3
::
:: Creates exe for targetAssist
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

python setup.py install
python setup.py py2exe
if not exist "..\..\dist" mkdir ..\..\dist
copy /Y .\dist\app.exe          ..\..\dist
copy /Y .\targetAssist.json     ..\..\dist
copy /Y ..\..\third-party\*     ..\..\dist
:: del  /s /q .\dist .\build
rm -rf .\dist .\build
