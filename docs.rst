===========================================
PollyReports -- A Database Report Generator
===========================================

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

As noted above, PollyReports expects a Reportlab-like canvas interface.  

The module has been kept as clean as possible, so that, though I don't actually
recommend it, it would not be insane to say

    ``from PollyReports import *``

Importing only what you expect to use is still a better idea, of course.

Class Structure
===============

In the descriptions below, only methods and properties intended to be "public"
will be described.  I have taken no particular steps to hide the non-public
methods, but I make no representation that I won't change them later.

Of course, I make no representation that I won't change the public interface
either; but it is reasonable to assume that I won't do that as often.

All measurements used in PollyReports are in terms of points, where one point
is equal to 1/72 inch.  In actuality, this is a feature of Reportlab (and of
PDF generation in general), not merely a feature of PollyReports.

Attributes are shown with their default values, if any.

class Report
------------

    ``rpt = Report(datasource)``

    *datasource* must be an iterable object which yields objects that
    can be indexed with [].  A standard database cursor yielding
    lists, tuples, or dicts is the expected case.  When Report.generate()
    is called, this datasource will be consumed one row at a time.

    If the datasource is empty, no output is generated.

    **Methods**

    ``rpt.generate(canvas)``

    The generate method requires a single parameter, which must be a
    Reportlab Canvas object or an object that presents a similar interface.
    As it stands now, the following methods and attributes are the only
    ones being used by PollyReports::

        canvas.drawRightString()
        canvas.drawString()
        canvas.line()
        canvas._pagesize
        canvas.restoreState()
        canvas.saveState()
        canvas.setFont()
        canvas.setLineWidth()
        canvas.setStrokeGray()
        canvas.showPage()
        canvas.translate()

    **Attributes**

    This is where the main work of setting up a Report gets done.
    In a future version, it's entirely possible I may add these things
    to the initialization function of the Report object, but for now,
    they are accessed by attribute only.

    ``rpt.topmargin = 36`` defines the top margin of the report.

    ``rpt.bottommargin = 36`` defines the bottom margin of the report.

    ``rpt.detailband = None`` should be initialized to a Band object (see below)
    which will be generated once per row in the data source.

    ``rpt.pageheader = None`` is a Band object which is printed at the top
    of each page. When the pageheader Band is generated, it receives the
    row of data that will appear as the first on the page.

    ``rpt.pagefooter = None`` 
    is a Band object which is printed at the bottom
    of each page. When the pagefooter Band is generated, it receives the
    row of data that will appear as the first on the page.

    ``rpt.reportfooter = None``
    is a Band object which is printed at the very end of the report.
    When the reportfooter Band is generated, it receives the
    row of data that was last processed.

    ``rpt.groupheaders = []``
    is a list of Band objects which are printed at the beginning of a new
    group of records, as defined by the 'value' of the Band (see below for
    more details).  Whenever the value changes, that header, and all higher-level
    (i.e. earlier in the list) headers automatically print.
    When a groupheader Band is generated, it receives the
    row of data that will be the first in the new group.

    ``rpt.groupfooters = []``
    is a list of Band objects which are printed at the end of a new
    group of records, as defined by the 'value' of the Band (see below for
    more details).  Whenever the value changes, that footer, and all lower-level
    (i.e. later in the list) footers automatically print.
    When a groupfooter Band is generated, it receives the
    row of data that was last in the group.

    ``rpt.pagenumber = 0`` is not generally changed by the caller; however,
    as a Report attribute, it is accessible to an Element using the ``sysvar``
    option, so it is documented here.  While Report.generate is running,
    the pagenumber attribute contains the current page number.

