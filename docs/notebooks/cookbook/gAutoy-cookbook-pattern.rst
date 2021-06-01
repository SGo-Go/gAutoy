
Patterns : Pattern Specification, Patternic Algebra, and Improved Search
========================================================================

In skilly hands, ``gAutoy`` patterns provide efficient mechanism for
spotlighting relevant information from logs. ``gAutoy`` patterns were
inspired by ```Python`` regular
expressions <https://docs.python.org/2/library/re.html>`__ and have
similar functionality advanced and adopted to the purposes of log search
(in contrast to convential text search with regexps).

Prerequisites
-------------

Before trace analysis with ``gautoy`` pattern facilities, configure
``gautoy``, create logger instance with ``get_logger()`` and load traces
(or connect logger for traces listening)

.. code:: python

    import gautoy
    from gautoy import pattern
    gautoy.init_printing()
    from gautoy.core.output import pprint
    #gautoy.core.config.set_option('target.ip', '196.1.1.1')
    logs = gautoy.get_logger()
    
    import os
    #os.chdir(r'')
    logs.load(r'D:\dev\CPM\tickets\summary\source\1766802\EXCH_BUG_300848028_20151113_0414_NA_[NBT]_label_guiding_-_details__X2E (1)\Omap\V527239_2015-11-13[13.13.38]_2015-11-13[13.14.31]_3_NBTEvo_Omap_000_x2eC.xaa')
    
    gautoy.core.config.set_option(r'display.log.output', 'Message TimeStamp')

Defining Patterns
-----------------

Basic patterns
~~~~~~~~~~~~~~

*Basic* (or so called *atomic*) patterns provide basic log search
functionality, and serve as building blocks for specilication of more
complicates patternic structures. ``gAutoy`` provides two ways to define
atomic patterns: via C format strings and via ```Python`` regular
expressions <https://docs.python.org/2/library/re.html>`__. Atomic
patterns of both types can be created with function ``compile()`` from
subpackage ``gautoy.pattern``.

The easiest way to define atomic pattern in ``gAutoy`` is to use **C
format** based patterns. In this case, the user must specify C format
string and the list with mnemonic names for each of the formatted
pattern fields. User does not have control on parsing and formatting of
pattern fields, these are fully driven by C format string. Next cell
specifies pattern for the new car position message:

.. code:: python

    patternCarPosition = pattern.compile(r'-- new car position: ts[%d] route[%d] lon=%d lat=%d linkId=%d heading=%f link.heading=%f',
                                         ['ts', 'route', 'lon_WGS84', 'lat_WGS84', 'linkId', 'heading', 'link_heading'])
    patternCarPosition




.. parsed-literal::

    pattern(r'\-\- new car position: ts\[(?P<ts>\-?\d+)\] route\[(?P<route>\-?\d+)\] lon=(?P<lon_WGS84>\-?\d+) lat=(?P<lat_WGS84>\-?\d+) linkId=(?P<linkId>\-?\d+) heading=(?P<heading>.*) link\.heading=(?P<link_heading>.*)')



C format based pattern for MOST messages has a following definition:

.. code:: python

    pattern.compile(r'[%4X][MSS] [%4X->%4X] %2X %2X %3X %1X %4X %s',
                    ['no', 'from', 'to', 'funcBlock', 'device', 'funcId', 'opCode', 'size', 'data'])




.. parsed-literal::

    pattern(r'\[(?P<no>\-?[0-9A-F]+)\]\[MSS\] \[(?P<from>\-?[0-9A-F]+)\->(?P<to>\-?[0-9A-F]+)\] (?P<funcBlock>\-?[0-9A-F]+) (?P<device>\-?[0-9A-F]+) (?P<funcId>\-?[0-9A-F]+) (?P<opCode>\-?[0-9A-F]+) (?P<size>\-?[0-9A-F]+) (?P<data>.*)')



In contrast, **regexp** based patterns somewhat trickier to define, but
they provide full controll on pattern's parsers and formatters. Here is
a regexp based patterns for MOST messages similar to the previous one:

