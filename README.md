<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />

# `gAutoy`: *G*PL licensed framework for developers employed in *AUTO*motive industr*Y* (`Python` *TOY* for navigation system developers and QAs)

<!-- * auto-gen TOC: -->
<!-- {:toc} -->

## Introduction

### Tiny description
<!-- Preliminaries -->

This module customizes access to
[`Harman`](http://www.harman.com/) [`CNLogger`](mailto:TraceClientHelp@harman.com)/[`TraceClient`](mailto:TraceClientHelp@harman.com),
targets (processing units in cars),
[`GoogleMaps`](https://maps.google.com/),
and has a potential to be expanded on
other tools for automotive software development.
In addition to conventional Python environments, 
it supports notebook apps
like [`IPython notebook`](http://ipython.org/notebook.html)
and its up-to-date fork [`Jupyter`](http://jupyter.org/).

Combined with the [`Jupyter`](http://jupyter.org/)/[`IPython`](http://ipython.org/notebook.html) and immence set of `Python` libraries,
it creates convenient uniform environment for analysing traces
and manipulating automotive software/hardware.

Though more work is still needed to make `gAutoy` a unification tool-of-choice
in the automotive software community,
we are on our way towards this goal.

### Motivation

Automotive software development is related to extensive use of different legacy tools,
which are not customized under a single convenient environment.
We designed `gAutoy` with an attempt to fill this gap,
enabling you to manage different tasks in a single environment.

#### Purpose 

`gAutoy` was developed with the following goals in mind:

- **automated** *issue reproduction, testing, and analysis*
- **"live" documentation**
  (provide a unified, customizable, and convenient environment for
  *creating documents that combine explanatory text with live codes*
  driven by automotive software development utils)
- **integration** of automotive software development utils **with IDEs** 

#### Target audience

This tool is aimed to serve primarily to the following categories of people involved in automotive software industry:

- smart and **"lazy"** QA specialists who are interested in testing process automation
- ~~allure and~~ flabby developers who knows `Python`

## Installation

Read details on installation process in
[INSTALL](https://github.com/SGo-Go/gAutoy/blob/master/docs/INSTALL.rst)
or on [the documentation site](http://gautoy.readthedocs.org/en/latest/INSTALL.html).

## Examples

For **quick start** We welcome users to start study `gAutoy` with the
[**Cookbook**](http://nbviewer.ipython.org/urls/raw.github.com/sgo-go/gAutoy/master/docs/notebooks/gAutoy-doc-index.ipynb) --
a tiny introductory tutorial for those, who wish to get an at-a-glance impression of the `gAutoy`.

In addition, we collected some notable
[`IPython notebook`](http://ipython.org/notebook.html)/[`Jupyter`](http://jupyter.org/) cells in
[this notebook](http://nbviewer.ipython.org/urls/raw.github.com/sgo-go/gAutoy/master/docs/notebooks/gAutoy-doc-index.ipynb).
These can serve as introductory examples too. 

Find more simple examples [here](docs/EXAMPLES.rst). For sophisticated examples,
we refer to the [`utils`](https://github.com/SGo-Go/gAutoy/tree/master/utils) folder.


## API Reference

Complete documentation is available [here](http://gautoy.readthedocs.org/en/latest/index.html).
For `gAutoy` API details see [API Reference](http://gautoy.readthedocs.org/en/latest/api/index.html).

<!-- The tool is not properly documented yet. -->

Use question mark in notebooks
(or `.__doc__` in interactive `Python` console)
to get dynamic info about class, method, function, and/or magic of interest.
<!-- @TODO -->

## TODO list

### Urgent

The following features are not extremely time-consumung, but very "handy":

- [`Python 3`](https://docs.python.org/3/) support
- [`Jupyter`](http://jupyter.org/) (so far works fine with `Jupyter 4` and `IPython 3.2.1+`)
- ~~`set_option` function to specify package options (similar to [this](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.set_option.html))~~ (mostly done)
- Enhanced [RegExp](https://en.wikipedia.org/wiki/Regular_expression) support for log messages:
  make it consistent with `Python` [`re`](https://docs.python.org/2/library/re.html);
  enhanced C format parsing: use [parse](https://pypi.python.org/pypi/parse)
- Unicode support
- Simple plugins for [`Sublime`](http://www.sublimetext.com/) and [`Emacs`](https://www.gnu.org/software/emacs/)
- ~~multi-line patterns with multi-occurances (so far use only single occurance in multi-line)~~ (mostly done by power taking syntax)
- improve [`KML`](https://kml-samples.googlecode.com/svn/trunk/interactive/index.html) viewer
  using [OpenLayers 3](http://openlayers.org/) as map API and [blogspot](http://googlemapsmania.blogspot.com/) collection as examples
  (see more on `KML` [here](https://developers.google.com/kml/))
- Full support of [`pandas`](http://pandas.pydata.org/)-like wraps for traces
- Documentation (fix API description, more examples)
- [`pip`](https://pypi.python.org/pypi) and [`conda`](http://conda.pydata.org/docs/) installation
  
<!-- http://openlayers.org/en/v3.11.2/examples/kml-earthquakes.html -->
<!-- http://openlayers.org/en/v3.11.2/examples/vector-layer.html -->

<!-- https://github.com/pydata/pandas/tree/master/pandas/core -->
<!-- http://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang/ -->
<!-- https://www.chromium.org/developers/sublime-text#TOC-Example-plugin -->
<!-- http://pandas.pydata.org/pandas-docs/version/0.16.2/tutorials.html -->
<!-- http://stackoverflow.com/questions/16818871/extracting-value-and-creating-new-column-out-of-it -->

### Other (either require much effort or barely important)

The following features are ordered by usefulness and usually take considerable time to implement:

- Link log massages and source codes: use [`Clang` parser binds](https://pypi.python.org/pypi/clang/)
- Play with [`C++ Cling`](https://root.cern.ch/cling) [kernel](https://github.com/minrk/clingkernel)
  (and [other](https://github.com/ipython/ipython/wiki/IPython-kernels-for-other-languages))
- Extend loggers support with: [`dlt-viewer`](https://github.com/mikelima/dlt-viewer), etc
- Anvanced plugins for [`Sublime`](http://www.sublimetext.com/) and [`Emacs`](https://www.gnu.org/software/emacs/) editors
  Optional: plugins for IDEs (e.g., `Eclipse`, `MS VS`, etc)
- Add [notebook widgets](http://nbviewer.ipython.org/github/quantopian/ipython/blob/master/examples/Interactive%20Widgets/Index.ipynb) for `GoogleMaps`
- create custom [`IPython`]()
  and [`Jupyter`](http://stackoverflow.com/questions/32320836/how-do-i-get-ipython-profile-behavior-from-jupyter-4-x)
  profiles/[configs](http://jdfreder-notebook.readthedocs.org/en/latest/config.html)
- better support of MOST function catalogs (e.g., input and output parameters for MOST function calls)

<!-- http://code.tutsplus.com/tutorials/how-to-create-a-sublime-text-2-plugin--net-22685 -->
<!-- http://www.sublimetext.com/docs/plugin-examples -->
<!-- http://www.sublimetext.com/docs/api-reference -->
<!-- https://www.chromium.org/developers/sublime-text -->


## Contributors and Contacts

Email: <sergiy.gogolenko@gmail.com> (Sergiy Gogolenko)

So far only one contributor.

## Note

:bangbang: :warning: | This repo excludes parts of the code related to legacy tools APIs and other bits that may violate NDAs of BMW, Harman, and Luxoft.
:---: | :---



## License

See the [LICENSE](https://github.com/SGo-Go/gAutoy/tree/master/LICENSE.md) file
for license rights and limitations ([GPLv3](https://www.gnu.org/licenses/gpl.txt)).

[**`gAutoy`**](https://github.com/SGo-Go/gAutoy) Copyright &copy; 2015 [**SGogolenko**](mailto:sergiy.gogolenko@gmail.com)

<!-- .ipython/profile_default/static/custom/custom.cs -->

<!-- [Python Crash Course](http://nbviewer.ipython.org/urls/bitbucket.org/cfdpython/cfd-python-class/raw/master/lessons/00_Quick_Python_Intro.ipynb) -->

<!-- from IPython.core.display import HTML -->
<!-- def css_styling(): -->
<!--     styles = open("../styles/custom.css", "r").read() -->
<!--     return HTML(styles) -->
<!-- css_styling() -->
<!-- http://www.heapoverflow.me/question-resizing-images-to-fit-width-in-ipython-21121082 -->
