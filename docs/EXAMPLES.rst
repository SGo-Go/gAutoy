Examples
========

Simple Code Examples
--------------------

Examples are available in `examples <https://github.com/SGo-Go/gAutoy/tree/master/examples/>`_ folder:

- `grabLastTrace.py <https://raw.github.com/SGo-Go/gAutoy/master/examples/grabLastTrace.py>`_

    Grab last trace from `CNLogger`

- `takeScreenshotInPos.py <https://raw.github.com/SGo-Go/gAutoy/master/examples/takeScreenshotInPos.py>`_

    Use callbacks and target API to move carsor to the given position and take screenshot.

- `enabledGVLabelsSummary.py <https://raw.github.com/SGo-Go/gAutoy/master/examples/enabledGVLabelsSummary.py>`_

    Walk through log and collect certain information:
    summarize data about lifetime of GV-lables controlled by `NavNBTEvoController`
    and output GV-lables timeline table
    
- `serviceAvailabilityCallbacks.py <https://raw.github.com/SGo-Go/gAutoy/master/examples/serviceAvailabilityCallbacks.py>`_

    Use callbacks to show `iPark <http://www.autoworldnews.com/articles/14907/20150606/bmw-will-make-finding-parking-spots-easier-through-ipark-service.htm>`_
    service availability areas

- `trace2gmap.py <https://raw.github.com/SGo-Go/gAutoy/master/examples/trace2gmap.py>`_ (deprecated)

    Generate `GoogleMap <https://maps.google.com>`_-based `HTML`/`KML <https://developers.google.com/kml/documentation/kmlreference?hl=en>`_ containing car routes.
    Uses `jinja2 <http://jinja.pocoo.org/>`_ template from `templates <https://github.com/SGo-Go/gAutoy/tree/master/examples/templates/>`_.

In addition, we collected some notable
`IPython notebook <http://ipython.org/notebook.html>`_/`Jupyter <http://jupyter.org/>`_ cells in
`this notebook <http://nbviewer.ipython.org/urls/raw.github.com/sgo-go/gAutoy/master/docs/notebooks/gAutoy-doc-index.ipynb>`_.
These can serve as introductory examples too. 

Utilities
---------

For more sophisticated examples of use,
we refer to the `utils <https://github.com/SGo-Go/gAutoy/tree/master/utils>`_ folder,
which include

- `targetAssist <https://github.com/SGo-Go/gAutoy/tree/master/utils/targetAssist>`_

    (a `PyQT <https://wiki.python.org/moin/PyQt>`_-based tool for managing targets)

- `log2kml <https://github.com/SGo-Go/gAutoy/tree/master/utils/log2kml>`_ with
  `KML viewer <https://rawgit.com/SGo-Go/gAutoy/master/utils/log2kml/kmlviewer/index.html>`_
  (alternatively you drag KML's on `OpenLayers 3 Drag-and-Drop map <http://openlayers.org/en/v3.11.2/examples/drag-and-drop.html>`_ for visualization)
