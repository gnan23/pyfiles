import pyautogui
import time
import webbrowser
import requests
from tkinter import *


pyautogui.FAILSAFE = False
#from selenium import webdriver
#from selenium.webdriver.common.keys import keys
#import requests
url="https://icm.ad.msft.net/imp/v3/incidents/search/advanced"


def webopenstatus():
    requests.packages.urllib3.disable_warnings()
    try:

        #"https://dev.azure.com/RD/_apis/wit/workitems?ids=15191737&api-version=5.0"           ##"https://icm.ad.msft.net"
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
    boxLocation=pyautogui.locateOnScreen('checkBox2.png',tolerance = 10, confidence = 0.9)
    boxLocation2=pyautogui.Center(boxLocation)
    print(boxLocation2)
    #print(boxLocation2.x)
    pyautogui.click(boxLocation2.x,boxLocation2.y,duration = 1.5 )
    #pyautogui.click(59,282, duration = 1);pyautogui.click(1431,205, duration = 1);pyautogui.click(59,282, duration = 1)
    pyautogui.FAILSAFE = False
    time.sleep(1)

def play():

    pyautogui.click(308,205,duration=1)
    playButton = pyautogui.locateOnScreen('play.png')
    playButton2 = pyautogui.Center(playButton)
    pyautogui.click(playButton2.x,playButton2.y, duration = 2)

def buttonPress():
    try:
        pressLocation=pyautogui.locateOnScreen('button.png')
    except Exception as e:
        webopen()
        checkBox()
        buttonLocation=pyautogui.locateOnScreen('button.png')
    pressLocation2=pyautogui.center(pressLocation)
    print(boxLocation2)
    #print(boxLocation2.x)
    pyautogui.click(pressLocation2.x,pressLocation2.y,duration = 1.5 )


def window():
    webopen()                  #opening weblink

    while True:


        time.sleep(15)
        print(pyautogui.size())
        #pyautogui.click(100, 100)
        time.sleep(10)

        checkBox()           # recognizing id checkbox

        buttonPress()        #recognizing a button
        play()


root = Tk()
root.geometry('500x500')
root.title("AcknowledgeImage")
startButton=Button(root,text="start",width=60,command=window)
startButton.pack()

stopButton = Button(root,text="stop",width=60,command=root.destroy)
stopButton.pack()

root.mainloop()
