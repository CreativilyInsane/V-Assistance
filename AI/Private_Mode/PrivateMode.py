from AI.Private_Mode.FaceRecognition import FaceID
from ThreadManagement import threadappend, remove_dead_thread
import time
from pynput import keyboard, mouse
import threading
import datetime
import win32api
import win32con
import pyWinhook, pythoncom
from AI.Notification import Notification


def mouselistener():
    with mouse.Events() as events:
        event = events.get(20)
        if event is None:
            return False
        else:
            return True


def keyboardlistener():
    with keyboard.Events() as events:
        event = events.get(20)
        if event is None:
            return False
        else:
            return True


class PrivateMode(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(False)
        self.running = True
        self.name = "Private_Mode"

    def keyboardlistener(self):
        with keyboard.Events() as events:
            event = events.get(20)
            if event is None:
                return False
            else:
                return True

    def mouselistener(self):
        with mouse.Events() as events:
            event = events.get(20)
            if event is None:
                return False
            else:
                return True

    def run(self):
        block = InputBlocker()
        while True:
            mouse_listen = self.mouselistener()
            key_listen = self.keyboardlistener()
            if self.running:
                if key_listen or mouse_listen:
                    pass
                else:
                    result = FaceID().run()
                    if result:
                        pass
                    else:
                        Notification("Blocking Mouse and Keyboard").start()
                        block.block()
                        # break
    def Stop(self):
        self.running = False


class InputBlocker:

    def __init__(self):
        self.hm = pyWinhook.HookManager()


    main_thread_id = win32api.GetCurrentThreadId()

    def OnKeyboardEvent(self, event):
        if event.Ascii == 96:
            result = FaceID().run()
            if result:
                self.unblock()
                self.stopblock()
                Notification("unblocking Mouse and Keyboard").run()
                # pm = PrivateMode()
                # pm.Stop()
                # remove_dead_thread(pm)
                # pm.start()
            return True
        return False

    def stopblock(self):
        win32api.PostThreadMessage(self.main_thread_id, win32con.WM_QUIT, 0, 0);

    def OnMouseEvent(self, event):
        return False

    def unblock(self):

        try:
            self.hm.UnhookKeyboard()
        except:
            pass
        try:
            self.hm.UnhookMouse()
        except:
            pass

    def block(self):
        try:
            self.hm.KeyAll = self.OnKeyboardEvent
            self.hm.HookKeyboard()
        except SystemError:
            pass
        try:
            self.hm.MouseAll = self.OnMouseEvent
            self.hm.HookMouse()
        except SystemError:
            pass
        pythoncom.PumpMessages()

        # print("here")
