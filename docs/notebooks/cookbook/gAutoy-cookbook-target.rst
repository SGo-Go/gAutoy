
Target
======

Before any manipulations with targets import and configure ``gautoy``

.. code:: python

    import gautoy
    gautoy.core.config.set_option('target.ip', '196.1.1.1')




Configuring
-----------

Target access can be configured in a standard way via ``gAutoy``
*configuration options*. To get their list use:

.. code:: python

    gautoy.core.config.describe_option('target')


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
    
    
    

As you can see, by default we use SSH connect with
```paramiko`` <http://www.paramiko.org/>`__ library to get access to
target. Use ``backend.target`` option to change this behaviour.

Basic use
---------

To get access to the default target use function ``get_target()`` which
returns target object. If you want to manipulate with several targets
with different IPs use function ``new_target()``:

Set of target object methods is similar to the set of standard ``sys``
library functions.

In the cell below we copy ``/opt/nav/eceusa/bin/navigation.ini`` from
target with IP ``172.30.136.138`` to the default target.

.. code:: python

    target = gautoy.new_target('172.30.136.138')
    target.get(r'/opt/nav/eceusa/bin/navigation.ini', '.') # copy navigation.ini from target to local CWD
    # !cat -n navigation.ini
    target = gautoy.get_target()
    target.system(r'mount -uw /fs/sda0')                   # mount /fs/sda0 to make it writable
    target.put('navigation.ini', r'/opt/nav/eceusa/bin')   # copy local navigation.ini to target
    # clean up temporary local navigation.ini
    !rm navigation.ini

Examples
--------

For more examples see `cells
collection <cells/gAutoy-cells-target.ipynb>`__.
