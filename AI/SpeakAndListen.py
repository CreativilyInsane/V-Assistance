import speech_recognition as sr, threading, AI.Notification
from tkinter import *
from AI.Others import connectionStatus
# from AI.animation import animation
import time, pyttsx3
# from AI.ChatBot import engine
from AI import CsvFiles
#     # CsvFiles.write_file([{"name": "onetimerun", "address": 1}],"./AI/onetimerun")
# engine = engine()
# onetimerun = CsvFiles.read_files("onetimerun", "./AI")
# if int(onetimerun[0]["address"]) == 0:



def ini():
    engine = pyttsx3.init('sapi5')
    return engine

def voi(engine):
    voices = engine.getProperty('voices')
    return voices



def set_engine_prop(engine, voices, rate, gender):
    engine.setProperty('voice', voices[gender].id)
    engine.setProperty('rate', rate)
    return engine

def load_VA_config():
    configs = CsvFiles.read_files("setting", "./AI")
    return float(configs[2]["address"]), int(configs[1]["address"])

def speak(text, gender = None, rate = None):
    engine = ini()
    voices = voi(engine)
    if rate is None and gender is None:
        rate, gender = load_VA_config()
    engine = set_engine_prop(engine,voices, int(rate), int(gender))
    engine.say(text)
    engine.runAndWait()



def get_audio():
    if connectionStatus():
        for i in range(3):
            r = sr.Recognizer()
            AI.Notification.Notification("Listening").start()
            with sr.Microphone() as source:
                r.pause_threshold = 1
                audio = r.listen(source)
            try:
                query = (r.recognize_google(audio, language='en-in')).lower()
                return query
            except Exception as e:
                speak("Say that again")

    cmd = Input("Command")
    return cmd


def Input(LabelName = "Call You"):
    import PySimpleGUI as sg

    # sg.theme('SandyBeach')


    layout = [
        [sg.Text(LabelName, size =(15, 1)), sg.InputText()],
        [sg.Submit()]
    ]

    window = sg.Window('Simple data entry window', layout)
    event, values = window.read()
    window.close()
    return values[0]

