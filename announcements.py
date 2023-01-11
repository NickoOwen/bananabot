import datetime
import json
import time
import requests
import itertools
from multiprocessing import Process

# Announcement data class for storing the information of each announcement
class Announcement:
    id_iter = itertools.count()
    banana_time = datetime.time(15, 30, 0)
    # Keeps track of what days the announcements should be sent
    selected_days = {
        "monday": True,
        "tuesday": True,
        "wednesday": True,
        "thursday": True,
        "friday": True,
        "saturday": False,
        "sunday": False
    }

    def __init__(self, time, text):
        self.id = next(self.id_iter)
        self.time = time
        self.text = text

# AnnouncementWorker class that makes use of multiprocessing to allow it to run standalone and sleep until the right time
class AnnouncementWorker(Process):
    def __init__(self, announcement: Announcement):
        super(AnnouncementWorker, self).__init__()
        self.id = announcement.id
        self.time = announcement.time
        self.text = announcement.text
        self.banana_time = Announcement.banana_time
        self.selected_days = Announcement.selected_days

    def calculate_alert_time(self):
        return datetime.datetime.combine(datetime.date.today(), self.time)

    def run(self):
        while True:
            current_time = datetime.datetime.now()
            
            alert_time = self.calculate_alert_time()
            
            sleep_time = alert_time - current_time
            sleep_time_seconds = sleep_time.seconds
            print(f"[{str(datetime.datetime.now())}] DEBUG - Announcement with ID {str(self.id)} is sleeping for {str(sleep_time_seconds)} seconds")
            time.sleep(sleep_time_seconds + 1) # Offset by 1 second

            # POST Request to send message
            current_day = datetime.datetime.now().strftime('%A').lower()
            print(f"[{str(datetime.datetime.now())}] DEBUG - Announcement (id: {str(self.id)}) post on {current_day}: {str(self.selected_days[current_day])}")
            if self.selected_days[current_day]:
                url = 'https://your.endpoint.here'

                json_data = {
                    'text': self.text
                }

                requests.post(url, json=json_data, verify=False)
                print(f"[{str(datetime.datetime.now())}] INFO - Request sent with message: {self.text}")

            # Sleep until next day warning
            time.sleep(1)

# Announcement data class for storing the information of each minutes before announcement
class MinsBeforeAnnouncement(Announcement):
    def __init__(self, mins_before, text):
        super().__init__(None, text)
        self.mins_before = mins_before

# AnnouncementWorker class that makes use of multiprocessing to allow it to run standalone and sleep until the right time
class MinsBeforeAnnouncementWorker(AnnouncementWorker):
    def __init__(self, announcement: MinsBeforeAnnouncement):
        super().__init__(announcement)
        self.mins_before = announcement.mins_before

    def calculate_alert_time(self):
        normalised_time = datetime.datetime.combine(datetime.date.today(), self.banana_time)
        return normalised_time - datetime.timedelta(minutes = self.mins_before) 