class Band
----------

    ``band = Band(elements, childbands, key, getvalue, newpagebefore = 0, newpageafter = 0)``

    *elements* is a list of Element (or Element-like) objects which define what data from 
    the row to print, and how to print it.  See Element, below, for details.

    *childbands* is a list of Band objects which will be appended below this Band when
    it is generated.  Child bands float below their parent, so if the parent has an
    Element which renders at different heights, the Elements in the child band(s) will 
    not overwrite it.
    
    *getvalue* is a function which accepts one parameter, the row, and returns an
    item of data.  This permits calculations or modifications of the data before use.
    If getvalue is not provided, key is used.
    If neither key nor getvalue are provided, the value of the Band is None.

    *key* is the key used to access data within the row, i.e., the row will be
    accessed as ``row[key]``.  key is only used if getvalue is not provided.

    *Note: Band values are used only in group headers and group footers, to determine
    if the value has changed.*

    *newpagebefore* and *newpageafter*, if true, indicate that a new page must
    be started at the indicated time.
    Neither apply to detail bands, page headers, or page footers, and newpageafter 
    also does not apply to the report footer.

    **Methods** and **Attributes**

    Bands have no public methods or attributes.

class Element
-------------

    ``element = Element(pos, font, text = None, key = None, getvalue = None, 
    sysvar = None, right = 0, format = str, leading = None, onrender = None)``

    *Note: An important feature of an Element is its value.  In general, the value
    of an Element is relative to the current row, though this is not always so.
    There are four methods an Element may employ to acquire a value, and they
    are always applied in this order: getvalue, key, text, sysvar.  If more than
    one of these methods is defined, the first in order is the only one which will
    be applied.*

    *pos* is a tuple of (x, y) defining the location relative to the top left
    corner of the band where the Element will be rendered.

    *fonts* is a tuple of (fontname, fontsize) defining the font to be used
    when rendering the Element.

    *getvalue* is a function which accepts one parameter, the row, and returns an
    item of data.  This permits calculations or modifications of the data before use.
    If getvalue is provided (and key is omitted, of course), it will be used; if it is
    None, one of the lower-level access methods will be applied.

    *key* is the key used to access data within the row, i.e., the row will be
    accessed as ``row[key]``.  If the key is provided, it will be used; if it is None,
    one of the other access methods will be applied.

    *text* is a value to be used directly as the value of this Element, regardless
    of the current row's content.

    *sysvar* is used to acquire a value from an attribute of the top-level Report
    object.  It is usually used to access the current page number, i.e. ``sysvar = "pagenumber"``.

    *right*, if true, indicates that the Element should be rendered aligned to the right
    rather than to the left.  The pos value will then indicate the upper-right corner
    of the Element.

    *format* is a reference to a function or other callable (str by default) which
    is applied to the Element's value before rendering.

    *leading* is the number of points to add to the "official" height of the Element
    to accomodate line and Band spacing.  If not given, an internal calculation will be applied.

    *onrender* is a reference to a function that is called when the Element is
    rendered.  It is actually passed to the Renderer (see below).  onrender is
    called with a single parameter, a reference to the Renderer.  Assuming you
    called that parameter “obj”, the Element which spawned the Renderer is
    accessible as obj.parent, and the Report as obj.parent.report.

    **Methods**

    Elements have no public methods.

    **Attributes**

    ``element.report`` contains a reference to the top-level Report object.
    This is initialized at the beginning of Report.generate().

class SumElement
----------------

    ``sumelement = SumElement(pos, font, text = None, key = None, getvalue = None, 
    sysvar = None, right = 0, format = str, leading = None, onrender = None)``

    SumElement is a subclass of Element which is used to calculate a sum (total)
    of the value of the SumElement over a group of records.  SumElements are only
    effective when included within group footers or the report footer.  In general,
    a SumElement sums up its values continuously until the value is retrieved,
    i.e. until the SumElement is rendered, at which point the running total is
    reset to zero.

    SumElements have the same parameters, methods, and attributes as regular
    Elements; see above for details of these features.

class Renderer
--------------

    Renderers are internal objects used by PollyReports to print out the values
    of Elements.  As they are entirely internal, they will not be described in
    any particular detail here; if you need to understand more fully how they
    work, please consult the source code.

class Rule
----------

    ``rule = Rule(pos, width, thickness = 1)``

    The Rule class is used to print out horizontal lines, such as separators.

    *pos* is a tuple defining the starting position of the Rule when rendered.  

    *width* is the width (extending right from the position indicated by *pos*)
    to which the Rule will extend.

    *thickness* defines the thickness of the Rule when rendered.

    **Methods** and **Attributes**

    Rules have no public methods or attributes.

