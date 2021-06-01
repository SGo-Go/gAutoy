
Domain for manipulations with maps
==================================

Basic use
---------

First of all, load ``gautoy`` and confidure domain ``map``

.. code:: python

    import gautoy
    from gautoy import pattern
    gautoy.core.config.set_option('domain.map.template_folder',  r'd:/dev/github/gAutoy/gautoy/domain/maps/jinja2')
    gautoy.core.config.set_option('domain.map.info_text_format', 'markdown')
    gautoy.core.config.set_option('domain.map.height', '300')

Central class in the domain ``map`` is ``BaseMapHolder``. It represents
the map instance which can be filled with labels (method ``new_label``)
and paths (method ``new_path``). See example below:

.. code:: python

    from gautoy.domain.maps import *
    
    gmap = BaseMapHolder(default_output = 'test_gmaps.html') # create basic map and store it 'test_gmaps.html'
    path = []
    for coos, name, descr, icon, color in (((48.965299, 37.816164), 'Start', 'An *accident* was here', 'turnaround', None),
                                           ((48.965909, 37.810709), 'Progress', 'Doctors **fixed** it here', None, None),
                                           ((48.969600, 37.807539), 'Finish', 
                                            "They _left_ patiend here with\n\n- pizza\n- cheery mood", None, 'green'),):
        # add labels on the map
        gmap.new_label(coos, name = name, description = descr, icon = icon, color = color)
        # fill up path with labels coordinates
        path.append(coos) 
    # add path that connects these labels
    gmap.new_path(path, name='Guidance',color='black', weight=1)
    
    gmap # show map




.. raw:: html

    <iframe src="test_gmaps.html"  width="100%" height="300"></iframe>



Filling maps with the information from traces
---------------------------------------------

``BaseMapHolder`` instances (in combination with decorator
``patternic``) are particularly convenient for creating maps on the
basis on log messages. The following code shows how to define class
``MapWithRoute`` that extracts routes from traces into the map.

.. code:: python

    logs = gautoy.get_logger()
    
    from gautoy.domain.maps import BaseMapHolder
    
    @pattern.patternic
    class MapWithRoute(BaseMapHolder):
        def __init__(self, *args,**kwargs):
            super(MapWithRoute, self).__init__(*args,**kwargs)
            self.car_position = 0,0
            self.curr_route_id = -1
            self.curr_route = None
    
        @pattern.handler(r'-- new car position: ts[%d] route[%d] lon=%d lat=%d linkId=%d heading=%f link.heading=%f',
                         ['ts', 'route', 'lon_WGS84', 'lat_WGS84', 'linkId', 'heading', 'link_heading'])
        def storeCarPosition(self,r): 
            self.car_position = gautoy.converter.WGS84_to_latlon(r.lon_WGS84, r.lat_WGS84)
            route_id = int(r.route)
            if route_id != self.curr_route_id: 
                self.curr_route_id = route_id
                self.curr_route = self.new_path([], weight=2, name='Route {0}'.format(self.curr_route_id))
                if len(self.paths) >= 2: self.curr_route.append(self.paths[-2].path[-1])
            self.curr_route.append(self.car_position)

Next cell illustrates class that shows positions on the routes where
screenshots were taken.

.. code:: python

    import datetime
    patternDoingScreenshot = pattern.compile(r'Doing screenshot with filename: '\
                                             r'(?P<fullname>(?P<name>screenshot_(?P<datetime>(?P<date>\d+)-(?P<time>\d+))'\
                                             r'_(?P<type>.+))(?P<ext>\.png))',
                                             parsers = {
                                                 'datetime': lambda d: datetime.datetime.strptime(d, '%Y%m%d-%H%M%S'),
                                                 'date'    : lambda d: datetime.datetime.strptime(d, '%Y%m%d').date(),
                                                 'time'    : lambda d: datetime.datetime.strptime(d, '%H%M%S').time()},
                                             formatters = {
                                                 'datetime': lambda d: d if isinstance(d, basestring) else d.strftime('%Y%m%d-%H%M%S'),
                                                 'date'    : lambda d: d if isinstance(d, basestring) else d.strftime('%Y%m%d'),
                                                 'time'    : lambda d: d if isinstance(d, basestring) else d.strftime('%H%M%S')}
                                            )
    
    @pattern.patternic
    class Notifier(MapWithRoute): # inherit from class which stores current car position
        def __init__(self, log, *args, **kwargs): 
            super(Notifier, self).__init__(*args, **kwargs)
            # Walk immediately inside constructor to fill class up with log info
            self.walk(log)
    
        def message(self, msg): 
            # Decorate info string with current car position at the bottom
            return ('{1}\n\n<small style=\\\"color:gray\\\">{0[0]:.5f}, {0[1]:.5f}</small>'.format(self.car_position, msg))
    
        @pattern.handler(patternDoingScreenshot(type='HU1'))
        def handleDoingScreenshot(self,r): 
            if r.date != datetime.date.today(): 
                descr = self.message("""
    name  : `{0.fullname}`
    date  : *{0.date}*
    today : *{1}*
    """.format(r, datetime.date.today()))
                self.new_label(self.car_position, icon='screenshot', name = 'Screenshot', description=descr)
    
    Notifier(logs, default_output = 'notifier_gmaps.html')




.. raw:: html

    <iframe src="notifier_gmaps.html"  width="100%" height="300"></iframe>


