#!/usr/bin/env python
# Setup for PollyReports

from distutils.core import setup

long_description = """\
Report Generation Module
------------------------

PollyReports.py provides a set of classes for database report writing.  It
assumes that you are using Reportlab to do PDF generation, but can work with
any "canvas-like" object as desired.

PollyReports provides the following framework for report generation:

A Report object has a data source bound to it at instantiation.  One or more
Band objects (at least, a detail Band) must be added to it, and then the
generate() method will be called to process the data source.  The data source
must be an iterator that produces objects that can be accessed via []
operations, meaning mainly dict, list, and tuple types, i.e. the most common
types of records returned by standard database modules.  The detail band is
generated() once for each row.

Band objects contain a list of Elements (generally at least one) which define
how data from the row should be printed.  An Element may print any normal data
item or label and may be subclassed to handle other things like images.
Generating a band in turn calls Element.generate() for each element, producing
a list of Renderers with the first item in the list being the overall height of
the band.  The height is used to decide if the band will fit on the current
page; if not, a new page will be created first.  When the page is finally ready
for the band, Renderer.render() will be called for each Renderer in the element
list in order to actually render the data.

This version is written for Python 2.7, but should be easily adapted to Python 3.
"""

setup(

    name = "PollyReports",
    version = "1.1",
    author = "Chris Gonnerman",
    author_email = "chris@gonnerman.org",
    url = "http://newcenturycomputers.net/projects/pollyreports.html",

    description = "Report Generation Module",
    long_description = long_description,
    py_modules = ["PollyReports"],
    keywords = "database report",

    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Printing",
    ],
)

# end of file.
