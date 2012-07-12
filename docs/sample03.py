from reportlab.pdfgen.canvas import Canvas
from PollyReports import *
from testdata import data

rpt = Report(data)
rpt.detailband = Band([
    Element((36, 0), ("Helvetica", 11), key = "name"),
    Element((400, 0), ("Helvetica", 11), key = "amount", align = "right"),
])
rpt.pageheader = Band([
    Element((36, 0), ("Times-Bold", 20), text = "Page Header"),
    Element((36, 24), ("Helvetica", 12), text = "Name"),
    Element((400, 24), ("Helvetica", 12), text = "Amount", align = "right"),
    Rule((36, 42), 7.5*72, thickness = 2),
])
rpt.pagefooter = Band([
    Element((72*8, 0), ("Times-Bold", 20), text = "Page Footer", align = "right"),
    Element((36, 16), ("Helvetica-Bold", 12), sysvar = "pagenumber", format = lambda x: "Page %d" % x),
])

canvas = Canvas("sample03.pdf", (72*11, 72*8.5))
rpt.generate(canvas)
canvas.save()