.. code:: python

    patternMOST = pattern.compile(r"\[([0-9A-F]+)\]\[MSS\] \[(?P<from>[0-9A-F]+)->(?P<to>[0-9A-F]+)] "\
                                  r"(?P<funcBlock>[0-9A-F]+) (?P<device>[0-9A-F]+) (?P<funcId>[0-9A-F]+) "\
                                  r"(?P<opCode>[0-9A-F]) (?P<size>[0-9A-F]+) (?P<data>([0-9A-F][0-9A-F])*)",
                                             parsers = {
                                                 'funcBlock': lambda s: int(s, 16),
                                                 'device'   : lambda s: int(s, 16),
                                                 'funcId'   : lambda s: int(s, 16),
                                                 'opCode'   : lambda s: int(s, 16),
                                                 'size'     : lambda s: int(s, 16),
                                                 'data'     : lambda s: tuple(int(x+y,16) for x,y in zip(s[0::2], s[1::2]))},
                                             formatters = {
                                                 'funcBlock': lambda x: r'{0:02X}'.format(x),
                                                 'device'   : lambda x: r'{0:02X}'.format(x),
                                                 'funcId'   : lambda x: r'{0:03X}'.format(x),
                                                 'opCode'   : lambda x: r'{0:1X}'.format(x),
                                                 'size'     : lambda x: r'{0:04X}'.format(x),
                                                 'data'     : lambda x: ''.join('%02X'%a for a in x),}
                                 )
    patternMOST




.. parsed-literal::

    pattern(r'\[([0-9A-F]+)\]\[MSS\] \[(?P<from>[0-9A-F]+)->(?P<to>[0-9A-F]+)] (?P<funcBlock>[0-9A-F]+) (?P<device>[0-9A-F]+) (?P<funcId>[0-9A-F]+) (?P<opCode>[0-9A-F]) (?P<size>[0-9A-F]+) (?P<data>([0-9A-F][0-9A-F])*)')



Note, some pattern fields are left without parsers and formatters (e.g.,
``data``). These fields are treated as normal strings.

Here is a bit more sophisticated regexp based pattern for message
notifying about screenshots

.. code:: python

    import datetime
    patternDoingScreenshot = pattern.compile(r'Doing screenshot with filename: '\
                                             r'(?P<fullname>(?P<name>screenshot_(?P<datetime>(?P<date>\d+)-(?P<time>\d+))_(?P<type>.+))(?P<ext>\.png))',
                                             parsers = {
                                                 'datetime': lambda d: datetime.datetime.strptime(d, '%Y%m%d-%H%M%S'),
                                                 'date'    : lambda d: datetime.datetime.strptime(d, '%Y%m%d').date(),
                                                 'time'    : lambda d: datetime.datetime.strptime(d, '%H%M%S').time()},
                                             formatters = {
                                                 'datetime': lambda d: d if isinstance(d, basestring) else d.strftime('%Y%m%d-%H%M%S'),
                                                 'date'    : lambda d: d if isinstance(d, basestring) else d.strftime('%Y%m%d'),
                                                 'time'    : lambda d: d if isinstance(d, basestring) else d.strftime('%H%M%S')}
                                            )
    patternDoingScreenshot




.. parsed-literal::

    pattern(r'Doing screenshot with filename: (?P<fullname>(?P<name>screenshot_(?P<datetime>(?P<date>\d+)-(?P<time>\d+))_(?P<type>.+))(?P<ext>\.png))')



Note, in this pattern we use nested groups (e.g., group ``time`` is a
part of group ``datetime``, the latter is a part of ``name`` and
``fullname``). You cannot easily make nested groups inside

In order to narrow search, the user has an opportunity to **specialize**
pattern -- assign certain values to the pattern fields. To do it, simply
list the groups with the new values in brackets as shown below. This
will return you a new narrower pattern.

.. code:: python

    patternMOST(funcId=0xC2F,device=0, size=1, data = [0x1A, 0x10])




