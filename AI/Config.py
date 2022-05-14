# import getpass
import win32api
from datetime import datetime
from AI.GUI import get
from AI.Response import errorresponse as er
from AI.SpeakAndListen import speak, voi, ini
from AI.Private_Mode import FaceDatasetCreate, Capturepic
from AI import CsvFiles
from tkinter import *
from tkinter.ttk import Progressbar
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Text
import time









def get_drive(TEXT = ""):
    Drives = []

    try:
        TEXT = TEXT[TEXT.index("from")::]
        if TEXT:
            Drives_Not_Avail = []
            Searching_Word = TEXT.split(" ")
            for word in Searching_Word:
                if len(word) == 1:
                    if word.upper() + ":\\"  in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
                        Drives.append(word.upper())
                    else:
                        Drives_Not_Avail.append(word)
            if Drives_Not_Avail:
                if not Drives:
                    speak.run("All Drives Are not accessable")
                    return False
                else:
                    speak.run("Some of these are not accessable")
    except ValueError:
        Drives = win32api.GetLogicalDriveStrings().split('\000')[:-1:]
        Drives = list(map(lambda x: x.replace(':\\',''),Drives))
    return Drives

import getpass



class config():
    root = {}

    def __init__(self, appindex = []):
        Drives = []
        self.dataset = []
        self.values = []
        self.speed = None
        self.gender = None
        username = getpass.getuser()
        Drives = get_drive()
        Drives.remove("C")
        Drives.append('c:/users/'+username+'/Downloads')
        App = ['c:/program files (x86)', 'c:/program files', 'c:/users/'+username+'/appData/Local/Programs']
        for app in appindex:
            App.append(app)
        self.root["AppIndexing"] = App
        self.root["FolderIndexing"] = self.root["MediaIndexing"] = Drives




    def set_config(self):
        layout = [[sg.Text('Configration')],
              [sg.ProgressBar(1, orientation='h', size=(70, 15), key='progress')]]
        self.window = sg.Window('Configration', layout ,disable_close=TRUE, keep_on_top=True, location=(300, 100) ,disable_minimize=True).Finalize()
        self.progress_bar = self.window.FindElement('progress')

        self.progress_bar.UpdateBar(0, 100)
        self.get_VA_prop()
        self.progress_bar.UpdateBar(20, 100)
        speak("We don't share your gmail crediential, it save on your local machine", self.gender, self.speed)
        gmail = get(self.gender, self.speed)
        if gmail:
            self.save_user_info(gmail)
        self.progress_bar.UpdateBar(50, 100)
        if Capturepic.list_ports():
            speak("Setting up your face, be patient", self.gender, self.speed)
            FaceDatasetCreate.learning_face()
            speak("Your face data has captured", self.gender, self.speed)
        else:
            speak.run(er["CNF"], self.gender, self.speed)
        self.progress_bar.UpdateBar(80, 100)
        time.sleep(2.3)
        self.save_config()
        self.progress_bar.UpdateBar(100, 100)
        time.sleep(1.5)
        self.window.close()

    def save_config(self):
        CsvFiles.write_file(self.dataset, "./AI/setting")

    def save_user_info(self, gmail_config):
        try:
            self.dataset[3]["name"] ="User"
            if gmail_config["name"]: self.dataset[3]["address"] = gmail_config["name"]
            self.dataset[4]["name"] = "Email"
            if gmail_config["email"]: self.dataset[4]["address"] =  gmail_config["email"]
            self.dataset[5]["name"] = "Password"
            if gmail_config["password"]: self.dataset[5]["address"] = gmail_config["password"]
        except IndexError:
            self.dataset.append({"name":"User", "address": gmail_config["name"]})
            self.dataset.append({"name":"Email", "address": gmail_config["email"]})
            self.dataset.append({"name":"Password", "address": gmail_config["password"]})


    def get_VA_prop(self):
        layout = [[sg.Text('Virtual Assistance Setting', size=(30, 1), font=("Helvetica", 25), text_color='white')],
            [sg.Text("My Name is 'V'")],
            [sg.Text('Voice Gender')],
            [sg.Radio('Female', "gender", default=True, key="female"), sg.Radio('Male', "gender", key="male")],
            [sg.Text('Voice Rate')],
            [sg.Slider(range=(1, 100), key="rate",orientation='h', size=(35, 20), default_value=45)],
            [sg.Button(button_text="Test",bind_return_key=True)],
            [sg.Submit(button_color=('white', 'green'))]]

        window = sg.Window('Everything bagel', layout, auto_size_text=True, default_element_size=(40, 1),keep_on_top=True, no_titlebar=True)
        while True:
            event, self.values  = window.Read()

            self.speed = self.values['rate']
            if self.values['male']:
                self.gender = 0
            elif self.values['female']:
                self.gender = 1
            self.speed *= 4
            if event == 'Test':
                self.test()
            elif event in 'Submit':
                self.save_prop()
                break
        window.close()

    def test(self):
        voices = voi(ini())
        speak(f"You Have Selected {(voices[self.gender].name).split('Desktop')[0]} as my voice and my name is V", self.gender, self.speed)

    def save_prop(self):
        try:
            self.dataset[0]["name"] = 'VaName'
            self.dataset[0]["address"] = "V"
            if self.speed:
                self.dataset[1]["name"] = 'gender'
                self.dataset[1]["address"]= self.gender
            if self.gender:
                self.dataset[2]["name"] = 'rate'
                self.dataset[2]["address"] = self.speed
        except:
            self.dataset.append({"name": "VaName", "address": "V"})
            self.dataset.append({"name": "gender", "address": self.gender})
            self.dataset.append({"name": "rate", "address": self.speed})


    def load_gmail_crediential(self):
        config = CsvFiles.read_files("setting", "./AI")
        try:
            return {"email": config[4]['address'], "password": config[5]['address']}
        except Exception as e:
            return False

    def Update(self):
        self.dataset.clear()
        self.dataset = CsvFiles.read_files("setting", "./AI")
        return self.dataset[3]['name']






