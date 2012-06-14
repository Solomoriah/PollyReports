#!/usr/bin/env python
# Setup for PollyReports

from distutils.core import setup, Extension
import sys

# version of this PollyReports.py package
this_version = "1.0"

setup(
    name="PollyReports",
    version=this_version,
    description="PollyReports",
    long_description="Report Generation Module",
    author="Chris Gonnerman",
    author_email="chris@gonnerman.org",
    url="http://newcenturycomputers.net/projects/pollyreports.html",
    py_modules=["PollyReports"],
    keywords="database report",
)

# end of file.
