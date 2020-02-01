import qrcode
from tkinter import *

def code():

    details = ment.get()
    qr = qrcode.make(details)
    x = "qrcode" + ".png"
    qr.save(x)
    return


window1 = Tk()
window1.configure(background = 'white')

ment = StringVar()
window1.title('qrcode generator')
window1.geometry('500x200')
wlabel = Label(window1,text = "Enter details").pack()
#wlabel = Label(window1,text = "           mid:    ").grid(row=4,column=6,sticky = W)
tInput = Entry(window1,textvariable = ment).pack()
#tInput = Entry(window1,textvariable = ment).grid(row=4,column=8,sticky = E)

qrcode1 = Button(window1, text = 'Generate',command = code).pack()
#qrcode1 = Button(window1, text = 'Generate',command = code).grid(row=5,column=8,sticky=E)
window1.mainloop()
