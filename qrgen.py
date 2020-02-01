import qrcode
from tkinter import *


def code2():
    TextInput = Entry().pack()

    qr = qrcode.make(TextInput)
    qr.save("image.png")


window1 = Tk()
window1.title('qrapp')
window1.geometry('1000x1000')
qrcode1 = Button(window1, text = 'Generate',command = code2)
qrcode1.pack()

window1.mainloop()
