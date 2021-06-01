
Target Processes and Callbacks Manager
======================================

Before any manipulations with callback manager import and configure
``gautoy``

.. code:: python

    import gautoy
    gautoy.core.config.set_option('backend.cbm', 'traceclient')
    gautoy.init_printing()




Configuring
-----------

Callback manager can be configured in a standard way via ``gAutoy``
*configuration options*. To get their list use:

.. code:: python

    gautoy.core.config.describe_option(r'(^|\.)cbm(\.|$)')


.. parsed-literal::

    backend.cbm Back-end for callback manager: ['traceclient']
        [default: traceclient] [currently: traceclient]
    
    
    

So far we support only ``traceclient`` as a CBM backend.

Usage
-----

CBM API bacics
~~~~~~~~~~~~~~

CBM can be accessed via ``get_callback_manager()`` function:

.. code:: python

    cbm = gautoy.get_callback_manager()

You can connect to CBM by method ``connect()``

.. code:: python

    cbm.connect()
    cbm




.. raw:: html

    <code>TraceClient v<b>67436800</b> (connection:<b>GNLogger</b>)</code>



To check whether connection was successful use property ``is_connected``

.. code:: python

    cbm.is_connected




.. parsed-literal::

    True



If connection was successful, the set of target processes can be
accessed

.. code:: python

    processes = cbm.processes
    processes




.. raw:: html

    <b><i>38</i> processes</b> (active:<i>BrowserRenderer-NBTEVOEXT_Main</i>)



Further, you can select any process and load its callbacks by methos
``activate()``

.. code:: python

    NBTCarHU = processes.NBTCarHU
    NBTCarHU.activate()
    NBTCarHU




.. raw:: html

    <code>process <u><b>NBTCarHU</b></u> (callbacks:<i>37</i>; active)</code>



Use property ``is_active`` to check whether scopes were loaded

.. code:: python

    processes.NBTCarHU.is_active




.. parsed-literal::

    True



After callbacks are load, you can call them as local process methods

.. code:: python

    NBTCarHU.CScreenshotControllerBase_CallBack_doScreenShot(1)

If you do not need CBM connection, you can disconnect:

.. code:: python

    cbm.disconnect()
    cbm.is_connected




.. parsed-literal::

    False



Doing callbacks
~~~~~~~~~~~~~~~

Method 1: Use ``with`` statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the easiest way to do callbacks. ``with`` statement API includes
guards that automatically connect to CBM, activate process before
entering into block and disconnect on exit (if it was connected before
``with``). In this case you have to obtain callbacks from the specified
process by means of function ``get_callbacks()``.

Cell below demonstraits how to take screenshot by this method:

.. code:: python

    with gautoy.get_callbacks('NBTCarHU') as cb:
        cb.CScreenshotControllerBase_CallBack_doScreenShot(1)
    cbm.is_connected




.. parsed-literal::

    False



**Note**: after exit from ``with``-section we are disconnected as it was
on entrance

Method 2: Use general CBM API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See basic CBM API above.

Method 3: Harman ``TraceClient`` API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

@TBA

Examples
--------

For more examples see `cells
collection <../gAutoy-cells-collection.ipynb>`__.
