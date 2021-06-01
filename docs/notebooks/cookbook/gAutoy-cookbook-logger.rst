
Logger: traces analysis with highly customizable output and callbacks availability
==================================================================================

Before any manipulations with logger import and configure ``gautoy``

.. code:: python

    import gautoy
    gautoy.core.config.set_option('target.ip', '196.1.1.1')

Configuring
-----------

Logger can be configured in a standard way via ``gAutoy`` *configuration
options*. To get their list use:

.. code:: python

    gautoy.core.config.describe_option(r'(^|\.)log(\.|$)')


.. parsed-literal::

    log.message_fields list of fields stored in logger message lines by default (note: DO NOT put "line" in the list)
        [default: TimeStamp Message] [currently: TimeStamp Message]
    
    display.log.output list of displayable output fields (note: field "line" is reserved for line no)
        [default: line TimeStamp Message ] [currently: line TimeStamp Message ]
    
    backend.log Back-end for logger: ['traceclient']
        [default: traceclient] [currently: traceclient]
    
    
    

So far we support only ``traceclient`` as a logger backend.

Usage
-----

Basic logger APIs
~~~~~~~~~~~~~~~~~

To get access to log processor, simply call the function
``get_logger()`` which returns logger frontend instance

.. code:: python

    logs = gautoy.get_logger()

Traces can be **loaded** into backend via fronend's method ``load()``

.. code:: python

    import os
    os.chdir(r'D:\dev\CPM\tickets\summary\source\1766802\EXCH_BUG_300848028_20151113_0414_NA_[NBT]_label_guiding_-_details__X2E (1)\Omap')
    logs.load(r'V527239_2015-11-13[13.13.38]_2015-11-13[13.14.31]_3_NBTEvo_Omap_000_x2eC.xaa')




.. parsed-literal::

    False



Alternatively, backend can receive traces on-flight if logger is
connected to target.

To store traces use method ``save()``

.. code:: python

    logs.save('traces')




.. parsed-literal::

    True



Log search
~~~~~~~~~~

For details of log search see section
`patterns <gAutoy-cookbook-pattern.ipynb>`__.
