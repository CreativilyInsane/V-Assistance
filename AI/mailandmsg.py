import smtplib
import webbrowser
import time
import pyautogui
from AI import CsvFiles, Others
from AI.Config import config
from AI.FileAndFolder import get_search_word, get_names
from AI.GUI import two_input, get, multiplechoice
from AI.SpeakAndListen import speak, get_audio


def contact(filename, name):
    address = []
    if not name:
        speak("name of receiver")
        name = get_audio()
    result = CsvFiles.read_files(filename, "./AI/Data")
    if result:
        for aname in result:
            if name in aname["name"]:
                address.append(aname)
        if address:
            return address
    return two_input(op=filename, name=name)


def sendmail(reciver, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        get_con = config()
        get_con.load_gmail_crediential()
        cre = get_con.load_gmail_crediential()
        if not cre:
            speak("Need to give credential, we won't save your credentials")
            cre = get()
        server.login(cre["email"], cre["password"])
        server.sendmail(cre["email"], reciver, content)
        server.close()
    except:
        speak("Mail can't send, may be there is internet issue")


def sendmsg(reciver, msg):
    webbrowser.open('https://web.whatsapp.com/send?phone=' + reciver + '&text=' + msg)
    time.sleep(2)
    width, height = pyautogui.size()
    pyautogui.click(width / 2, height / 2)
    time.sleep(6)
    pyautogui.press('enter')


def sending(TEXT, op):
    if Others.connectionStatus():
        name = get_search_word(TEXT)
        reciver = ""
        if not name:
            name = ""
        result = contact(op, name)
        if type(result) == list:
            if len(result) == 1:
                reciver = result[0]["address"]
            else:
                reciver = multiplechoice(get_names(result))
        else:
            reciver = result
            if op == "email":
                CsvFiles.append_files(reciver, "./AI/Data/email")
            else:
                CsvFiles.append_files(reciver, "./AI/Data/contact")
        try:
            content = ""
            content = TEXT[TEXT.index(result[0]["name"]) + len(result[0]["name"])::]
            # print(content)
        except ValueError or TypeError:
            content = TEXT[TEXT.index(name) + len(name)::]
        finally:
            if not content:
                speak("what do want to say")
                content = get_audio()
            speak("sending to " + str(name) + " " + content)
            # print(reciver)
            # print(content)
            if op == "email":
                sendmail(reciver, content)
                return speak("mail sended")
            else:
                sendmsg(reciver, contact())
                return speak("trying to send")
    else:
        return speak("you have no internet access")


