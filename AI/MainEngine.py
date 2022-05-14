import os, threading
import win32com.client
import win32api
import ctypes
from AI import CsvFiles, webrowser
from AI.Config import config
from AI.Response import positive_response as pr, errorresponse as er
from AI.GmailCalender import get_date, get_audio, CALANDER_STRS, get_events
from AI.Private_Mode.PrivateMode import PrivateMode
from AI.Private_Mode import FaceDatasetCreate
from AI.FileAndFolder import *
from AI.Private_Mode import Capturepic
from AI.mailandmsg import sending
import AI.Others
from AI.PatternUnderstanding import PatternUnderstanding
from ThreadManagement import  Timer, check_thread, threadappend, remove_dead_thread
from AI.GUI import speak, get_audio, get

def Main_Engine(TEXT):
    ans = PatternUnderstanding(TEXT)
    if ans:
        speak(ans)
        return True

    for phasre in CALANDER_STRS:
        if phasre in TEXT.lower():
            date = get_date(TEXT)
            if date:
                get_events(date)
                return True
            else:
                speak("please try again")
                return False
    if "lock" in TEXT:
        speak("See you again soon")
        ctypes.windll.user32.LockWorkStation()
        return True

    elif "search" in TEXT:
        webrowser.searchinurl(TEXT)
        return True

    elif "open " in TEXT or "play" in TEXT:
        thread = check_thread("Indexing")
        if thread and thread.is_alive():
            speak("Indexing file wait until you got notification")
            return
        if "play" in TEXT and ("on yt" in TEXT or "on youtube" in TEXT):
            from AI.webrowser import playonyt
            searched = get_search_word(TEXT)
            AI.webrowser.playonyt(searched)
        elif TEXT.split()[0] in ["movie", "song", "media", "play"]:
            file_finder(TEXT, "media")
        elif "folder" in TEXT:
            file_finder(TEXT, "folder")
        else:
            file_finder(TEXT, "app")
    elif "shutdown" in TEXT:
        speak("Do you really want to shoutdown your machine?")

        ch = get_audio()
        if ch in pr:
            AI.Others.shutdown()
        else:
            speak("Ok!")

    elif "email to" in TEXT or "mail to" in TEXT:
        sending(TEXT, "email")

    elif "message to" in TEXT:
        sending(TEXT, "phone")


    elif "take pic" in TEXT:
        Cam_Detail = Capturepic.list_ports()
        if Cam_Detail:
            if len(Cam_Detail) == 1:
                Capturepic.takepic(0)
            else:
                Capturepic.takepic(Cam_Detail["Camera_Id"])
        else:
            speak("Camera didn't detected")

    elif "connect to" in TEXT:
        name = get_search_word(TEXT)
        if not name:
            name = ""
        from AI.WiFiConnection import main
        main(name)

    elif "disable wi-fi" in TEXT:
        AI.Others.disable()
        speak("wi-fi disabled")

    elif "enable wi-fi" in TEXT:
        AI.Others.enable()
        speak("wi-fi enabled")

    elif "weather in" in TEXT:
        from AI import weather
        city = TEXT.replace("weather in", "")
        result = weather.weather_app(city)
        speak(result)

    elif "roll a dice" in TEXT:
        speak(AI.Others.dice())

    elif "news" in TEXT or "update me" in TEXT:
        speak(AI.Others.news())

    elif "close" in TEXT:
        AI.Others.terminate()

    elif "setting" in TEXT and ("update" in TEXT or "go to" in TEXT) and ("v" in TEXT or "your" in TEXT):
        update = config()
        update.Update()
        update.get_VA_prop()
        update.save_config()

    elif "update" in TEXT and "gmail" in TEXT:
        update = config()
        name = update.Update()
        cre = get(name=name)
        if cre:
            update.save_user_info()
        update.save_config()

    elif "update" in TEXT and "my" in TEXT and "face" in TEXT:
        speak(er['ncre'])
        cre = stop.load_gmail_crediential()
        temp = get(get=False)
        if cre["email"] == temp["email"] and temp["password"] == cre["password"]:
            FaceDatasetCreate.learning_face()




    elif "start private mode" in TEXT:
        P_M = PrivateMode()
        if check_thread(P_M.name):
            speak("Module is already Working")
        else:
            P_M = PrivateMode()
            threadappend(P_M)
            P_M.start()
            speak("Private Mode started")

    elif "stop private mode" in TEXT:
        thread = check_thread("Private_Mode")
        if thread:
            stop = config()
            speak(er['ncre'])
            cre = stop.load_gmail_crediential()
            temp = get(get=False)
            if cre["email"] == temp["email"] and temp["password"] == cre["password"]:
                thread.Stop()
                remove_dead_thread(thread)
                speak("Private Mode is stopped")
        else:
            speak("Its not running")

    elif "remindme " in TEXT or "remind me " in TEXT:

        if check_thread("Reminder"):
            speak("reminder is already running")
            return
        else:
            timer = AI.Others.getint(TEXT) * 60
            msg = AI.Others.get_msg(TEXT)
            reminder = Timer(interval=timer,function= lambda: AI.Others.reminder(msg))
            reminder.setName("Reminder")
            reminder.start()
            threadappend(reminder)
            speak("reminder is set")
    elif ("remove" in TEXT or "cancel" in TEXT) and "reminder" in TEXT:
        thread = check_thread("Reminder")
        if thread:
            thread.cancel()
            speak("reminder is cancel")
        else:
            speak("not reminder is set")
    elif TEXT:
        speak("i think it is not in my domain")