.. parsed-literal::

    pattern(r'\[([0-9A-F]+)\]\[MSS\] \[(?P<from>[0-9A-F]+)->(?P<to>[0-9A-F]+)] (?P<funcBlock>[0-9A-F]+) 00 C2F (?P<opCode>[0-9A-F]) 0001 1A10')



Fields also can be accessed by their positions (which is the only way to
access ananymous fields):

.. code:: python

    patternMOST(1,'0018', 6, 0xC2F, size=1, data=[0x1A])




.. parsed-literal::

    pattern(r'\[0018\]\[MSS\] \[(?P<from>[0-9A-F]+)->(?P<to>[0-9A-F]+)] (?P<funcBlock>[0-9A-F]+) (?P<device>[0-9A-F]+) C2F (?P<opCode>[0-9A-F]) 0001 1A')



Advanced searcheable structures and algebra of patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Atomic patterns are not only simple trace search instruments, but also
builing blocks for advanced **searcheable structures**: *multiline
patterns* and *pattern multi-sets* (sets with possible repetitions).
``gAutoy``'s algebra of patterns provides an easy mechanism to construct
both.

Multiline patterns
^^^^^^^^^^^^^^^^^^

We suggest to use multiline patterns, if the user has a situation when
the function/method of interest consequently writes several log
messages, each of which conveys piece of relevant information.

To define multiline patterns, use either bit-wise and ``&`` or
multiplication ``*``:

.. code:: python

    a = pattern.compile('a')
    b = pattern.compile('b')
    x = a & b
    x, a * b




.. parsed-literal::

    (pattern(r'a')&pattern(r'b'), pattern(r'a')&pattern(r'b'))



You can use ``&=`` and/or ``*=`` operations as well. Finally, power
taking operator ``**`` allows to repeat atomic patterns in multiline
pattern

.. code:: python

    x &= a**2
    x




.. parsed-literal::

    pattern(r'a')&pattern(r'b')&pattern(r'a')&pattern(r'a')



Multiline patterns will search groups of closest messages positioned in
the given order. E.g., if the log contains messages
``['c', 'a', 'c', 'a', 'c', 'b', 'c', 'b', 'a', 'b', 'x', 'a', 'x', 'x']``,
pattern ``x`` will return single match with message positions
``(3 ,7, 8, 11)``:

.. code:: python

    log_content = list('cacacbcbabxaxx')
    match_indices = 3,7,8,11
    [log_content[i] for i in match_indices]




.. raw:: html

    ['a', 'b', 'a', 'a']



Pattern multi-sets
^^^^^^^^^^^^^^^^^^

Pattern multi-sets serve the purposes of handling several patterns as a
whole. E.g., to apply several patterns to log in arbitrary order.

To define multiline patterns, use either bit-wise or ``|`` or addition
``+``:

.. code:: python

    x = a + b
    x




.. parsed-literal::

    pattern(r'a') | 
    pattern(r'b')



You can also use ``|=`` and/or ``+=`` operations.

.. code:: python

    x |= a**2 * b
    x




.. parsed-literal::

    pattern(r'a') | 
    pattern(r'b') | 
    pattern(r'a')&pattern(r'a')&pattern(r'b')



More on algebra
^^^^^^^^^^^^^^^

Note that both ways to define patterns -- via arithmetic operators
(``*``, ``+``) and via bit-wise operators (``&``, ``|``) -- are totally
similar.

Next note (for mathematicians), patternic "algebra" is not an algebra in
a common mathematical sense -- it does not define neither algebra, nor
even ring of patterns, though it satisfies most axioms of
non-commutative rings. E.g., it follows associative and distributive
laws, but it does not have additive identity element (so consequently
lacks additive inverses).

.. code:: python

    a = pattern.compile('a')
    b = pattern.compile('b')
    c = pattern.compile('c')
    
    a**2 * (b + c)




.. parsed-literal::

    pattern(r'a')&pattern(r'a')&pattern(r'b') | 
    pattern(r'a')&pattern(r'a')&pattern(r'c')



Search methods
--------------

