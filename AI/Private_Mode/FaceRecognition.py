import cv2
import sys
import numpy as np
import ctypes
from AI.Private_Mode import Capturepic
import os
from datetime import datetime
import threading
import time
import pyWinhook


class FaceID():
    def __init__(self, id=0):
        self.id = id
        path = "trainer"
        self.intercepter = "./AI/Private_Mode/Intercepter"
        cascadePath = "./AI/Private_Mode/haarcascade/haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(cascadePath);
        path = "trainer"
        try:
            self.cam = cv2.VideoCapture(self.id, cv2.CAP_DSHOW)
        except:
            pass
        self.assure_path_exists("./AI/Private_Mode/trainer/")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('./AI/Private_Mode/trainer/Users.yml')

    def assure_path_exists(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def run(self, timeout=5):
        # print("Ficail Recognition Start")
        counter_correct = 0
        counter_wrong = 0
        startTime = time.time()

        while True:
            if time.time() - startTime > timeout:
                try:
                    # print("no face found")
                    self.cam.release()
                    Capturepic.takepic(self.id, self.intercepter)
                    ctypes.windll.user32.LockWorkStation()
                    return False
                except:
                    pass
            _, im = self.cam.read()
            try:
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            except cv2.error:
                return True

            faces = self.faceCascade.detectMultiScale(gray, 1.4, 5)

            for (x, y, w, h) in faces:
                Id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])

                if confidence > 80:
                    counter_wrong += 1
                    # print("wrong")
                else:
                    counter_correct += 1
                    # print("correct")

                if counter_wrong == 3:
                    self.cam.release()
                    Capturepic.takepic(self.id, self.intercepter)
                    ctypes.windll.user32.LockWorkStation(0)
                    return False

                if counter_correct == 6:
                    self.cam.release()
                    return True

            # cv2.imshow("Face Detection", im)

# FaceID().run()
