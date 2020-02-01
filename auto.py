import sys
from selenium import webdriver
#from selenium.webdriver.common.keys import keys
import requests
usr = "gnana007"
web = webdriver.Firefox()#(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")

web.get("https://www.facebook.com")
web2 = web.find_element_by_link_text('submit')
web2.click()
