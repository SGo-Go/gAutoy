
Configuring ``gAutoy``
======================

It is preferable to configure ``gAutoy`` before doing actual
manipulations.

.. code:: python

    import gautoy
    import gautoy.core.config as cf

Target access can be configured in a standard way via ``gAutoy``
*configuration options*. To modify and check config options we provide
``set_option`` and ``get_option`` functions.

E.g., to check target IP use:

.. code:: python

    cf.get_option('target.ip')




.. parsed-literal::

    '127.0.0.1'



to set the new target IP use:

.. code:: python

    cf.set_option('target.ip', '196.1.1.1')

The list of available options can be viewed with the function
``describe_option``.

The following cell lists options for related to target:

.. code:: python

    cf.describe_option('target')


.. parsed-literal::

    target.ssh.shell Console utility for running remote commands via SSH
        [default: plink.exe -ssh] [currently: plink.exe -ssh]
    
    target.prompt regex for target shell prompts
        [default: hu-omap:(\/([a-zA-Z])+)+> ] [currently: hu-omap:(\/([a-zA-Z])+)+> ]
    
    target.ssh.client SSH console
        [default: kitty.exe] [currently: kitty.exe]
    
    target.password Target password
        [default: some_password] [currently: some_password]
    
    target.ssh.max_local_get_file_size Upper bound for file size downloadable without need to invoke SSH utility
        [default: 20000] [currently: 20000]
    
    target.ssh.max_local_put_file_size Upper bound for file size uploadable without need to invoke SSH utility
        [default: 4096] [currently: 4096]
    
    target.host Target ip
        [default: 127.0.0.1] [currently: 196.1.1.1]
        (Deprecated , use `target.ip` instead.)
    
    target.login Target login
        [default: root] [currently: root]
    
    target.ip Target ip
        [default: 127.0.0.1] [currently: 196.1.1.1]
    
    backend.target Back-end for target: ['paramiko', 'putty']
        [default: paramiko] [currently: paramiko]
    
    
    

Note: the new target IP is ``196.1.1.1``

One can reset either sets or indiwidual options to defaults with
``reset_option()``.

.. code:: python

    cf.reset_option('display.nb')

If you wish to reset all options use ``"*"``:

.. code:: python

    cf.reset_option('*')
    cf.get_option('target.ip')




.. parsed-literal::

    '127.0.0.1'


