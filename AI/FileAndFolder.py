import os
import win32com.client
import win32api
import sys
import itertools
from AI import CsvFiles, GUI
from AI.Indexing import Indexing
from AI.SpeakAndListen import speak, get_audio
# from AI.Config import *
from AI.Response import positive_response, microsoft_softwares


def get_search_word(TEXT):
    queries = ['open', 'play','movie', 'song', 'mail', 'folder', 'email', 'media','on','yt', 'youtube', "connect","to", "my","wifi"]
    try:
        searching_word = TEXT[:TEXT.index("from"):]
    except ValueError:
        searching_word = TEXT
    finally:

        for query in queries:
            if query in searching_word.split():
                searching_word = searching_word.replace(query, "")
        return searching_word.strip()


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

def get_result(filetype, FileName, Drives = ['Index']):
    path = "./AI/Searching/"+filetype.capitalize()
    results = []
    files = os.listdir(path)
    for file in files:
        for Drive in Drives:
            if Drive+".csv" == file:
                result = CsvFiles.read_files(Drive, path)
                if result:
                    results.append(result)
    return final_results(results, FileName)

def final_results(addresses, filename):
    final_result = []
    for address in addresses:
        for addrss in address:

            if single_compare(filename.split(),addrss["name"]):
                final_result.append(addrss)

    return final_result


def single_compare(filename_list, actualname):
    for filename in filename_list:
        for appname in actualname.split():
            if filename in appname.lower():
                return True


def file_finder(TEXT, file_type = "app"):
    final_result = []
    search_word = get_search_word(TEXT)
    if file_type == 'app':
        for key in microsoft_softwares.keys():
            if search_word.replace(" ", "") in key.replace(" ",""):
                final_result.append(key)

            elif single_compare(search_word.split(), key):
                final_result.append(key)
        if final_result:
            if len(final_result) > 1:
                speak("which one")
                key = GUI.multiplechoice(final_result)
                os.startfile(microsoft_softwares[key])
                return
            else:
                os.startfile(microsoft_softwares[final_result[0]])
                return
        else:
            final_result = get_result(file_type,search_word)
    else:
        Drives = get_drive(TEXT)
        if Drives:
            final_result = get_result(file_type,search_word, Drives)

    if final_result:
        if len(final_result) != 1:
            names = get_names(final_result)
            ind = GUI.multiplechoice(names)
            result = next((index for (index, d) in enumerate(final_result) if d["name"] == ind), None)
            os.startfile(final_result[result]["address"])
        elif len(final_result) == 1:
            os.startfile(final_result[0]["address"])
            speak(f"This {file_type} is most related")

    else:
        speak("cannot find your need")


def get_names(r):
    names = []
    for name in r:
        names.append(name['name'])
    return names

