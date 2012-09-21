#!/usr/bin/env python
# Setup for PollyReports

from distutils.core import setup

long_description = """\
PollyReports.py
---------------

**Band-oriented PDF report generation from database query**

PollyReports.py provides a set of classes for database report writing.  It
assumes that you are using Reportlab to do PDF generation, but can work with
any "canvas-like" object as desired.

PollyReports provides a framework for report generation.  The developer
instantiates a Report object, passing it a data source and passing or assigning
one or more Band objects.  A Band, in turn, will contain a list of Elements
representing data items, labels, or system variables which will be printed.
When the Report object is fully populated, its generate() method is called,
passing in a Reportlab Canvas object (or any object providing a similar interface);
the Report object then consumes the data source and renders the various Bands
of Elements into the Canvas object.

The data source must be an iterator that produces objects that can be accessed
via [] operations, meaning mainly dict, list, and tuple types, i.e. the most
common types of records returned by standard database modules.

This version is written for Python 2.7, but should be easily adapted to Python 3.

Development versions of this module may be found on Github_.

.. _Github: https://github.com/Solomoriah/PollyReports
"""

setup(

    name = "PollyReports",
    version = "1.6.5",
    author = "Chris Gonnerman",
    author_email = "chris@gonnerman.org",
    url = "http://newcenturycomputers.net/projects/pollyreports.html",

    description = "Band-oriented PDF report generation from database query",
    long_description = long_description,
    py_modules = ["PollyReports"],
    keywords = "database report",

    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Printing",
    ],
)

# end of file.
