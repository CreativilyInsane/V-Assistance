from datetime import datetime
# import pythoncom

# pythoncom.PumpMessages()

import time
from threading import Thread, Timer
from AI.Response import thread_list
from threading import Timer


def log(ThreadName):
    timeStramp = datetime.now()
    with open('thread_log.txt', '+a') as f:
        f.write(timeStramp.strftime(
            "%b %d %Y %I %M %S") + " " + ThreadName + "\n--------------------------------------------------"
                                                      "-----------\n")


def threadappend(thread):
    log(thread.getName())
    thread_list.append(thread)


def remove_dead_thread(thread):
    thread_list.remove(thread)


def check_thread(thread_name):
    for thread in thread_list:
        if thread.name == thread_name:
            if thread.is_alive():
                return thread
    return False


# def named_timer(name, interval, function, *args, **kwargs):
#     """Factory function to create named Timer objects.
#
#       Named timers call a function after a specified number of seconds:
#
#           t = named_timer('Name', 30.0, function)
#           t.start()
#           t.cancel()  # stop the timer's action if it's still waiting
#     """
#     timer = Timer(interval, function, *args, **kwargs)
#     timer.name = name
#     return timer
