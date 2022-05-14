from datetime import datetime

thread_list = []

remind = ""


def getime():
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    return current_time


def getdate():
    now = datetime.now()
    current_date = now.strftime("%b %d %Y")
    return current_date


dataset = [
    {"hello": "Hi"},
    {"Hi": "hello"},
    {"how are you": "I'm fine and you"},
    {"i'm fine": "what can i do"},
    {"who are you": "I'm your virtual Assistance"},
    {"what is your name": "My name is V"},
    {"who is the best from all of us": "offcourse, you"},
    {"who is smart from all of us": "offcourse, you"},
    {"why are you here": "I'm here to give some help related to your need"},
    {"what is the time": "The current time is " + getime()},
    {"what is the date": "date is " + getdate()},
    {"who made you": "My master made me"},
    {"who is your master": "offcourse, you"},
    {"value of pie": "value of pie is 3.14"},
    {"hey you are duffer": "i think you are"},
    {"no you": "no, its not me"}
]

microsoft_softwares = {"microsoft word": "winword.exe",
                       "microsoft excel": "excel.exe",
                       "microsoft power point": "powerpnt.exe",
                       "microsoft access": "msaccess.exe",
                       "microsoft one note": "onenote.exe",
                       "microsoft publisher": "mspub.exe",
                       "control panel": 'control.exe',
                       "registry editor": "regedit",
                       'command prompt cmd': "cmd.exe",
                       'file explorer': 'explorer',
                       'notepad': 'notepad.exe',
                       'wordpad': 'write.exe'}

errorresponse = {
    "SAError": "Authentication Failed. For using this feature you need to unable less secure app in gmail account setting",
    "EmailNV": "Your Email is not valid",
    "IR": "Please,All information are dead required",
    "or": "Other, you can skip it",
    "AdminError": "Need Administrator Privileges",
    "CNF": "Camera is not available",
    "fr": 'default input mode is push to talk and key is "left control". if you want to change input '
          'method press "print screen" button',
    "ncre": "first confirm credential"
}

positive_response = ["yes", "hmm", "offcouse", "it's better than pervious", "it's on own", "it's on you", "why not", ]
