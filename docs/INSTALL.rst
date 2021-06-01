Installation
============

@TODO

.. code-block:: bash

   python setup.py install

Approach 1: Install on top of ``Python(x,y)``
---------------------------------------------

The easiest way to get full functionality of ``gAutoy`` is to install it on top of `Python(x,y) <https://python-xy.github.io>`_.

#. Download last version of `Python(x,y) <https://python-xy.github.io>`_ from the official site
#. Make full installation of `Python(x,y) <https://python-xy.github.io>`_
#. Checkout (or download and unpack) ``gAutoy`` repository::

     $ git clone https://github.com/SGo-Go/gAutoy.git

#. Install ``gAutoy`` with GNU ``make``::

     $ make install

#. (*Optional*) Make and compile documentation::

     $ make docs

Approach 2: Manual installation
-------------------------------

Alternatively, you can install ``Python`` itself and ``Python`` packages one-by-one using ``pip`` command.

*Short list of dependencies*:

- ``argparse``
- ``posixpath``,
- `Pywin32 <https://pypi.python.org/pypi/pypiwin32>`_,
- `Paramiko <http://www.paramiko.org/>`_,
- `telnetlib <https://docs.python.org/2/library/telnetlib.html>`_,
- `jinja2 <http://jinja.pocoo.org/>`_,
- `lxml <http://lxml.de/>`_

*Optional packages*:

- `PyKML <https://pythonhosted.org/pykml/>`_, 
- `simplekml <http://www.simplekml.com/en/latest/gettingstarted.html>`_,
- `NumPy <http://www.numpy.org/>`_,
- `SciPy <http://www.scipy.org/>`_,
- `pandas <http://pandas.pydata.org/>`_,
- `Flask <http://flask.pocoo.org/>`_,
- `simplejson <https://pypi.python.org/pypi/simplejson/>`_,
- `PyQt4 <https://pypi.python.org/pypi/PyQt4>`_,
- `pygments <http://pygments.org/>`_,
- `markdown2 <https://github.com/trentm/python-markdown2>`_,
- ``win32com``

Example of packages installation via `pip`::

  pip install markdown2
  pip install simplejson
  
For *documenting* one also needs to install:

- ``recommonmark``