Conventional search methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Search facilities of basic patterns and patternic structures are similar
(almost 1-2-1) to those provided by ``Python`` regexps. Next table lists
the most popular search methods:

.. raw:: html

   <table>

.. raw:: html

   <tr>

.. raw:: html

   <th>

Method

.. raw:: html

   </th>

.. raw:: html

   <th>

Description

.. raw:: html

   </th>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

``finditer``

.. raw:: html

   </td>

.. raw:: html

   <td>

Return an iterator yielding MatchObject instances over all matches for
the pattern in ``log_frame``. The ``log_frame`` is scanned top-to-down,
and matches are returned in the order found.

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

``findall``

.. raw:: html

   </td>

.. raw:: html

   <td>

Return all matches of pattern in ``log_frame``, as a list of matches.
The ``log_frame`` is scanned top-to-down, and matches are returned in
the order found.

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

``match``

.. raw:: html

   </td>

.. raw:: html

   <td>

If message at the given line ``pos`` in ``log_frame`` matches pattern,
return a corresponding MatchObject instance (otherwise ``None``).

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

``search``

.. raw:: html

   </td>

.. raw:: html

   <td>

Scan through ``log_frame`` looking for the first location where the
pattern produces a match, and return a corresponding MatchObject
instance (otherwise ``None``).

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

Note that all these methods return either MatchObject of MatchObject
lists if succeed. If nothing is found, they return ``None``.

See a couple of examples below

.. code:: python

    patternDoingScreenshot.findall(logs)




.. raw:: html

    <small><table style="width:100%"><tr><td style="border:1px solid #EEE;"><i></i><b>Doing screenshot with filename: screenshot_20151113-131436_HU1.png</b><i></i></td><td style="color:#888;border:1px solid #EEE;">2232.303</td></tr><tr><td style="border:1px solid #EEE;"><i></i><b>Doing screenshot with filename: screenshot_20151113-131437_KOMBI.png</b><i></i></td><td style="color:#888;border:1px solid #EEE;">2233.394</td></tr></table></small>



.. code:: python

    patternDoingScreenshot(type='KOMBI').findall(logs)




.. raw:: html

    <small><table style="width:100%"><tr><td style="border:1px solid #EEE;"><i></i><b>Doing screenshot with filename: screenshot_20151113-131437_KOMBI.png</b><i></i></td><td style="color:#888;border:1px solid #EEE;">2233.394</td></tr></table></small>



.. code:: python

    patternDoingScreenshot.search(logs, pos=100)




.. raw:: html

    <small><table style="width:100%"><tr><td style="border:1px solid #EEE;"><i></i><b>Doing screenshot with filename: screenshot_20151113-131436_HU1.png</b><i></i></td><td style="color:#888;border:1px solid #EEE;">2232.303</td></tr></table></small>



.. code:: python

    patternDoingScreenshot.match(logs, pos=100)

Match objects
~~~~~~~~~~~~~

Match objects does not only allow pretty output in notebook environment,
but also give access to pattern match information user can be interested
in. There are two sorts of match objects: atomic pattern matches and
multi-line pattern matches (Pattern multi-sets do not have own match
type and return individual match objects atomic and multi-line patterns,
they are composed of).

Below is a lists of the most common match object properties:

.. raw:: html

   <table>

.. raw:: html

   <tr>

.. raw:: html

   <th>

Property

.. raw:: html

   </th>

.. raw:: html

   <th>

Description

.. raw:: html

   </th>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

``pattern``

.. raw:: html

   </td>

.. raw:: html

   <td>

Host pattern for this match object.

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

``pos``

.. raw:: html

   </td>

.. raw:: html

   <td>

Line no in the log where the match starts.

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

``endpos``

.. raw:: html

   </td>

.. raw:: html

   <td>

Line no of message which follows the match in the log.

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

Named match fields can be accesssed as attributes for both atomic and
multi-line match objects. In atomic match objects, you can access
messages time stamps and other fields directly as properties.
Information about individual matched messages in multiline match can be
accessed by indices.

