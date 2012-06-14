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

    def __init__(self, pos, font, text):
        self.pos = pos
        self.font = font
        self.text = text
        self.height = self._adjust_font_height(font[1])

    def render(self, offset, canvas):
        canvas.setFont(*self.font)
        canvas.drawString(self.pos[0], (-1) * (self.pos[1]+offset), self.text)


class Element:

    # text refers to a label;
    # key is a value used to look up data in the record;
    # getvalue is a function that accepts the row as a parameter
    #   and returns text to print.
    # all three should not be submitted at the same time,
    #   but if they are, getvalue overrides key overrides text.

    def __init__(self, pos, font, text = None, key = None, getvalue = None):
        self.text = text
        self.key = key
        self.getvalue = getvalue
        self.pos = pos
        self.font = font

    def gettext(self, row):
        if self.getvalue:
            return str(self.getvalue(row))
        if self.key:
            return str(row[self.key])
        if self.text:
            return str(self.text)
        return "???"

    # generating an element returns a Renderer object
    # which can be used to print the element out.

    def generate(self, row):
        return Renderer(self.pos, self.font, self.gettext(row))


class Band:

    def __init__(self):
        self.elements = []

    # generating a band creates a list of Renderer objects.
    # the first element of the list is a single integer
    # representing the calculated printing height of the 
    # list.

    def generate(self, row):
        elementlist = [ 0 ]
        for element in self.elements:
            el = element.generate(row)
            elementlist[0] = max(elementlist[0], el.height)
            elementlist.append(el)
        return elementlist


class Report:

    def __init__(self, datasource):
        self.datasource = datasource
        self.detailband = None
        self.pagesize = None
        self.topmargin = 36
        self.bottommargin = 36

    def _newpage(self, canvas):
        canvas.showPage()
        canvas.translate(0, self.pagesize[1])

    def generate(self, canvas):
        self.pagesize = (int(canvas._pagesize[0]), int(canvas._pagesize[1]))
        canvas.translate(0, self.pagesize[1])
        pagenumber = 1
        current_offset = self.topmargin
        for row in self.datasource:
            elementlist = self.detailband.generate(row)
            if elementlist[0] >= (self.pagesize[1] - current_offset - self.bottommargin):
                self._newpage(canvas)
                current_offset = self.topmargin
            for el in elementlist[1:]:
                el.render(current_offset, canvas)
            current_offset += elementlist[0]
        canvas.showPage()


if __name__ == "__main__":

    from reportlab.pdfgen.canvas import Canvas

    data = [
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Joe Blow", "phone": "555-1212", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
        { "name": "Jane Doe", "phone": "555-2121", },
    ]

    rpt = Report(data)
    rpt.detailband = Band()
    rpt.detailband.elements = [
        Element((36, 0), ("Helvetica", 20), key = "name"),
        Element((360, 0), ("Helvetica", 20), key = "phone"),
    ]

    canvas = Canvas("test.pdf", rpt.pagesize)
    rpt.generate(canvas)
    canvas.save()


# end of file.
