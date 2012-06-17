
from PollyReports import *
from reportlab.pdfgen.canvas import Canvas

data = [
    ("Hello", "World"),
]

rpt = Report(datasource = data, 
        detailband = Band([
            Element((36, 0),  ("Helvetica", 12), key = 0),
            Element((72, 14), ("Helvetica", 12), key = 1),
        ]))

canvas = Canvas("sample01.pdf")
rpt.generate(canvas)
canvas.save()

