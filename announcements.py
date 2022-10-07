import datetime
import time
import requests
from multiprocessing import Process

class MinsBeforeAnnouncement:
    def __init__(self, minsBefore, text):
        self.minsBefore = minsBefore
        self.text = text

class MinsBeforeAnnouncementWorker(Process):
    def __init__(self, minsBefore, text, time):
        super(MinsBeforeAnnouncementWorker, self).__init__()
        self.minsBefore = minsBefore
        self.text = text
        self.time = time

    def run(self):
        while True:
            currentTime = datetime.datetime.now()
            normalisedTime = datetime.datetime.combine(datetime.date.today(), self.time)
            alertTime = normalisedTime - datetime.timedelta(minutes = self.minsBefore)
            
            sleepTime = alertTime - currentTime
            sleepTimeSeconds = sleepTime.seconds
            print("[" + str(datetime.datetime.now()) + "] DEBUG - Announcement for " + str(self.minsBefore) + " minutes before is sleeping for " + str(sleepTimeSeconds) + " seconds")
            time.sleep(sleepTimeSeconds)

            print(self.text)
            # curl chat app here with self.text

            # Sleep until next day warning
            time.sleep(1) # This is a hacky way to make it work

class TimeAnnouncement:
    def __init__(self, time, text):
        self.time = time
        self.text = text

class TimeAnnouncementWorker(Process):
    def __init__(self, announcementTime, text, time):
        super(TimeAnnouncementWorker, self).__init__()
        self.annoucementTime = announcementTime
        self.text = text
        self.time = time

    def run(self):
        while True:
            currentTime = datetime.datetime.now()
            
            alertTime = datetime.datetime.combine(datetime.date.today(), self.time)
            
            sleepTime = alertTime - currentTime
            sleepTimeSeconds = sleepTime.seconds
            print("[" + str(datetime.datetime.now()) + "] DEBUG Announcement for " + str(self.time) + " sleeping for seconds: " + str(sleepTimeSeconds) + " seconds")
            time.sleep(sleepTimeSeconds + 1) # Offset by 1 second

            print(self.text)
            # curl chat app here with self.text

            # Sleep until next day warning
            time.sleep(1) # This is a hacky way to make it work