.. code:: python

    m = patternDoingScreenshot.search(logs, pos=100)
    if m: print( r'Screenshot "{0}" was taken at {1} (TimeStamp:{2}, line:{3})'.format(m.fullname, m.time, m.TimeStamp, m.pos))


.. parsed-literal::

    Screenshot "screenshot_20151113-131436_HU1.png" was taken at 13:14:36 (TimeStamp:2232.303, line:112524)
    

.. code:: python

    mdatDumpManeuver = pattern.compile(r'MDAT dumpManeuver[%d %d] -----------', ['man_id', 'id'])
    mdatWhereToRoad  = pattern.compile(r'whereTo   [%d][ %d] roadNumber "%s" "%d" "%s" "%s" prio %d', 
                                       ['shit1', 'shit2', 'road_prefix', 'road_no', 'road_part3', 'road_part4', 'prio'])
    
    m = (mdatDumpManeuver & mdatWhereToRoad).search(logs)
    m




.. raw:: html

    <small><table style="width:100%"><tr><td style="border:1px solid #EEE;"><i></i><b>MDAT dumpManeuver[209 177] -----------</b><i></i></td><td style="color:#888;border:1px solid #EEE;">2225.464</td></tr><tr><td style="border:1px solid #EEE;"><i>MDAT   </i><b>whereTo   [3][ 0] roadNumber "US-" "101" "" "-" prio 2</b><i></i></td><td style="color:#888;border:1px solid #EEE;">2225.504</td></tr></table></small>



.. code:: python

    if m: 
        print(r'Maneuver {0} goes to road {1}{2} (track MDAT messages for lines from {3} {4})'.\
              format(m.man_id, m.road_prefix, m.road_no, m.pos, m.endpos))
        print(r'- see message: "{0}" (time stamp:{1})'.format(m[1].Message, m[1].TimeStamp))


.. parsed-literal::

    Maneuver 209 goes to road US-101 (track MDAT messages for lines from 87629 88171)
    - see message: "MDAT   whereTo   [3][ 0] roadNumber "US-" "101" "" "-" prio 2" (time stamp:2225.504)
    

Message waiting
~~~~~~~~~~~~~~~

In order to wait for messages while logger is connected and listens for
trace messages, you can use method ``wait()`` available in atomic
patter. In this method you specify logger and maximum waiting time
(timeout) in seconds. If *timeout lapses* while logger still have not
received message, pattern throws *run-time exception*:

.. code:: python

    line = pattern.compile('x'*10).wait(logs, 10)
    if line: print('{0} {1}'.format(line, logs.Message[line-1]))


::


    ---------------------------------------------------------------------------

    RuntimeError                              Traceback (most recent call last)

    <ipython-input-26-82043016fd19> in <module>()
    ----> 1 line = pattern.compile('x'*10).wait(logs, 10)
          2 if line: print('{0} {1}'.format(line, logs.Message[line-1]))
    

    C:\Python27\lib\site-packages\gautoy-0.1.dev20150731100039-py2.7.egg\gautoy\log\pattern\AtomicMessagePattern.pyc in wait(self, log_frame, timeout)
         72         endpos = log_frame._wait_re(self.logger_pattern(log_frame), timeout)
         73         if endpos is None:
    ---> 74             raise RuntimeError('Pattern waiting timeout is lapsed') # TimeoutError
         75         return endpos
         76 
    

    RuntimeError: Pattern waiting timeout is lapsed


Otherwise (message is found) it returns the line number next to the
observed pattern match.

.. code:: python

    patternCarPosition = pattern.compile(r'-- new car position: ts[%d] route[%d] lon=%d lat=%d linkId=%d heading=%f link.heading=%f',
                                         ['ts', 'route', 'lon_WGS84', 'lat_WGS84', 'linkId', 'heading', 'link_heading'])
    line = patternCarPosition.wait(logs, 10)
    if line: print('{0} "{1}"'.format(line, logs.Message[line-1]))

Assigning callbacks to patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assigning callbacks to patterns allows to handle match objects on flight
(without collecting them in lists). It is particularly useful for
pattern multi-sets (one can use ``finditer()`` method for this purpose
in case of atomic and multi-line patterns).

