import pyscreenshot
from win10toast import ToastNotifier
import pyautogui
import os
from datetime import datetime
from threading import Thread
import time
import webbrowser
import subprocess

from win32comext.shell import shell

from AI.Notification import Notification


def cmd(commands):
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c ' + commands)


def screenshot():
    now = datetime.now()
    image = pyscreenshot.grab()
    image.show()
    import getpass
    username = getpass.getuser()
    image.save("C:/Users/" + username + "/Pictures/ScreenShot_" + now.strftime("%b %d %Y %I %M %S") + ".png")


def terminate():
    pyautogui.hotkey("alt", "f4")


def random(end, start=0):
    from random import randint
    num = randint(start, end)
    Notification(msg="Number is " + str(num))
    return "number is " + str(num)


def enable():
    cmd1 = "netsh interface set interface Wi-Fi enabled"
    Thread(target=cmd(cmd1), name="WifiEnable").start()


def disable():
    cmd1 = "netsh interface set interface Wi-Fi disabled"
    Thread(target=cmd(cmd1), name="WifiDisable").start()


import pyperclip


def speakaloud():
    return pyperclip.paste()


def connectionStatus():
    import urllib.request

    try:
        urllib.request.urlopen('http://google.com')
        return True
    except urllib.error.URLError:
        return False


# speakaloud()


from random import randint


def dice():
    return "it's" + str(randint(1, 6))


def coin():
    output = ['heads', 'tails']
    return "It's " + output[randint(0, 1)]


def shutdown(time=4):
    cont = "shutdown -s -t %s" % time
    os.system(cont)


def cancelShutdown():
    cont = "shutdown /a"
    os.system(cont)


def reminder(msg):
    Notification("Reminder", msg).run()





from urllib.request import urlopen
from bs4 import BeautifulSoup as soup


def news():
    if connectionStatus():
        try:
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = soup(xml_page, "xml")
            news_list = soup_page.findAll("item")
            li = []
            for news in news_list[:15]:
                li.append(str(news.title.text.encode('utf-8'))[1:])
            return filter_news(li)
        except Exception as e:
            return "They is some error occur"
    else:
        return "you have no internet access"


import wikipedia
import re


def get_filter(news):
    return re.findall(r"\\\w\w\w", news)


def filter_news(news_list):
    Filter_News = []
    for news in news_list:
        cases = get_filter(news)
        for case in cases:
            news = news.replace(case, " ")
        Filter_News.append(news)
    return Filter_News


def tell_me_about(topic):
    topic = topic_for_wp(topic)
    topic = topic.replace("wikipedia", "")
    results = wikipedia.summary(topic, sentences=2)
    return results


def topic_for_wp(query):
    q_words = ["how", "to", "what", "the", "who", "is"]
    for word in q_words:
        if word in query.split():
            query = query.replace(word + " ", "")
    return query


def getint(str):
    try:
        int_str = {"first": 1, "second": 2, "third": 3, "forth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eight": 8,
                   "ninth": 9, "tenth": 10}
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
        return False


def get_msg(TEXT):
    remove_word = ["remind", "me", "about"]
    for word in remove_word:
        if word in TEXT.split():
            TEXT = TEXT.replace(word + " ", "")
    return TEXT.split("after")[0]


