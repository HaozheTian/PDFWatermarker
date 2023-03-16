from PyPDF2 import PdfReader, PdfWriter
import fitz
import os
from reportlab.pdfgen import canvas

def toUnEditable(page):
    width, length = page.mediabox[2], page.mediabox[3]

    pdf_TEMP = PdfWriter()
    pdf_TEMP.add_page(page)
    pdf_TEMP.write(open("temp.pdf",'wb'))
    
    doc = fitz.open("temp.pdf")

    page = doc.load_page(0)
    pix = page.get_pixmap(matrix = fitz.Matrix(3, 3))
    pix.save("temp.png")
    doc.close()
    os.remove("temp.pdf")

    c = canvas.Canvas("temp.pdf", pagesize = (width, length))
    c.drawImage("temp.png", 0 , 0, *(width, length))
    c.save()
    os.remove("temp.png")

    pdf_colated = PdfReader(open('temp.pdf', 'rb'), strict=False)
    return pdf_colated.pages[0]

    

pdf_target = PdfReader(open('momentus.pdf', 'rb'), strict=False)

for page in pdf_target.pages:
    page = toUnEditable(page)