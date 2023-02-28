import datetime
import time
import requests
import itertools
from multiprocessing import Process
from pydantic import BaseModel

class Announcement:
    """
    A class used to store the data for an Announcement

    Attributes
    ----------
    banana_time : datetime.time
        banana time
    url : str
        the url where the request will be sent
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
    url = 'http://your.endpoint.here' # Change this to your endpoint

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


    @staticmethod
    def send_message(text):
        json_data = {
            'text': text
        }

        # POST Request to send message
        # requests.post(Announcement.url, json=json_data, verify=False)
        print(f"[{str(datetime.datetime.now())}] INFO - Request sent with message: {text}")


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
                Announcement.send_message(self.text)

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
    

#### Data Classes ####
class AnnouncementData(BaseModel):
    """
    A class used for transporting Announcement data between the frontend and backend

    Attributes
    ----------
    type : str
        the type of announcement (time, mins_before, instant)
    time : str (optional)
        the time for a time announcement
    text : str
        the message for the announcement
    mins_before : int (optional)
        the number minutes before for a MinsBeforeAnnouncement
    """
    type: str
    time: str = None
    text: str
    mins_before: int = None


class SelectedDaysData(BaseModel):
    """
    A class used for transporting selected days data between the frontend and backend

    Attributes
    ----------
    monday : str
        the value for monday (on or off)
    tuesday : str
        the value for tuesday (on or off)
    wednesday : str
        the value for wednesday (on or off)
    thursday : str
        the value for thursday (on or off)
    friday : str
        the value for friday (on or off)
    saturday : str
        the value for saturday (on or off)
    sunday : str
        the value for sunday (on or off)
    """
    monday: str = None
    tuesday: str = None
    wednesday: str = None
    thursday: str = None
    friday: str = None
    saturday: str = None
    sunday: str = None