from reportlab.pdfgen.canvas import Canvas
from PollyReports import *
from testdata import data

rpt = Report(data)
rpt.detailband = Band([
    Element((36, 0), ("Helvetica", 11), key = "name"),
    Element((400, 0), ("Helvetica", 11), key = "amount", align = "right"),
])

canvas = Canvas("sample02.pdf", (72*11, 72*8.5))
rpt.generate(canvas)
canvas.save()
