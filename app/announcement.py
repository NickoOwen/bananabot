import datetime
import requests
import itertools
import logging
import threading
from pydantic import BaseModel
from logging.config import fileConfig

#### Setup Logger ####
fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

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

    def __init__(self, text, time=None, mins_before=None):
        """
        Parameters
        ----------
        text : str
            The message that will be sent
        time : datetime.time
            The time the announcement will be sent
        mins_before
        """

        # Check at least one of `time` or `mins_before` is set but not both
        if time is None and mins_before is None:
            raise ValueError("Either 'time' or 'mins_before' must be set")
        if time is not None and mins_before is not None:
            raise ValueError("Both 'time' and 'mins_before' cannot be set simultaneously")
        
        # Set announcement type
        if time is not None:
            self.type = 'time'
        else:
            self.type = 'mins_before'

        self.id = next(self.id_iter)
        self.time = time
        self.text = text
        self.mins_before = mins_before


    @staticmethod
    def send_message(text):
        """
        Sends the provided text using a POST request

        Parameters
        ----------
        text : str
            The message that will be sent
        """

        json_data = {
            'text': text
        }

        # POST Request to send message
        logger.info(f"Sending request with message: {text}")
        requests.post(Announcement.url, json=json_data, verify=False)


def serialiseAnnouncement(announcement: Announcement):
    return {
        'id': announcement.id,
        'type': announcement.type,
        'time': str(announcement.time) if announcement.time is not None else None,
        'text': announcement.text,
        'mins_before': announcement.mins_before
    }

class AnnouncementWorker(threading.Thread):
    """
    A class that inherits Thread and is used to send the announcements. Makes use of threading to run standalone and sleep until it needs to send a message

    Attributes
    ----------
    stop_event : threading.Event
        a threading Event used to shutdown the worker when they are removed
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

        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.id = announcement.id
        self.time = announcement.time
        self.text = announcement.text
        self.banana_time = Announcement.banana_time
        self.selected_days = Announcement.selected_days


    def calculate_alert_time(self):
        """Calculates the alert time using the object's data"""
        return datetime.datetime.combine(datetime.date.today(), self.time)


    def run(self):
        """This function runs continuously until the Thread is terminated"""

        while True:
            # Calculate the number of seconds until the announcement needs to send the message
            current_time = datetime.datetime.now()
            
            alert_time = self.calculate_alert_time()
            
            sleep_time = alert_time - current_time
            sleep_time_seconds = sleep_time.seconds
            logger.debug(f"Announcement with ID {str(self.id)} is sleeping for {str(sleep_time_seconds)} seconds")
            self.stop_event.wait(sleep_time_seconds + 1) # Offset by 1 second

            # Break the loop if the threads have been ordered to stop
            if self.stop_event.is_set():
                logger.debug(f"Announcement {str(self.id)} stopping...")
                break

            # Check the current day and send message if required
            current_day = datetime.datetime.now().strftime('%A').lower()
            logger.debug(f"Announcement (id: {str(self.id)}) post on {current_day}: {str(self.selected_days[current_day])}")
            if self.selected_days[current_day]:
                Announcement.send_message(self.text)

            # Sleep until next day warning
            self.stop_event.wait(1)
            if self.stop_event.is_set():
                logger.debug(f"Announcement {str(self.id)} stopping...")
                break


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


class BananaTimeData(BaseModel):
    """
    A class used for transporting banana time data

    Attributes
    ----------
    time : str (optional)
        the time for banana time
    text : str (optional)
        the message for banana time
    """
    time: str = None
    text: str = None