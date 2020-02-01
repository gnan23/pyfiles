import pyautogui
import time
import webbrowser
import requests
import asyncio

from tkinter import *

def window():

    webopen()                  #opening weblink

    while True:
        time.sleep(10)
        print(pyautogui.size())
        #pyautogui.click(100, 100)
        time.sleep(10)

        checkBox()           # recognizing id checkbox

        buttonPress()        #recognizing a button

        play()
        #####time.sleep(300)


pyautogui.FAILSAFE = False

url="https://icm.ad.msft.net/imp/v3/incidents/search/advanced"

def webopenstatus():
    requests.packages.urllib3.disable_warnings()
    try:

        tfs=requests.get(url,verify=False)#HTTPBasicAuth('user', 'pass'))

        if tfs.status_code == 200:                                #response 401 is for unauthorized
            print("good connection")
            webbrowser.open(url)#"https://icm.ad.msft.net/imp/v3/incidents/search/advanced")

        else:
            print ("Exception")


    except Exception as a:

        time.sleep(5)
        #webbrowser.open(url)
        print("Exception"+a)
    #(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")

def webopen():
    webbrowser.open(url)

def checkBox():
    print("checking for checkbox")
    time.sleep(10)
    try:
        pyautogui.FAILSAFE = False
        boxLocation=pyautogui.locateOnScreen('checkBox2.png')#tolerance = 10, confidence = 0.9)
        boxLocation2=pyautogui.Center(boxLocation)
        print(boxLocation2)
        pyautogui.click(boxLocation2.x,boxLocation2.y,duration = 1.5 )
        #root.update_idletasks()
    except Exception as e:
        print (e)
    #else:
    #    pyautogui.click(60 ,283 ,duration=2 )
    pyautogui.click(60 ,283 ,duration=2 )
    #root.update_idletasks()


def buttonPress():
    try:
        pressLocation=pyautogui.locateOnScreen('button.png') # , confidence = 0.9)
        pressLocation2=pyautogui.center(pressLocation)
        print(boxLocation2)
        pyautogui.click(pressLocation2.x,pressLocation2.y,duration = 1.5 )
        #root.update_idletasks()
    except Exception as e:
        print (e)
    #else:
    #    pyautogui.click(1412,204,duration = 1)

    pyautogui.click(1412,204,duration = 1)
    #root.update_idletasks()
    #    webopen()
    #    checkBox()
    #    buttonLocation=pyautogui.locateOnScreen('button.png')
    #buttonLocation2=pyautogui.center(buttonLocation)
    #print(boxLocation2)
    #print(boxLocation2.x)


def play():
    try:
        playLocation=pyautogui.locateOnScreen('play.png') # , confidence = 0.9)
        playLocation2=pyautogui.center(playLocation)
        print(boxLocation2)
        pyautogui.click(playLocation2.x,playLocation2.y,duration = 1.5 )
        #root.update_idletasks()
    except Exception as e:
        print (e)
    #else:
    #    pyautogui.click(308,205,duration=1)
    #    root.update_idletasks()

    pyautogui.click(308,205,duration=1)
    #root.update_idletasks()




root = Tk()
root.geometry('1000x1000')
root.title('acknowledge')
startButton = Button(root, text ='Start' , command=window)
startButton.pack()

stopButton = Button(root, text= 'stop' , command = root.destroy)
#s= tkinter.windows()
#button2 = tkinter.Button(r, text='start', width=25, command=window())
#button2.pack()
stopButton.pack()
root.mainloop()
