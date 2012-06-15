# PollyReports
# Copyright &copy; 2012 Chris Gonnerman
# All rights reserved.
#
# Software License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# Neither the name of the author nor the names of any contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
    PollyReports.py

    PollyReports provides a framework for report generation.  

    A Report object has a data source bound to it at instantiation.
    One or more Band objects (at least, a detail Band) must be added
    to it, and then the generate() method will be called to process
    the data source (an iterator that produces objects that can be
    accessed via [] operations, meaning mainly dict, list, and tuple
    types), executing the detail Band once for each row and producing
    a PDF containing the output.

    Band objects contain a list of Elements (generally at least one)
    which define how data from the row should be printed.  An Element
    may print any normal data item or label and may be subclassed
    to handle other things like images.
"""




class Renderer:

    def _adjust_font_height(self, height):
        # we want to allow about 5% leading on fonts,
        # with a minimum of 1 point, rounded to the
        # nearest integer point.
        return height + max(1, int(height * 0.05 + 0.5))

    def __init__(self, pos, font, text, right):
        self.pos = pos
        self.font = font
        self.text = text
        self.right = right
        self.height = self._adjust_font_height(font[1])

    def render(self, offset, canvas):
        canvas.setFont(*self.font)
        if self.right:
            canvas.drawRightString(self.pos[0], (-1) * (self.pos[1]+offset+self.font[1]), self.text)
        else:
            canvas.drawString(self.pos[0], (-1) * (self.pos[1]+offset+self.font[1]), self.text)


class Element:

    # text refers to a label;
    # key is a value used to look up data in the record;
    # getvalue is a function that accepts the row as a parameter
    #   and returns text to print.
    # all three should not be submitted at the same time,
    #   but if they are, getvalue overrides key overrides text.

    def __init__(self, pos, font, text = None, key = None, getvalue = None, right = 0):
        self.text = text
        self.key = key
        self._getvalue = getvalue
        self.pos = pos
        self.font = font
        self._format = str
        self.right = right
        self.summary = 0 # used in SumElement, below

    def gettext(self, row):
        return self._format(self.getvalue(row))

    def getvalue(self, row):
        if self._getvalue:
            return self._getvalue(row)
        if self.key:
            return row[self.key]
        if self.text:
            return self.text
        return "???"

    # generating an element returns a Renderer object
    # which can be used to print the element out.

    def generate(self, row):
        return Renderer(self.pos, self.font, self.gettext(row), self.right)


class SumElement(Element):

    def getvalue(self, row):
        rc = self.summary
        self.summary = 0
        return rc

    def summarize(self, row):
        self.summary += Element.getvalue(self, row)


class Rule:

    def __init__(self, pos, width, thickness = 1):
        self.pos = pos
        self.width = width
        self.height = thickness

    def gettext(self, row):
        return "-"

    def getvalue(self, row):
        return "-"

    def generate(self, row):
        return self

    def render(self, offset, canvas):
        canvas.saveState()
        canvas.setLineWidth(self.height)
        canvas.setStrokeGray(0)
        canvas.line(self.pos[0],            -1 * (self.pos[1]+offset), 
                    self.pos[0]+self.width, -1 * (self.pos[1]+offset))
        canvas.restoreState()


class Band:

    def __init__(self, elements = None):
        self.elements = elements

    # generating a band creates a list of Renderer objects.
    # the first element of the list is a single integer
    # representing the calculated printing height of the 
    # list.

    def generate(self, row):
        elementlist = [ 0 ]
        for element in self.elements:
            el = element.generate(row)
            elementlist[0] = max(elementlist[0], el.height + el.pos[1])
            elementlist.append(el)
        return elementlist

    # summarize() is only used for total bands, i.e. group and
    # report footers.

    def summarize(self, row):
        for element in self.elements:
            if hasattr(element, "summarize"):
                element.summarize(row)


class Report:

    def __init__(self, datasource):
        self.datasource = datasource
        self.pagesize = None
        self.topmargin = 36
        self.bottommargin = 36

        # bands
        self.detailband = None
        self.pageheader = None
        self.pagefooter = None
        self.reportfooter = None

    def newpage(self, canvas, row, pagenumber):
        if pagenumber:
            canvas.showPage()
        self.endofpage = self.pagesize[1] - self.bottommargin
        canvas.translate(0, self.pagesize[1])
        self.current_offset = self.topmargin
        if self.pageheader:
            elementlist = self.pageheader.generate(row)
            for el in elementlist[1:]:
                el.render(self.current_offset, canvas)
            self.current_offset += elementlist[0]
        if self.pagefooter:
            elementlist = self.pagefooter.generate(row)
            self.endofpage = self.pagesize[1] - self.bottommargin - elementlist[0]
            for el in elementlist[1:]:
                el.render(self.endofpage, canvas)
        return pagenumber + 1

    def generate(self, canvas):
        self.pagesize = (int(canvas._pagesize[0]), int(canvas._pagesize[1]))
        self.current_offset = self.pagesize[1]
        pagenumber = 0
        self.endofpage = self.pagesize[1] - self.bottommargin
        for row in self.datasource:
            elementlist = self.detailband.generate(row)
            if (self.current_offset + elementlist[0]) >= self.endofpage:
                pagenumber = self.newpage(canvas, row, pagenumber)
            for el in elementlist[1:]:
                el.render(self.current_offset, canvas)
            self.current_offset += elementlist[0]
            if self.reportfooter:
                self.reportfooter.summarize(row)
        if self.reportfooter:
            elementlist = self.reportfooter.generate(row)
            if (self.current_offset + elementlist[0]) >= self.endofpage:
                pagenumber = self.newpage(canvas, row, pagenumber)
            for el in elementlist[1:]:
                el.render(self.current_offset, canvas)
            self.current_offset += elementlist[0]
        canvas.showPage()


if __name__ == "__main__":

    from reportlab.pdfgen.canvas import Canvas
    from testdata import data

    rpt = Report(data)
    rpt.detailband = Band([
        Element((36, 0), ("Helvetica", 12), key = "name"),
        Element((240, 0), ("Helvetica", 12), key = "phone"),
        Element((400, 0), ("Helvetica", 12), key = "amount", right = 1),
    ])
    rpt.pageheader = Band([
        Element((36, 0), ("Times-Bold", 20), text = "Page Header"),
        Element((36, 24), ("Helvetica", 12), text = "Name"),
        Element((240, 24), ("Helvetica", 12), text = "Phone"),
        Element((400, 24), ("Helvetica", 12), text = "Amount", right = 1),
        Rule((36, 42), 7.5*72),
    ])
    rpt.pagefooter = Band([
        Element((72*8, 0), ("Times-Bold", 20), text = "Page Footer", right = 1),
    ])
    rpt.reportfooter = Band([
        Rule((330, 4), 72),
        Element((240, 4), ("Helvetica-Bold", 12), text = "Total"),
        SumElement((400, 4), ("Helvetica", 12), key = "amount", right = 1),
    ])

    canvas = Canvas("test.pdf", rpt.pagesize)
    rpt.generate(canvas)
    canvas.save()


# end of file.
