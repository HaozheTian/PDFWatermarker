from tkinter import *
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import os
import fitz

def toUnEditable(page):
    width, length = page.mediabox[2], page.mediabox[3]

    pdf_TEMP = PdfWriter()
    pdf_TEMP.add_page(page)
    pdf_TEMP.write(open("temp.pdf",'wb'))
    
    doc = fitz.open("temp.pdf")

    page = doc.load_page(0)
    pix = page.get_pixmap(matrix = fitz.Matrix(4, 4))
    pix.save("temp.png")
    doc.close()
    os.remove("temp.pdf")

    c = canvas.Canvas("temp.pdf", pagesize = (width, length))
    c.drawImage("temp.png", 0 , 0, *(int(width), int(length)))
    c.save()
    os.remove("temp.png")

    pdf_colated = PdfReader('temp.pdf', strict=False)
    os.remove("temp.pdf")
    return pdf_colated.pages[0]

def browseFiles():
    global filename_target
    filename_target = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Portable Document Format File",
                                                        "*.pdf*"),
                                                       ("all files",
                                                        "*.*")))
    if filename_target[-4:] != ".pdf":
        label_file_explorer.configure(text = "must choose a .pdf file")
    else:
        label_file_explorer.configure(text = filename_target)
    return filename_target

def create_watermark(text, pagesize):
    global filename_watermark
    filename_watermark = "watermark.pdf"

    c = canvas.Canvas(filename_watermark, pagesize) # AUTOGET PAGE SIZE LATER
    c.translate(int(pagesize[0]/2), int(pagesize[1]/2))

    c.setFont("Helvetica", int(pagesize[0]/20))
    c.setStrokeColorRGB(0, 0, 0)
    c.setStrokeColorRGB(0, 0, 0)
    c.rotate(45)
    c.setFillAlpha(0.1)

    unit_x, unit_y = int(pagesize[0]/2), int(pagesize[1]/5)
    for i in range(-2, 3):
        for j in range(-2, 3):
            c.drawString(i * unit_x, j * unit_y, text)
    
    c.save()
    return filename_watermark
    
def addWatermark():
    # read in target pdf
    pdf_target = PdfReader(filename_target, strict=False)
    width, length = pdf_target.pages[0].mediabox[2], pdf_target.pages[0].mediabox[3]

    # create watermark pdf
    text = entry_watermark.get()
    filename_watermark = create_watermark(text, (width, length))

    # read in target pdf
    pdf_watermark = PdfReader(filename_watermark, strict=False)

    # add to each page
    pdf_output = PdfWriter()
    for page in pdf_target.pages:
        page.merge_page(pdf_watermark.pages[0])
        if var_colate.get() == 1:
            page = toUnEditable(page)
        page.compress_content_streams()
        pdf_output.add_page(page)

    # save pdf
    pdf_output.write(open(filename_target[:-4] + '_watermarked' + '.pdf','wb'))

    os.remove(filename_watermark)

    
    return


                                                                                                  
# Create the root window
window = Tk()

var_colate = IntVar()
  
# Set window title
window.title('File Explorer')
  
# Set window size
window.geometry("700x200")
  
# Create a File Explorer label
label_watermark = Label(window,
                        text = "enter watermark (only support English)",
                        width = 40, height = 2)
entry_watermark = Entry(window,
                        width = 40)
label_file_explorer = Label(window,
                            text = "File Explorer using Tkinter",
                            width = 40, height = 2)
button_explore = Button(window,
                        text = "Choose File",
                        command = browseFiles,
                        width = 40, height = 2)
button_add_watermark = Button(window,
                     text = "Add Watermark",
                     command = addWatermark,
                     width=60)
check_colate = Checkbutton(window,
                           text = "colate",
                           width=10,
                           variable=var_colate)
button_exit = Button(window,
                     text = "Exit",
                     command = window.destroy,
                     width=60)
  
# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_watermark.place(relx=.5, rely=.1,anchor= CENTER)
entry_watermark.place(relx=.5, rely=.2,anchor= CENTER)
label_file_explorer.place(relx=.5, rely=.4,anchor = W)
button_explore.place(relx=.05, rely=.4,anchor= W)
button_add_watermark.place(relx=.05, rely=.65,anchor= W)
check_colate.place(relx=.7, rely=.65,anchor= W)
button_exit.place(relx=.05, rely=.85,anchor= W)
  
# Let the window wait for any events
window.mainloop()