import speech_recognition as sr
import time
from AI.SpeakAndListen import speak, get_audio
from AI.MainEngine import Main_Engine
from keyboard import wait
import win32api, win32con


class BackGroundListening():
    main_thread_id = win32api.GetCurrentThreadId()

    def __init__(self):
        self.r = sr.Recognizer()
        self.source = sr.Microphone()

    def callback(self, recognizer, audio):

        try:
            speech_as_text = (recognizer.recognize_google(audio, language="en-in")).lower()

            if "v" in speech_as_text or "hey v" in speech_as_text or "hello" in speech_as_text:
                TEXT = get_audio()
                Main_Engine(TEXT)

        except sr.UnknownValueError:
            pass

    def start_recognizer(self):
        stop = self.r.listen_in_background(self.source, self.callback)
        wait("snapshot")
        stop(wait_for_stop=False)
