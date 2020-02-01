import qrcode
from tkinter import *


def code2():
    TI = tInput()
    qr = qrcode.make(TI)
    qr.save("image.png")

def tInput():
    TextInput = Entry().pack()

window1 = Tk()
window1.title('qrapp')
window1.geometry('1000x1000')
qrcode1 = Button(window1, text = 'Generate',command = code2)
qrcode1.pack()

window1.mainloop()
