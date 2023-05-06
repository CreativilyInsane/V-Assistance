from datetime import datetime
import cv2
import time
import getpass
import os


def takepic(id, path=None):
    now = datetime.now()
    if not path:
        user = getpass.getuser()
        path = f"C:\\Users\\{user}\\Pictures\\Camera Roll"
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        cap = cv2.VideoCapture(id, cv2.CAP_DSHOW)

        if not cap.isOpened():
            raise IOError("Cannot open webcam")
        _, frame = cap.read()
        # start = time.time()
        # end = time.time()

        # print(end - start)
        # image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(path+"/"+now.strftime("%b %d %Y %I %M %S")+".jpg", frame)
        cap.release()
    except:
        pass

def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    is_working = True
    dev_port = 0
    working_ports = []
    available_ports = []
    while is_working:
        camera = cv2.VideoCapture(dev_port, cv2.CAP_DSHOW)
        if not camera.isOpened():
            is_working = False
            # print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                # print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                Camera_Detail = {"Camera_Id":dev_port, "Height":h, "Width": w}
                working_ports.append(Camera_Detail)
            else:
                # print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                Camera_Detail = {"Camera_Id":dev_port, "Height":h,"Width": w}
                available_ports.append(Camera_Detail)
        dev_port +=1
    return working_ports

