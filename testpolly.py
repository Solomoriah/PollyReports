# PollyReports
# Copyright 2012 Chris Gonnerman
# All rights reserved.
# 
# BSD 2-Clause License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.  Redistributions in binary
# form must reproduce the above copyright notice, this list of conditions and
# the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
    testpolly.py -- demonstrate PollyReports functionality
"""


from reportlab.pdfgen.canvas import Canvas
from PollyReports import *
from testdata import data
import sys


def pagecount(obj):
    sys.stdout.write("%d " % obj.parent.report.pagenumber)
    sys.stdout.flush()

    
rpt = Report(data)
rpt.detailband = Band([
    Element((36, 0), ("Helvetica", 11), key = "name"),
    Element((400, 0), ("Helvetica", 11), key = "amount", align = "right"),
], childbands = [
    Band([
        Element((72, 0), ("Helvetica", 11), key = "phone"),
    ]),
])
rpt.titleband = Band([
    Element((36, 0), ("Times-Bold", 20), text = "Title Band"),
    Element((36, 22), ("Helvetica", 12), text = "Appears before page header on first page"),
    Image((400, 0), 64, 64, text = "typewriter.png"),
    Rule((36, 66), 7.5*72, thickness = 2),
])
rpt.pageheader = Band([
    Element((36, 0), ("Times-Bold", 20), text = "Page Header", onrender = pagecount),
    Element((36, 24), ("Helvetica", 12), text = "Name"),
    Element((400, 24), ("Helvetica", 12), text = "Amount", align = "right"),
    Rule((36, 42), 7.5*72, thickness = 2),
])
rpt.reportheader = Band([
    Element((36, 0), ("Times-Bold", 20), text = "Report Header"),
    Element((36, 22), ("Helvetica", 12), text = "Appears after page header on first page"),
    Rule((36, 36), 7.5*72, thickness = 2),
])
rpt.pagefooter = Band([
    Element((72*8, 0), ("Times-Bold", 20), text = "Page Footer", align = "right"),
    Element((36, 16), ("Helvetica-Bold", 12), sysvar = "pagenumber", format = lambda x: "Page %d" % x),
])
rpt.reportfooter = Band([
    Rule((330, 4), 72),
    Element((240, 4), ("Helvetica-Bold", 12), text = "Grand Total"),
    SumElement((400, 4), ("Helvetica-Bold", 12), key = "amount", align = "right"),
    Element((36, 16), ("Helvetica-Bold", 12), text = ""),
])
rpt.groupheaders = [
    Band([
        Rule((36, 20), 7.5*72),
        Element((36, 4), ("Helvetica-Bold", 12), key = "year",
            format = lambda x: "Year %d" % x),
    ], key = "year"),
    Band([
        Rule((36, 20), 7.5*72),
        Element((36, 4), ("Helvetica-Bold", 12), getvalue = lambda x: x["name"][0].upper(),
            format = lambda x: "Names beginning with %s" % x),
    ], getvalue = lambda x: x["name"][0].upper()),
]
rpt.groupfooters = [
    Band([
        Rule((330, 4), 72),
        Element((36, 4), ("Helvetica-Bold", 12), getvalue = lambda x: x["name"][0].upper(),
            format = lambda x: "Subtotal for %s" % x),
        SumElement((400, 4), ("Helvetica-Bold", 12), key = "amount", align = "right"),
        Element((36, 16), ("Helvetica-Bold", 12), text = ""),
    ], getvalue = lambda x: x["name"][0].upper()),
    Band([
        Rule((330, 4), 72),
        Element((36, 4), ("Helvetica-Bold", 12), key = "year",
            format = lambda x: "Subtotal for %d" % x),
    ], key = "year", newpageafter = 1),
]

sys.stdout.write("Report Starting...\nPage ")

canvas = Canvas("test.pdf", (72*11, 72*8.5))
rpt.generate(canvas)
canvas.save()

print "\nDone."


# end of file.
