PollyReports.py
Copyright (c) 2012 Chris Gonnerman
All Rights Reserved
See the LICENSE file for more information.

------------------------------------------------------------------------------

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

As noted above, PollyReports expects a Reportlab-like canvas interface.  The
module has been kept as clean as possible, so that, though I don't actually
recommend it, it would not be insane to say

    from PollyReports import *

Importing only what you expect to use is still a better idea, of course.

