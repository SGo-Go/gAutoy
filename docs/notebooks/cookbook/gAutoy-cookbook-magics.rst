
Magics
======

So far ``gAutoy`` supports only 2 core magics: ``%%gautoy_bash`` and
``%gautoy_screenshot``. The former allows to run ``ksh`` codes on the
targets, while the latter serves as in-place screenshot taker. Upon
request we can introduce more core magics later.

Core magics can be **imported** directly from ``gautoy`` package

.. code:: python

    import gautoy
    gautoy.core.config.set_option('target.ip', '196.1.1.1')




Taking screenshots with ``%gautoy_screenshot``
----------------------------------------------

Line magic ``%gautoy_screenshot`` helps to take screenshots easily. Take
help on this magic with option ``-h``.

.. code:: python

    %gautoy_screenshot -h


.. parsed-literal::

    usage: __main__.py [-h] [-l LOGIN] [-p PASSWORD] [-ne] [-c] [-o OUTPUT] [host]
    
    positional arguments:
      host
    
    optional arguments:
      -h, --help            show this help message and exit
      -l LOGIN, --login LOGIN
                            Target login
      -p PASSWORD, --password PASSWORD
                            Target password
      -ne, --no-embed       Embed image to notebook
      -c, --close-traceclient
                            Close TraceClient after callback that takes screenshot
      -o OUTPUT, --output OUTPUT
                            Output folder
    

To take a screenshot simply write

.. code:: python

    %gautoy_screenshot



.. image:: gAutoy-cookbook-magics_files%5CgAutoy-cookbook-magics_7_0.png




.. parsed-literal::

    ['screenshot_20000101-005432_HU1.png']



This magic returns a list of taken screenshots names. You can suppress
screenshots insertion and manipulate screenshots names like this:

.. code:: python

    screenshots = %gautoy_screenshot -ne
    print('Received screenshots: %s' % ','.join(screenshots))


.. parsed-literal::

    Received screenshots: screenshot_20000101-005452_HU1.png
    

Remote run of scripts on target via ``telnet`` connect with magic ``%%bash_target``
-----------------------------------------------------------------------------------

This magic allows to run *non-interactive scripts* on targest. It
establishes ``Telnet`` connect and runs ``ksh/bash`` codes from cell on
it.

Basic use
^^^^^^^^^

Here is a basic cell where we try to find lines with text ``rse-`` in
``/opt/nav/eceusa/bin/navigation.ini``.

.. code:: python

    %%gautoy_bash
    
    cat -n /opt/nav/eceusa/bin/navigation.ini | grep "rse-" 




.. raw:: html

    <div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="color: #888888">    52: ;invert-reverse-signal = true</span>
    <span style="color: #888888">   348: ln-pathmapper-minimum-distance-reverse-mapping        = 250.0</span>
    </pre></div>
    



Configuring and advanced ``%%gautoy_bash`` use
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default magic parameters are taken from ``gAutoy`` *configuration
options*. E.g., the cell below sets ``%%gautoy_bash`` output style to
``murphy``

.. code:: python

    gautoy.core.config.set_option('display.nb.code_highlight', 'murphy')

But you can specify them in the *magic's config line* as well. To get
help on the magic config line parameters use option ``-h``:

.. code:: python

    %%gautoy_bash -h
     


.. parsed-literal::

    usage: __main__.py [-h] [-l LOGIN] [-p PASSWORD] [-w WAIT] [-i]
                       [--prompt PROMPT] [-s STYLE] [-n] [-v VERBOSE]
                       [host]
    
    positional arguments:
      host
    
    optional arguments:
      -h, --help            show this help message and exit
      -l LOGIN, --login LOGIN
                            Target login
      -p PASSWORD, --password PASSWORD
                            Target password
      -w WAIT, --wait WAIT  Time to wait [in sec] before closing connection
      -i, --no-exit         Skip auto-exit (caution: exit must be done explicitely
                            in last cell's line)
      --prompt PROMPT       Regex for target shell prompts [use for correct syntax
                            highlight]
      -s STYLE, --style STYLE
                            Output style schema
      -n, --lineno          Display line number
      -v VERBOSE, --verbose VERBOSE
                            Verbose level [0 - no output; 1 - `sh` output]
    

E.g., if you with you can deepen the output level with option ``-v 2``
and change output style with ``-s native``.

.. code:: python

    %%gautoy_bash -s native -v 2
    
    cat -n /opt/nav/eceusa/bin/navigation.ini | grep "rse-" 




.. raw:: html

    <div class="highlight" style="background: #202020"><pre style="line-height: 125%"><span style="color: #aaaaaa">#</span>&gt; cat -n /opt/nav/eceusa/bin/navigation.ini <span style="color: #d0d0d0">|</span> grep <span style="color: #ed9d13">&quot;rse-&quot;</span> 
    
    <span style="color: #cccccc">    52: ;invert-reverse-signal = true</span>
    <span style="color: #cccccc">   348: ln-pathmapper-minimum-distance-reverse-mapping        = 250.0</span>
    <span style="color: #aaaaaa">#</span>&gt; <span style="color: #24909d">exit</span>
    </pre></div>
    



The following cell resets target with ip ``172.30.136.138``. In this
case we are forced to use option ``-i`` to avoid auto-exit and have to
wait a second before closing ``Telnet`` connection (``-w 1``). We
suppress output (which is irrelevant in this case) with ``-v 0``.

.. code:: python

    %%gautoy_bash 172.30.136.138 -i -w 1 -v 0
    
    OnOffDSICommander appreset




.. raw:: html

    <div class="highlight" style="background: #ffffff"><pre style="line-height: 125%">
    </pre></div>
    



You can make tabular output with specifying output line numbers with
option ``-n``.

.. code:: python

    %%gautoy_bash -n
    
    ls -l /opt/nav/eceusa/bin | sort -nk5 | tail -n4




.. raw:: html

    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">1
    2
    3
    4</pre></div></td><td class="code"><div class="highlight" style="background: #ffffff"><pre style="line-height: 125%"><span style="color: #888888">nrwxrwxrwx  3 root      root       10485760 Jan 01 00:00 DataAccess.Cache</span>
    <span style="color: #888888">-rwxrwxr-x  2 root      root       17351452 Nov 11  2015 NavigationBasic</span>
    <span style="color: #888888">-rwxrwxrwx  1 root      root       56887157 Nov 13  2015 NavNBTEvoController_backup</span>
    <span style="color: #888888">-rwxrwxrwx  1 root      root       56925017 Nov 19  2015 NavNBTEvoController</span>
    </pre></div>
    </td></tr></table>



Examples
--------

For more examples see `cells
collection <cells/gAutoy-cells-magics.ipynb>`__.