At first, obtain callable patterns by calling method ``call()`` with
callback function as parameter. And then apply method ``walk()`` for the
composed pattern. See example below:

.. code:: python

    def cb_mdatDumpManeuver(r): print(r'Maneuver {0.man_id} moves to road "{0.road_prefix}{0.road_no}"'.format(r))
    def cb_patternDoingScreenshot(r): 
        if r.date != datetime.date.today(): 
            print(r'Old screenshot "{0.fullname}" (date:{0.date}; today:{1})'.format(r, datetime.date.today()))
    
    ( (mdatDumpManeuver & mdatWhereToRoad).call(cb_mdatDumpManeuver) 
     | patternDoingScreenshot.call(cb_patternDoingScreenshot) ).walk(logs) 


.. parsed-literal::

    Maneuver 209 moves to road "US-101"
    Old screenshot "screenshot_20151113-131436_HU1.png" (date:2015-11-13; today:2015-12-16)
    Old screenshot "screenshot_20151113-131437_KOMBI.png" (date:2015-11-13; today:2015-12-16)
    

Patternic classes
~~~~~~~~~~~~~~~~~

Patternic classes allow to customize pattern handling. In particular,
method ``walk()`` of patternic classes allows to apply methods which
handle patterns in a way simlar to applying callbacks with method
``walk()`` of patternic structures. Moreover, you can inhrerit pattern
handlers from parents.

In order to make class patternic use decorator ``@patternic``. Decorator
``@handler`` allows to define methods that handle patterns.

Next example extends example with callbacks from section *"Assigning
callbacks to patterns"* by printing car pasition in from of information
about message matches.

.. code:: python

    @pattern.patternic
    class WithCarPosition(object):
        def __init__(self, log):
            self.car_position = 0,0
    
        @pattern.handler(patternCarPosition)
        def storeCarPosition(self,r): 
            self.car_position = gautoy.converter.WGS84_to_latlon(r.lon_WGS84, r.lat_WGS84)
    
    @pattern.patternic
    class Notifier(WithCarPosition): # inherit from class which stores current car position
        def __init__(self, log): 
            # Walk immediately inside constructor
            self.walk(log)
            
        def message(self, msg): 
            # Decorate string output with current car position
            print('[lat={0[0]} lon={0[1]}] {1}'.format(self.car_position, msg))
    
        @pattern.handler(patternDoingScreenshot)
        def handleDoingScreenshot(self,r): 
            if r.date != datetime.date.today(): 
                self.message(r'Old screenshot "{0.fullname}" (date:{0.date}; today:{1})'.format(r, datetime.date.today()))
    
        @pattern.handler(mdatDumpManeuver & mdatWhereToRoad)
        def handleWhereToRoad(self,r): self.message(r'Maneuver {0.man_id} moves to road "{0.road_prefix}{0.road_no}"'.format(r))
    
    Notifier(logs) # Run Notifier constructor (which automatically calls ``walk()``)
    None


.. parsed-literal::

    [lat=34.2641583458 lon=-119.234991632] Maneuver 209 moves to road "US-101"
    [lat=34.2630448099 lon=-119.232649729] Old screenshot "screenshot_20151113-131436_HU1.png" (date:2015-11-13; today:2015-12-16)
    [lat=34.2630448099 lon=-119.232649729] Old screenshot "screenshot_20151113-131437_KOMBI.png" (date:2015-11-13; today:2015-12-16)
    

Other
-----

Somtimes it is useful to be aware of pattern which can be used for
search directly inside logger backend. For this purposes you can use
method ``logger_pattern()``

.. code:: python

    print(patternMOST(funcId=0xC2F,device=0, size=1).logger_pattern(logs))


.. parsed-literal::

    \[([0-9A-F]+)\]\[MSS\] \[([0-9A-F]+)->([0-9A-F]+)] ([0-9A-F]+) 00 C2F ([0-9A-F]) 0001 (([0-9A-F][0-9A-F])*)
    
