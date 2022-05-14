import speech_recognition as sr
from io import BytesIO
import keyboard
import pyaudio
import threading
from AI.Notification import Notification
from AI.SpeakAndListen import speak
from AI.MainEngine import Main_Engine


class PushToTalk:

    def __init__(self):
        self.__recognizer = sr.Recognizer()
        self.__audio = pyaudio.PyAudio()

        self.__microphone = None
        self.set_input_device(self.__audio.get_default_input_device_info()['name'])

        self.__output_index = None
        self.set_output_device(self.__audio.get_default_output_device_info()['name'])

        self.text = ""

    def set_input_device(self, device_name):
        self.__microphone = sr.Microphone(self.__get_device_index(device_name))

    def set_output_device(self, device_name):
        self.__output_index = self.__get_device_index(device_name)

    def list_device_names(self):
        out = list()
        for i in range(0, self.__audio.get_device_count()):
            out.append(self.__audio.get_device_info_by_index(i)['name'])
        return out

    def __get_device_index(self, device_name):
        device_index = None
        for i, name in enumerate(self.list_device_names()):
            if name == device_name[:31]:
                device_index = i
                break
        if device_index is None:
            raise Exception('Device name "{0}" not found'.format(device_name))
        return device_index

    def __modifiers_str(self):
        out = str()
        for key, val in self.__modifiers.items():
            out += '[:{0} {1}]'.format(key, val)
        return out

    def start(self, key, key_quit="snapshot", block=True):
        running = Event()
        lock = Event()

        def stop():
            nonlocal lock, running
            lock.stop()
            running.set()
            if keyboard.key_to_scan_codes(key) != keyboard.key_to_scan_codes(key_quit):
                keyboard.unhook(key_quit)

        def target():
            while not running.is_set():
                lock.clear()
                keyboard.on_press_key(key, lambda e: lock.set())

                lock.wait()
                keyboard.unhook(key)

                lock.clear()
                if running.is_set():
                    break
                keyboard.on_release_key(key, lambda e: lock.set())

                # noti = Notification("Listening...")
                # noti.start()
                frames = BytesIO()
                with self.__microphone as source:
                    while not lock.is_set():
                        if source.stream is None or source.stream.pyaudio_stream.is_stopped(): break
                        buffer = source.stream.read(source.CHUNK)
                        if len(buffer) == 0:
                            break
                        frames.write(buffer)
                    keyboard.unhook(key)

                    frame_data = frames.getvalue()
                    frames.close()
                    audio = sr.AudioData(frame_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                    # noti.join()
                self.__audio_to_tts(audio)

        if key_quit is not None:
            keyboard.on_press_key(key_quit, lambda e: stop())

        thread = threading.Thread(target=target, daemon=True)
        thread.start()

        if block:
            thread.join()

        return stop

    def start_autodetect(self, energy_threshold=None, key_quit='snapshot', block=True):
        blocking = Event()

        if energy_threshold is None:
            with self.__microphone as source:
                self.__recognizer.adjust_for_ambient_noise(source)
        else:
            self.__recognizer.energy_threshold = energy_threshold

        def callback(recognizer, audio):
            self.__audio_to_tts(audio)
            Notification('Listening...').run()

        stop_listener = self.__recognizer.listen_in_background(self.__microphone, callback)

        def stop():
            nonlocal blocking
            stop_listener()
            blocking.set()
            keyboard.unhook(key_quit)

        if key_quit is not None:
            keyboard.on_press_key(key_quit, lambda e: stop())

        if block:
            blocking.wait()

        return stop

    def __audio_to_tts(self, audio):
        try:
            self.text = (self.__recognizer.recognize_google(audio, language="en-in")).lower()
            # speak(self.text)
            print(self.text)
            if self.text == "switch to background listening":
                from pyautogui import press
                press('snapshot')

            from AI.MainEngine import Main_Engine
            Main_Engine(self.text)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            speak("can't connect to google")


class Event(threading.Event):
    def __init__(self):
        self.__stopped = False
        super().__init__()

    def wait(self):
        while True:
            if super().wait(0.5) or self.__stopped:
                break

    def is_set(self):
        if self.__stopped:
            return True
        return super().is_set()

    isSet = is_set

    def stop(self):
        self.__stopped = True
