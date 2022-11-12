import datetime
import json
import time
import requests
import itertools
from multiprocessing import Process

class Announcement:
    id_iter = itertools.count()
    def __init__(self, time, text, banana_time):
        self.id = next(self.id_iter)
        self.time = time
        self.text = text
        self.banana_time = banana_time

class AnnouncementWorker(Process):
    def __init__(self, id, time, text, banana_time):
        super(AnnouncementWorker, self).__init__()
        self.id = id
        self.time = time
        self.text = text
        self.banana_time = banana_time

    def run(self):
        while True:
            current_time = datetime.datetime.now()
            
            alert_time = datetime.datetime.combine(datetime.date.today(), self.time)
            
            sleep_time = alert_time - current_time
            sleep_time_seconds = sleep_time.seconds
            print("[" + str(datetime.datetime.now()) + "] DEBUG - Announcement for " + str(self.time) + " sleeping for seconds: " + str(sleep_time_seconds) + " seconds")
            time.sleep(sleep_time_seconds + 1) # Offset by 1 second

            print(self.text)
            
            # POST Request to send message
            # url = 'https://your.endpoint.here'

            # headers = {
            #     # Already added when you pass json= but not when you pass data=
            #     # 'Content-Type': 'application/json'
            # }

            # json_data = {
            #     'text': self.text
            # }

            # requests.post(url, headers=headers, json=json_data, verify=False)

            # Sleep until next day warning
            time.sleep(1) # This is a hacky way to make it work

class MinsBeforeAnnouncement(Announcement):
    def __init__(self, mins_before, text, banana_time):
        super().__init__(None, text, banana_time)
        self.mins_before = mins_before

class MinsBeforeAnnouncementWorker(AnnouncementWorker):
    def __init__(self, id, mins_before, text, banana_time):
        super().__init__(id, None, text, banana_time)
        self.mins_before = mins_before

    def run(self):
        while True:
            current_time = datetime.datetime.now()
            normalised_time = datetime.datetime.combine(datetime.date.today(), self.banana_time)
            alert_time = normalised_time - datetime.timedelta(minutes = self.mins_before)
            
            sleep_time = alert_time - current_time
            sleep_time_seconds = sleep_time.seconds
            print("[" + str(datetime.datetime.now()) + "] DEBUG - Announcement for " + str(self.mins_before) + " minutes before is sleeping for " + str(sleep_time_seconds) + " seconds")
            time.sleep(sleep_time_seconds + 1) # Offset by 1 second

            print(self.text)
            
            # POST Request to send message
            # url = 'https://your.endpoint.here'

            # headers = {
            #     # Already added when you pass json= but not when you pass data=
            #     # 'Content-Type': 'application/json'
            # }

            # json_data = {
            #     'text': self.text
            # }

            # requests.post(url, headers=headers, json=json_data, verify=False)

            # Sleep until next day warning
            time.sleep(1) # This is a hacky way to make it work