
import tkinter
#Tk(screenName= Acknowledge, baseName= None,className=classname,useTk=1)
r = tkinter.Tk(screenName= None, baseName= None,className="acknowledge",useTk=1)
r.title('acknowledge')
button = tkinter.Button(r, text='Stop', width=25, command=r.destroy)
button.pack()
r.mainloop()
