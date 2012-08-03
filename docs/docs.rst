===========================================
PollyReports -- A Database Report Generator
===========================================

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
PDF generation in general), not merely a feature of PollyReports.  When
vertical coordinates are used, they increase going down (y) the page; this is
different than the normal usage when printing with Reportlab, where y
coordinates increase from bottom to top of the page.

Attributes are shown with their default values, if any.  Empty lists shown are
intelligently assigned (I know better than to actually include an empty list as
a default parameter value).

class Report
------------

    ``rpt = Report(datasource = None, detailband = None, pageheader = None, pagefooter = None,
    reportfooter = None, groupheaders = [], groupfooters = [])``

    *datasource* must be an iterable object which yields objects that
    can be indexed with [].  A standard database cursor yielding
    lists, tuples, or dicts is the expected case.  When Report.generate()
    is called, this datasource will be consumed one row at a time.

    If the datasource is empty, no output is generated.

    *detailband* should be initialized to a Band object (see below) which will
    be generated once per row in the data source.  It is acceptable for the
    detail band to be None, which means no detail band will be rendered for
    each row (but subtotals, for instance, will still be generated).  This is
    useful when you want a single report to offer both "detail" and "summary"
    views.  However, if your design calls for the detail band to always be
    omitted, you may wish to redesign your database query instead for better
    performance.

    *pageheader* is a Band object which is printed at the top of each page.
    When the pageheader Band is generated, it receives the row of data that
    will appear as the first on the page.

    *pagefooter* is a Band object which is printed at the bottom of each page.
    When the pagefooter Band is generated, it receives the row of data that
    will appear as the first on the page.

    *reportfooter* is a Band object which is printed at the very end of the
    report.  When the reportfooter Band is generated, it receives the row of
    data that was last processed.

    *groupheaders* is a list of Band objects which are printed at the
    beginning of a new group of records, as defined by the 'value' of the Band
    (see below for more details).  Whenever the value changes, that header, and
    all lower-level (i.e. later in the list) headers automatically print.  If
    more than one group header band is defined, be sure to list the most
    important one (the one that changes least often) first.  When a groupheader
    Band is generated, it receives the row of data that will be the first in
    the new group.

    *groupfooters* is a list of Band objects which are printed at the end
    of a new group of records, as defined by the 'value' of the Band (see below
    for more details).  Whenever the value changes, that footer, and all
    earlier (higher in the list) footers automatically print.  If more than one
    group footer band is defined, be sure to list the most important one (the
    one that changes least often) last.  *This behavior is different from the
    group header behavior, and is by design.* When a groupfooter Band is
    generated, it receives the row of data that was last in the group.

    **Methods**

    ``rpt.generate(canvas)``

    The generate method requires a single parameter, which must be a Reportlab
    Canvas object or an object that presents a similar interface.  As it stands
    now, the following canvas methods and attributes are the only ones being
    used by PollyReports::

        canvas.drawAlignedString()
        canvas.drawCentredString()
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

    All of the initialization parameters described above populate like-named
    attributes, which will not be described again.  It is equally acceptable to
    assign them via the attributes after instantiation as by the initialization
    parameters.

    ``rpt.topmargin = 36`` defines the top margin of the report.

    ``rpt.bottommargin = 36`` defines the bottom margin of the report.

    ``rpt.leftmargin = 36`` defines the left margin of the report; all
    Elements are offset this far from the left edge automatically.

    ``rpt.pagenumber = 0`` is not generally changed by the caller; however,
    as a Report attribute, it is accessible to an Element using the ``sysvar``
    option, so it is documented here.  While Report.generate is running,
    the pagenumber attribute contains the current page number.  An **onrender**
    handler (as described under the Element class, below) may be used to access
    this value to operate a progress bar, for instance.

    ``rpt.rownumber = 0`` is similar to row.pagenumber, in that it is 
    intended to be used within an **onrender** handler.  The *rownumber* value is
    one-based, that is, the first row to print is row number 1.

class Band
----------

    ``band = Band(elements, childbands, key, getvalue, newpagebefore = 0, newpageafter = 0)``

    *elements* is a list of Element (or Element-like) objects which define what
    data from the row to print, and how to print it.  See Element, below, for
    details.

    *childbands* is a list of Band objects which will be appended below this
    Band when it is generated.  Child bands float below their parent, so if the
    parent has an Element which renders at different heights, the Elements in
    the child band(s) will not overwrite it.
    
    *getvalue* is a function which accepts one parameter, the row, and returns
    an item of data.  This permits calculations or modifications of the data
    before use.  If getvalue is not provided, key is used.  If neither key nor
    getvalue are provided, the value of the Band is None.

    *key* is the key used to access data within the row, i.e., the row will be
    accessed as ``row[key]``.  key is only used if getvalue is not provided.

    *Note: Band values are used only in group headers and group footers, to
    determine if the value has changed.*

    *newpagebefore* and *newpageafter*, if true, indicate that a new page must
    be started at the indicated time.  Neither apply to detail bands, page
    headers, or page footers, and newpageafter also does not apply to the
    report footer.

    **Methods** and **Attributes**

    Bands have no public methods or attributes.

class Element
-------------

    ``element = Element(pos, font, text = None, key = None, getvalue = None, 
    sysvar = None, align = "left", format = str, leading = None, onrender = None)``

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

    *align* may be set to any of "left", "right", "center" (or "centre"), or "align".
    It indicates where the value should be printed with respect to the x coordinate
    of the Element.  If set to "left" (the default), the text will be aligned on the left,
    and therefore extend to the right from the given x coordinate.  If set to "right",
    it will be aligned to the right (and thus extends to the left of the x coordinate).
    "center" centers the text at the given coordinate, and "align" attempts to line
    up the decimal point at that location.  Please review the Reportlab documentation
    for more details on the "align" value (see the method *drawAlignedString()*).

    *format* is a reference to a function or other callable (str by default) which
    is applied to the Element's value before rendering.

    *leading* is the number of points to add to the "official" height of the Element
    to accomodate line and Band spacing.  If not given, an internal calculation will be applied.

    *onrender* is a reference to a function that is called when the Element is
    rendered.  It is actually passed to the Renderer (see below).  onrender is
    called with a single parameter, a reference to the Renderer.  Assuming you
    called that parameter "obj", the Element which spawned the Renderer is
    accessible as obj.parent, and the Report as obj.parent.report.

    **Methods**

    Elements have no public methods.

    **Attributes**

    ``element.report`` contains a reference to the top-level Report object.
    This is initialized at the beginning of Report.generate().

class SumElement
----------------

    ``sumelement = SumElement(pos, font, text = None, key = None, getvalue = None, 
    sysvar = None, align = "left", format = str, leading = None, onrender = None)``

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

