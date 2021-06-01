
Classes for work with ``MOST`` protocol function catalogs
=========================================================

Domain ``most`` contains classes that make access to and use of function
catalogs easier.

In order to use domain ``most``, import it from ``gautoy`` package.

.. code:: python

    import gautoy,os
    from gautoy import pattern
    gautoy.init_printing()
    from gautoy.core.output import pprint
    
    from gautoy.domain.most import *

Loading and browsing function catalogs
--------------------------------------

Function catalogs can be loaded from ``*.hbfc``-files. The following
cell shows how to load data from several ``*.hbfc`` into ``Python``
variable ``mostFC``:

.. code:: python

    EVO_sources_foulder = r'd:\dev\NBTevo_DevDef'
    mostFC = gautoy.domain.most.MOSTFuncCatalog().load_hbfc( os.path.join( EVO_sources_foulder, r'api', r'nav', r'ctrl', 
                                                                           r'prj', r'nbt', r'most',
                                                                           r'hudterminal', r'HUDTerminal_0x00.hbfc') ) \
                                                 .load_hbfc( os.path.join( EVO_sources_foulder, r'api', r'nav', r'ctrl', 
                                                                           r'prj', r'nbt', r'most',
                                                                           r'navstd', r'NavigationStd.hbfc') ) \
                                                 .load_hbfc( os.path.join( EVO_sources_foulder, r'api', r'nav', r'ctrl', 
                                                                           r'prj', r'nbt', r'most',
                                                                           r'mapctrl', r'MapControl.hbfc') ) \
                                                 .load_hbfc( os.path.join( EVO_sources_foulder, r'deliveries', r'nbt', r'B140', 
                                                                           r'omap', r'api', r'nbt', r'candi', r'most',
                                                                           r'sys', r'KombiInterface_0x00.hbfc') )

As the variable ``mostFC`` is created, one may use it to access
information about MOST function block and functions. It is possible to
use both memonic names of blocks/functions and theis IDs. The first
index stands for block and the second stands for function.

.. code:: python

    mostFC.HUDTerminal_0x00




.. raw:: html

    <code>[82] <b>HUDTerminal_0x00</b><br><i>Hinweis:
    * Die Funktion FktIDs liefert in Abhängigkeit des Verbaus mit dem Steuergerät JNAV alle FktIDs oder ohne Steuergerät JNAV nur 1 FktID (HUDDisplay).</i></code>



.. code:: python

    mostFC.HUDTerminal_0x00.HUDDisplay




.. raw:: html

    <code>[82 C00] <b>HUDTerminal_0x00.HUDDisplay</b><br><i>Stellt applikationsspezifische Informationen auf dem HUDDisplay dar.</i></code>



.. code:: python

    mostFC[0x82]




.. raw:: html

    <code>[82] <b>HUDTerminal_0x00</b><br><i>Hinweis:
    * Die Funktion FktIDs liefert in Abhängigkeit des Verbaus mit dem Steuergerät JNAV alle FktIDs oder ohne Steuergerät JNAV nur 1 FktID (HUDDisplay).</i></code>



.. code:: python

    mostFC[0x82][0xC00]




.. raw:: html

    <code>[82 C00] <b>HUDTerminal_0x00.HUDDisplay</b><br><i>Stellt applikationsspezifische Informationen auf dem HUDDisplay dar.</i></code>



Patterns for ``MOST`` traces
----------------------------

Domain ``most`` contains a pattern ``MOSTPattern`` which allows not only
search but also encode/decode content of MOST traces by means of
``MOSTFuncCatalog`` instances.

To benefit ``MOSTPattern`` one should enable field ``Comment`` in the
option ``display.log.output``

.. code:: python

    gautoy.core.config.set_option(r'display.log.output', 'Comment TimeStamp Message')
    logs = gautoy.get_logger()

The following cell lists MOST traces where the MapScale was set to 2.

.. code:: python

    MOSTPattern(mostFC.MapControl.MC_MapScale(2), opCode = MOSTTypes.OP_SET).findall(logs)




.. raw:: html

    <small><table style="width:100%"><tr><td style="border:1px solid #EEE;"><code>[set]1:<i>MapControl.MC_MapScale</i>()</code></td><td style="color:#888;border:1px solid #EEE;">532.142</td><td style="border:1px solid #EEE;"><i></i><b>[0022][MSS] [2022->2020] DA 01 220 0 0001 02</b><i></i></td></tr></table></small>



