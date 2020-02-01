import pyqrcode
from pyqrcode import *
import qrcode
from tkinter import *
from tkinter import messagebox
windows = Tk()
windows.title("QRcode")


def qr_code() :
    code = "v-gnaret@microsoft"
    qr = pyqrcode.create(code)
    qr = pyqrcode.QRCode(version = 1,box_size=10)
    qr.add_data("v-gnaret@microsoft.com")
    qr.make(fit=True)
    img = qr.make_image(fill_colour = 'black', back_colour = 'white')
    print(img)

btn = Button(windows , text = "qrcode2", command = qr_code)
btn.pack()

image = Image
windows.mainloop()
