import os
from time import sleep
from AI import CsvFiles
from threading import Thread
from AI.Notification import Notification
import PySimpleGUI as sg


def remove_dup(addresses):
    check = set()
    new_addresses = []
    for address in addresses:
        addr = tuple(address['name'])
        if addr not in check:
            check.add(addr)
            new_addresses.append(address)

    return new_addresses


class AppIndexing(Thread):

    def __init__(self, root):
        Thread.__init__(self)
        self.root_folders = root
        self.ADDRESSES = []

    def run(self):
        for root_folder in self.root_folders:
            self.find_exe_file(root_folder)
        fresh_addresses = remove_dup(self.ADDRESSES)
        CsvFiles.write_file(fresh_addresses)
        self.ADDRESSES.clear()
        self.__del__()

    def find_exe_file(self, root_folder, exten=".exe"):
        root_len = len(root_folder.split("/"))
        for root, dir, files in os.walk(root_folder):
            for file in files:
                if len(os.path.join(root, file).split("\\")) - root_len <= 4:
                    if file.endswith(exten):
                        self.compare_exe(os.path.join(root, file), file.replace(".exe", "").lower())

    def compare_exe(self, address, exefile):
        address = address.replace("\\", "/")
        app_name_list = address.split("/")
        for app_name in app_name_list[2:len(app_name_list) - 1:]:
            if app_name.replace(" ", "").lower() == exefile.lower():
                app_detail = {"name": app_name.lower(), "address": address.lower()}
                if app_detail["name"] and app_detail["address"]:
                    self.ADDRESSES.append(app_detail)

            elif self.singleword_compare(app_name.lower().split(), exefile):
                app_detail = {"name": app_name.lower(), "address": address.lower()}
                if app_detail["name"] and app_detail["address"]:
                    self.ADDRESSES.append(app_detail)

            elif self.random_compare(app_name.split(), exefile):
                app_detail = {"name": app_name.lower(), "address": address.lower()}
                if app_detail["name"] and app_detail["address"]:
                    self.ADDRESSES.append(app_detail)

    def random_compare(self, appname, exefile):
        if appname[0].isupper():
            app = appname[0] + ''.join([w[0] for w in appname[1::] if w])
            if app.lower() == exefile:
                return True
        else:
            app = ''.join([w[0] for w in appname if w])
            if app.lower() == exefile:
                return True
            app = ''.join([w for w in app[1::] if not w.isdigit()])
            if app.lower() == exefile:
                return True
            app = appname[0][0] + ''.join(appname[1::])
            if app.lower() == exefile:
                return True
            return False

    def singleword_compare(self, appname, exefile):
        if exefile in appname:
            return True

    def __del__(self):
        del self


class MediaIndexing(Thread):
    ADDRESSES = []

    def __init__(self, root):
        Thread.__init__(self)
        self.root_folders = root

    def run(self):
        for root in self.root_folders:
            self.Find_Media(root)
        self.__del__()

    def Find_Media(self, root_folder):
        MEDIAEXTEN = ('.mp4', '.mkv', '.flv', '.mp3', '.webm', '.3gp', 'ma4', '.mpg', '.mpeg')
        if len(root_folder) == 1:
            root_folder += ":/"
        for root, dir, file in os.walk(root_folder):
            for mediafile in file:
                if not (mediafile.startswith('$')) and mediafile.lower().endswith(MEDIAEXTEN):
                    path = (os.path.join(root, mediafile)).replace("\\", "/")
                    media_detail = {"name": path.split('/')[-1].lower(), "address": path.lower()}
                    self.ADDRESSES.append(media_detail)
        if len(root_folder) != 3:
            root_folder = get_name(root_folder)
        else:
            root_folder = root_folder.replace(":/", "")
        CsvFiles.write_file(self.ADDRESSES, "./AI/Searching/Media/" + root_folder)
        self.ADDRESSES.clear()

    def __del__(self):
        del self


class FolderIndexing(Thread):
    ADDRESSES = []

    def __init__(self, root_folder, level=3):
        Thread.__init__(self)
        self.root_folders = root_folder
        self.level = level

    def run(self):
        for Drive in self.root_folders:
            FolderIndexing.FindFolder(self, Drive)
        self.__del__()

    def FindFolder(self, root_Drive):
        if len(root_Drive) == 1:
            root_Drive += ":/"
        for root, dirs, files in os.walk(root_Drive):
            for dir in dirs:
                if (len(os.path.join(root, dir).split("\\")) - 1 <= self.level) and not (
                        '$' in os.path.join(root, dir)):
                    path = (os.path.join(root, dir)).replace("\\", "/")
                    folder_detail = {"name": path.split('/')[-1].lower(), "address": path.lower()}
                    self.ADDRESSES.append(folder_detail)
        if len(root_Drive) != 3:
            root_Drive = get_name(root_Drive)
        else:
            root_Drive = root_Drive.replace(":/", "")
        CsvFiles.write_file(self.ADDRESSES, './AI/Searching/Folder/' + root_Drive)
        self.ADDRESSES.clear()

    def __del__(self):
        del self


class Indexing(Thread):

    def __init__(self, root, level=5):
        Thread.__init__(self)
        self.root = root
        self.level = level
        self.name = "Indexing"
        # layout = [[sg.Text('Indexing')],
        #       [sg.ProgressBar(1, orientation='h', size=(70, 15), key='progress')]]
        # self.window = sg.Window('Indexing', layout, disable_close=True, keep_on_top=True, location=(300, 100) ,disable_minimize=True).Finalize()
        # self.progress_bar = self.window.FindElement('progress')

    def run(self):
        Notification("Start Indexing").run()
        # self.progress_bar.UpdateBar(0, 100)
        thread1 = AppIndexing(self.root["AppIndexing"])
        thread1.start()
        thread1.join()
        # self.progress_bar.UpdateBar(34, 100)
        thread2 = MediaIndexing(self.root["MediaIndexing"])
        thread2.start()
        thread2.join()
        # self.progress_bar.UpdateBar(67, 100)
        thread3 = FolderIndexing(self.root["FolderIndexing"])
        thread3.start()
        thread3.join()
        # self.progress_bar.UpdateBar(100, 100)
        sleep(1)
        Notification("Complete Indexing").run()
        # self.window.close()


def get_name(root):
    try:
        name = root.split("/")
        name = name[len(name) - 1]
        return name
    except:
        return name

# Indexing(root).run()
# obj = Indexing(root, 3)
# thread = ThreadManagement.Timer(interval=4, function= obj.run)
# # threading.Timer()
# thread.start()
# import time
# for i in range(10):
#     print(i)
#     if i==2:
#         thread.stop()
#     time.sleep(1)
# os.startfile("mytube.exe")
# T
# heard = AppIndexing(root["AppIndexing"])
# # Theard.setDaemon(True)
# Theard.start()
# thread = AppIndexing(["g:\\microsoft sql server management studio 18\\common7\\ide"])
# thread.start()