Next cell shows log entries for fail MOST calls in function block
``NavigationStd`` on the ``0`` device

.. code:: python

    MOSTPattern(mostFC.NavigationStd, device=0, opCode = MOSTTypes.OP_ERROR).findall(logs)




.. raw:: html

    <small><table style="width:100%"><tr><td style="border:1px solid #EEE;"><code>[<font color="red">ERR</font>]0:<i>NavigationStd.<font color="gray">Unspec</font></i>()</code></td><td style="color:#888;border:1px solid #EEE;">506.522</td><td style="border:1px solid #EEE;"><i></i><b>[0021][MSS] [2021->2022] 52 00 001 F 0004 20100C87</b><i></i></td></tr><tr><td style="border:1px solid #EEE;"><code>[<font color="red">ERR</font>]0:<i>NavigationStd.<font color="gray">Unspec</font></i>()</code></td><td style="color:#888;border:1px solid #EEE;">506.939</td><td style="border:1px solid #EEE;"><i></i><b>[0021][MSS] [2021->2022] 52 00 001 F 0004 20100C64</b><i></i></td></tr><tr><td style="border:1px solid #EEE;"><code>[<font color="red">ERR</font>]0:<i>NavigationStd.<font color="gray">Unspec</font></i>()</code></td><td style="color:#888;border:1px solid #EEE;">522.522</td><td style="border:1px solid #EEE;"><i></i><b>[0021][MSS] [2021->2022] 52 00 001 F 0004 20100C87</b><i></i></td></tr><tr><td style="border:1px solid #EEE;"><code>[<font color="red">ERR</font>]0:<i>NavigationStd.<font color="gray">Unspec</font></i>()</code></td><td style="color:#888;border:1px solid #EEE;">522.939</td><td style="border:1px solid #EEE;"><i></i><b>[0021][MSS] [2021->2022] 52 00 001 F 0004 20100C64</b><i></i></td></tr><tr><td style="border:1px solid #EEE;"><code>[<font color="red">ERR</font>]0:<i>NavigationStd.<font color="gray">Unspec</font></i>()</code></td><td style="color:#888;border:1px solid #EEE;">538.522</td><td style="border:1px solid #EEE;"><i></i><b>[0021][MSS] [2021->2022] 52 00 001 F 0004 20100C87</b><i></i></td></tr><tr><td style="border:1px solid #EEE;"><code>[<font color="red">ERR</font>]0:<i>NavigationStd.<font color="gray">Unspec</font></i>()</code></td><td style="color:#888;border:1px solid #EEE;">538.939</td><td style="border:1px solid #EEE;"><i></i><b>[0021][MSS] [2021->2022] 52 00 001 F 0004 20100C64</b><i></i></td></tr><tr><td style="border:1px solid #EEE;"><code>[<font color="red">ERR</font>]0:<i>NavigationStd.<font color="gray">Unspec</font></i>()</code></td><td style="color:#888;border:1px solid #EEE;">554.522</td><td style="border:1px solid #EEE;"><i></i><b>[0021][MSS] [2021->2022] 52 00 001 F 0004 20100C87</b><i></i></td></tr><tr><td style="border:1px solid #EEE;"><code>[<font color="red">ERR</font>]0:<i>NavigationStd.<font color="gray">Unspec</font></i>()</code></td><td style="color:#888;border:1px solid #EEE;">554.94</td><td style="border:1px solid #EEE;"><i></i><b>[0021][MSS] [2021->2022] 52 00 001 F 0004 20100C64</b><i></i></td></tr><tr><td style="border:1px solid #EEE;"><code>[<font color="red">ERR</font>]0:<i>NavigationStd.<font color="gray">Unspec</font></i>()</code></td><td style="color:#888;border:1px solid #EEE;">570.529</td><td style="border:1px solid #EEE;"><i></i><b>[0021][MSS] [2021->2022] 52 00 001 F 0004 20100C87</b><i></i></td></tr><tr><td style="border:1px solid #EEE;"><code>[<font color="red">ERR</font>]0:<i>NavigationStd.<font color="gray">Unspec</font></i>()</code></td><td style="color:#888;border:1px solid #EEE;">570.94</td><td style="border:1px solid #EEE;"><i></i><b>[0021][MSS] [2021->2022] 52 00 001 F 0004 20100C64</b><i></i></td></tr></table></small>



