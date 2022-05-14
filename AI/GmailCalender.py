from __future__ import print_function
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
from AI.SpeakAndListen import speak, get_audio
import pytz
import os.path

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
CALANDER_STRS = ["what do i have","do i have plans", "is i am free", "am i busy"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

def auth_google():

    creds = None

    if os.path.exists('./AI/Jsons/token.pickle'):
        with open('./AI/Jsons/token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            speak("refreshing credentials")
            creds.refresh(Request())
        else:
            speak("you need to give a access to use this feature")
            flow = InstalledAppFlow.from_client_secrets_file('./AI/Jsons/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('./AI/Jsons/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(date):
    service = auth_google()
    date =  datetime.datetime.combine(date, datetime.datetime.min.time())
    end_date =  datetime.datetime.combine(date, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        # print(f"You Have  {len(events)} events on this day.")
        speak(f"You Have  {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("00")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time.replace(":","") + "A M"
            else:
                start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
                start_time = start_time + "P M"

            speak(event["summary"] + "at" + start_time)

def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_weeks = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_weeks = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year + 1

    if day < today.day and month == -1 and day != -1:
        month += 1

    if month == -1 and day == -1 and day_of_weeks != -1:
        current_day_of_week = today.weekday()
        dif = day_of_weeks - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)
    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year)



