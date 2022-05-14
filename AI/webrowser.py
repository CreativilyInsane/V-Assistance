import webbrowser
# from google
import pyautogui
import time
from AI.SpeakAndListen import speak

searchengines = ["google", "youtube", "bing", "duckduckgo"]


def searchinurl(query, searchengine='google'):
    query = search_word(query)
    try:
        searchengine = query.split("from")[1]
        query = query.split("from")[0]
    except IndexError:
        pass
    finally:
        webbrowser.open("www."+searchengine+".com\?q="+query)
        time.sleep(1)
        pyautogui.press("enter")

def opensearchengine(searchengine="google"):
    webbrowser.open("www."+searchengine+".com")

def playonyt(topic):
    url = 'https://www.youtube.com/results?q=' + topic
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count+=1
        if i == 'WEB_PAGE_TYPE_WATCH':
            break
    if lst[count-5] == "/results":
        speak('No video found')

    webbrowser.open("https://www.youtube.com"+lst[count-5])
    # return "https://www.youtube.com"+lst[count-5]

def search_word(TEXT):
    com = ["search", "open"]
    for c in com:
        if c in TEXT.split():
            TEXT = TEXT.replace(c + " ", "")

    return TEXT
