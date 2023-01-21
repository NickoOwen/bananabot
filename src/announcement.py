import datetime
import time
import requests
import itertools
from multiprocessing import Process

class Announcement:
    """
    A class used to store the data for an Announcement

    Attributes
    ----------
    banana_time : datetime.time
        banana time
    selected_days :
        a dictionary that stores the days announcements should be sent
    id : int
        the announcement's id
    time : datetime.time
        the time the announcement will be sent
    text : str
        the message that will be sent
    """

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
        """
        Parameters
        ----------
        time : datetime.time
            The time the announcement will be sent
        text : str
            The message that will be sent
        """

        self.id = next(self.id_iter)
        self.time = time
        self.text = text

class AnnouncementWorker(Process):
    """
    A class that inherits Process and is used to send the announcements. Makes use of multiprocessing to run standalone and sleep until the right time

    Attributes
    ----------
    id : int
        the announcement's id
    time : datetime.time
        the time the announcement will be sent
    text : str
        the message that will be sent
    banana_time : datetime.time
        banana time
    selected_days :
        a dictionary that stores the days announcements should be sent
    """

    def __init__(self, announcement: Announcement):
        """
        Parameters
        ----------
        announcement : Announcement
            takes an Announcement as a parameter and creates the worker using the Announcement data
        """

        super(AnnouncementWorker, self).__init__()
        self.id = announcement.id
        self.time = announcement.time
        self.text = announcement.text
        self.banana_time = Announcement.banana_time
        self.selected_days = Announcement.selected_days

    def calculate_alert_time(self):
        """Calculates the alert time using the object's data"""

        return datetime.datetime.combine(datetime.date.today(), self.time)

    def run(self):
        """Inherited from Process. Is the function that runs continuously until terminated"""

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

class MinsBeforeAnnouncement(Announcement):
    """
    A class used to store the data for a minutes before Announcement. Inherits from Announcement

    Attributes
    ----------
    banana_time : datetime.time
        banana time
    selected_days :
        a dictionary that stores the days announcements should be sent
    id : int
        the announcement's id
    mins_before : int
        how many minutes before banana time to send the announcement
    text : str
        the message that will be sent
    """

    def __init__(self, mins_before, text):
        """
        Parameters
        ----------
        mins_before : int
            how many minutes before banana time to send the announcement
        text : str
            the message that will be sent
        """

        super().__init__(None, text)
        self.mins_before = mins_before

class MinsBeforeAnnouncementWorker(AnnouncementWorker):
    """
    A class that inherits AnnouncementWorker and is used to send announcements a set number of minutes before banana time

    Attributes
    ----------
    id : int
        the announcement's id
    mins_before : int
            how many minutes before banana time to send the announcement
    text : str
        the message that will be sent
    banana_time : datetime.time
        banana time
    selected_days :
        a dictionary that stores the days announcements should be sent
    """

    def __init__(self, announcement: MinsBeforeAnnouncement):
        """
        Parameters
        ----------
        announcement : MinsBeforeAnnouncement
            takes a MinsBeforeAnnouncement as a parameter and creates the worker using the MinsBeforeAnnouncement data
        """

        super().__init__(announcement)
        self.mins_before = announcement.mins_before

    def calculate_alert_time(self):
        """Calculates the alert time using the object's data"""

        normalised_time = datetime.datetime.combine(datetime.date.today(), self.banana_time)
        return normalised_time - datetime.timedelta(minutes = self.mins_before) 