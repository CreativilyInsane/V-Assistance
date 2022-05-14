from win10toast import ToastNotifier
from threading import Thread


class Notification(Thread):
    def __init__(self, msg, Title = "V"):
        Thread.__init__(self)
        self.toaster = ToastNotifier()
        self.Title = Title
        self.Msg = msg

    def run(self) -> None:
        self.toaster.show_toast(self.Title, self.Msg,icon_path="./AI/Images/NotificationLogo.ico", duration=2)

