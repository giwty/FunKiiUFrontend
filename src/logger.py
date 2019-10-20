import time
import sys

logs = []


def log(msg):
    global logs
    logs.append(time.strftime("%I:%M:%S") + ": " + msg)
    if sys.stdout.encoding != None:
        print(time.strftime("%I:%M:%S") + ": " +msg)
    else:
        print(time.strftime("%I:%M:%S") + ": " +
              msg.encode("utf-8", errors='replace'))


def get_logs():
    global logs
    templogs = list(logs)
    for log in templogs:
        logs.remove(log)
    return templogs
