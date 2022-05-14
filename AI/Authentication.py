import re
import smtplib
from AI.Response import errorresponse
from AI.EncryptionDecryption import gmail_crediential_encrypt
# from AI.globvar import email, password
from AI.SpeakAndListen import speak


def check(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    else:
        return False


def Authentication(mail, password, gender=None, rate=None):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(mail, password)
        speak("Authenticate is complete", gender, rate)
        return True
    except smtplib.SMTPAuthenticationError:
        return False
