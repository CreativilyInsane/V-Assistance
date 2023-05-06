import os
import cv2, time
import numpy as np
from AI.SpeakAndListen import speak
import PySimpleGUI as sg
from AI.Private_Mode.Capturepic import list_ports


def check_path(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def learning_face(filename="Users"):
    if not list_ports():
        speak("Camera is not opening")
        return False
    vid_cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    face_cascade = cv2.CascadeClassifier('./AI/Private_Mode/haarcascade/haarcascade_frontalface_default.xml')

    # if os.path.exists("trainer/Users"):
    face_id = 1
    count = 0
    faceSamples = []

    ids = []
    sg.Print('Capturing Face Data', do_not_reroute_stdout=False, no_button=True, no_titlebar=True)

    while True:
        _, img = vid_cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.4, 5)

        for (x, y, w, h) in faces:
            count += 1
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            faceSamples.append(gray[y:y + h, x:x + w])
            ids.append(face_id)
            print(f"Capturing Face Frame {face_id}.{count}")
            # time.sleep(10)

        cv2.imshow("Creating DataSet.", img)

        if count > 100:
            sg.sgprint_close()
            break

    vid_cam.release()
    cv2.destroyAllWindows()
    # time.sleep(10)
    recognizer.train(faceSamples, np.array(ids))
    check_path('./AI/Private_Mode/trainer/')
    recognizer.save('./AI/Private_Mode/trainer/' + filename + '.yml')


# learning_face()
