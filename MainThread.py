from AI import PushToTalk, animation, MainEngine, CsvFiles
from AI.SpeakAndListen import speak, get_audio
from AI.Response import errorresponse as er
from AI.Indexing import Indexing
from AI.Config import config
from AI.Notification import Notification
from ThreadManagement import threadappend, check_thread
from AI.BackgroundListening import BackGroundListening
from AI.Private_Mode.PrivateMode import PrivateMode
from AI.SpeakAndListen import ini
import os, time
import PySimpleGUI as sg
# sg.Print('Capturing Face Data', do_not_reroute_stdout=False, no_button=True, no_titlebar=True)


class AI:
    input_type = True

    def __init__(self):
        self.private_mode = PrivateMode()
        self.push_to_talk_key = 'ctrl'
        self.load_config = config()
        self.indexing = Indexing(self.load_config.root, 5)

    def run(self):
        if not os.path.exists('./AI/setting.csv'):
            animation.run()
            self.load_config.set_config()
            speak(er['fr'])

        # self.indexing.start()
        time.sleep(2.5)
        # threadappend(self.indexing)
        # self.load_config.load_config()
        # self.load_config.load_VA_config()
        # self.indexing.join()
        self.private_mode.start()

        threadappend(self.private_mode)

        # time.sleep(10)
        # MainEngine.Main_Engine("stop private mode")
        # print(check_thread(self.private_mode))
        # time.sleep(100)
        # MainEngine.Main_Engine("what is value of pie")
        # print("hello")
        while True:
            if self.input_type:
                Notification("Push to talk is enable").run()
                vr = PushToTalk.PushToTalk()
                vr.start(self.push_to_talk_key)
                self.input_type = False
            else:
                Notification("Background Listening is enable").run()
                bgl = BackGroundListening()
                bgl.start_recognizer()
                self.input_type = True
        # MainEngine.Main_Engine("open study folder")


if __name__ == '__main__':
    AI = AI()
    AI.run()
    # MainEngine.Main_Engine("open assignment folder")




