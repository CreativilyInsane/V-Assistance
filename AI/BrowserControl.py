from string import *
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from AI.SpeakAndListen import *
from AI.Response import *

import re
import pyautogui
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import StaleElementReferenceException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions





def openbrowser(browser = ""):
    if "edge" in browser:
        # driver = webdriver.Edge('C:\\Users\\kakar\\PycharmProjects\\AI\\venv\\WebDrivers\\MicrosoftWebDriver.exe')
        driver = webdriver.Edge()
    elif "firefox" in browser:
        driver = webdriver.Firefox()
    elif "opera" in browser:
        driver = webdriver.Opera()
    else:
        driver = webdriver.Chrome(r'WebDrivers\chromedriver.exe')
    return driver

def searchengine(driver,searchquery,searchengine="bing"):
    if searchengine == "google":
        driver.get("https://google.com/search?q="+searchquery)
        return
    driver.get("https://" + searchengine + ".com")
    search_bar = driver.find_element_by_name("q")
    search_bar.clear()
    search_bar.send_keys(searchquery)
    search_bar.send_keys(Keys.RETURN)


def openurls(driver, url):
    driver.get("https://www."+url+".com")


def backwards(driver):
    driver.back()

def forward(driver):
    driver.forward()

def refresh(driver):
    driver.refresh()

def quite(driver):
    driver.quit()



def ValidateUrl(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, str(url)):
        return True
    else:
        return False

def fetchlinks(driver, searchengine="bing"):
    for link in driver.find_elements_by_xpath('.//a'):
        VedioExist = False
        if ValidateUrl(link.get_attribute('href')):
            for video in VideoSearchEngine:
                if video in link.get_attribute('href'):
                    VideoLinks.append(link)
                    VedioExist = True
                    break
            if VedioExist:
                continue
            if searchengine in link.get_attribute('href'):
                EngineLinks.append(link)
            else:
                ResultLinks.append(link)

    # print('Engine Links \n')
    # print(EngineLinks)
    # print('\nResults Links \n')
    # print(ResultLinks)

def getint(str):
    try:
        int_str = {"first": 1,"second": 2,"third" : 3,"forth":4,"fifth":5,"sixth":6,"seventh": 7,"eight": 8,"ninth": 9,"tenth":10}
        for digt in str.split():
            if digt in int_str.keys():
                return int_str[digt]
        x = ""
        for s in str:
            if s.isdigit():
                x += s
        x = int(x)
        return x
    except ValueError or TypeError or AttributeError:
        pass


def ClickLink(driver, TEXT):


    for str1 in Engine_STRS:
        if str1 in TEXT:
            for link in EngineLinks:
                if str1 in link.get_attribute('href'):
                    if "new tab" in TEXT:
                        newtab(driver)
                    print(link.get_attribute('href'))
                    driver.get(link.get_attribute('href'))
                    return

    if "all" in TEXT:
        for link in EngineLinks:
            if "new tab" in TEXT:
                newtab(driver)
            driver.get(link.get_attribute('href'))
            return

    linknum = getint(TEXT)

    if "video" in TEXT:
        ExistEngine = False
        for engine in VideoSearchEngine:
            if engine in TEXT and ("v=" in TEXT or "video" in TEXT):
                ExistEngine = True
                break
        i=0
        for link in VideoLinks:
            # linknum -= 1
            if linknum == i:
                if ExistEngine and engine in link.get_attribute('href'):
                    if "new tab" in TEXT:
                        newtab(driver)
                    print(link.get_attribute('href'))
                    driver.get(link.get_attribute('href'))
                    return
                elif not ExistEngine:
                    if "new tab" in TEXT:
                        newtab(driver)
                    print(link.get_attribute('href'))
                    driver.get(link.get_attribute('href'))
                    return
                else:
                    if ExistEngine:
                        print("Can't Find Link according to your need")
                        return
                    else:
                        print("Link Can't Find")
                        return
            i +=1
    else:
        for link in ResultLinks:
            linknum -= 1
            if linknum == 0:
                linkurl = link.get_attribute('href')
                if "new tab" in TEXT:
                    newtab(driver)
                    driver.get(linkurl)
                    switchtabs(driver, TEXT)
                    # switchtabs(driver,TEXT)
                    break
                driver.get(linkurl)
                break

def pervioustabs(driver):
    clearlist()
    currenttab = driver.current_window_handle
    alltabs = driver.window_handles
    tabindex = alltabs.index(currenttab)
    driver.switch_to.window(driver.window_handles[tabindex - 1])
    fetchlinks(driver, driver.current_url())


def forwardtabs(driver):
    clearlist()
    currenttab = driver.current_window_handle
    alltabs = driver.window_handles
    tabindex = alltabs.index(currenttab)
    driver.switch_to.window(driver.window_handles[tabindex + 1])
    clearlist()
    fetchlinks(driver, driver.current_url())

def switchtabs(driver, TEXT):
    if "pervious" in TEXT:
        pervioustabs(driver)
    elif "next" in TEXT:
        forwardtabs(driver)

    # currenttab = driver.current_window_handle
    # alltabs = driver.window_handles
def clearlist():
    EngineLinks.clear()
    ResultLinks.clear()
    VideoLinks.clear()
    



def newtab(driver):
    driver.execute_script("window.open('');")
    currenttab = driver.current_window_handle
    alltabs = driver.window_handles
    tabindex = alltabs.index(currenttab)
    driver.switch_to.window(driver.window_handles[tabindex + 1])

# def browser(driver, TEXT):
def SWS(TEXT):
    word_list = ["open", "search", "go", "to"]
    for word in word_list:
        if word in TEXT.split():
            TEXT = TEXT.replace(word + " ", "")
    return TEXT

# driver = openbrowser()
# while True:
#     print("Listening")
#     TEXT = get_audio()
#     if "search" in TEXT:
#         if "from" in TEXT:
#             searchengine(driver, SWS(TEXT), TEXT.split("from")[-1])
#             fetchlinks(driver, TEXT.split("from")[-1])
#         else:
#             searchengine(driver, SWS(TEXT))
#             fetchlinks(driver)
#     elif "backwards" in TEXT:
#         backwards(driver)
#     elif "forwards" in TEXT:
#         forward(driver)
#     elif "refresh page" in TEXT:
#         refresh(driver)
#     elif "exit browser control" in TEXT:
#         quite(driver)
#     elif "link" in TEXT:
#         ClickLink(driver, TEXT)
#     elif "open " in TEXT or "go to " in TEXT:
#         openurls(driver,SWS(TEXT))
#     elif "open new tab" in TEXT:
#         newtab(driver)
#     else:
#         speak("Didn't UnderStand!" ).run()
