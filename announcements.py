import datetime
import json
import time
import requests
import itertools
from multiprocessing import Process

class Announcement:
    id_iter = itertools.count()
    banana_time = datetime.time(15, 30, 0)

    def __init__(self, time, text):
        self.id = next(self.id_iter)
        self.time = time
        self.text = text

class AnnouncementWorker(Process):
    def __init__(self, id, time, text, banana_time, selected_days):
        super(AnnouncementWorker, self).__init__()
        self.id = id
        self.time = time
        self.text = text
        self.banana_time = banana_time
        self.selected_days = selected_days

    def calculate_alert_time(self):
        return datetime.datetime.combine(datetime.date.today(), self.time)

    def run(self):
        while True:
            current_time = datetime.datetime.now()
            
            alert_time = self.calculate_alert_time()
            
            sleep_time = alert_time - current_time
            sleep_time_seconds = sleep_time.seconds
            print("[" + str(datetime.datetime.now()) + "] DEBUG - Announcement with ID " + str(self.id) + " is sleeping for " + str(sleep_time_seconds) + " seconds")
            time.sleep(sleep_time_seconds + 1) # Offset by 1 second

            # POST Request to send message
            current_day = datetime.datetime.now().strftime('%A').lower()
            print("[" + str(datetime.datetime.now()) + "] DEBUG - Announcement (id: " + str(self.id) + ") post on " + current_day + ": " + str(self.selected_days[current_day]))
            if self.selected_days[current_day]:
                url = 'https://your.endpoint.here'

                headers = {
                    # Already added when you pass json= but not when you pass data=
                    # 'Content-Type': 'application/json'
                }

                json_data = {
                    'text': self.text
                }

                # requests.post(url, headers=headers, json=json_data, verify=False)
                print("[" + str(datetime.datetime.now()) + "] INFO - Request sent with message: " + self.text)

            # Sleep until next day warning
            time.sleep(1) # This is a hacky way to make it work

class MinsBeforeAnnouncement(Announcement):
    def __init__(self, mins_before, text):
        super().__init__(None, text)
        self.mins_before = mins_before

class MinsBeforeAnnouncementWorker(AnnouncementWorker):
    def __init__(self, id, mins_before, text, banana_time, selected_days):
        super().__init__(id, None, text, banana_time, selected_days)
        self.mins_before = mins_before

    def calculate_alert_time(self):
        normalised_time = datetime.datetime.combine(datetime.date.today(), self.banana_time)
        return normalised_time - datetime.timedelta(minutes = self.mins_before) 