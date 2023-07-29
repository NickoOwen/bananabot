import datetime
import uuid
import threading
from pydantic import BaseModel

from logger import get_logger

logger = get_logger()

#### Announcement ####
class Announcement:

    
    def __init__(self, text, time=None, mins_before=None):
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

        self.id = str(uuid.uuid4()) # unique ID
        self.text = text
        self.time = time
        self.mins_before = mins_before

def serialiseAnnouncement(announcement: Announcement):
    return {
        'id': announcement.id,
        'type': announcement.type,
        'text': announcement.text,
        'time': str(announcement.time) if announcement.time is not None else None,
        'mins_before': announcement.mins_before
    }


#### AnnouncementWorker ####
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
        from models import appState

        # Check at least one of `time` or `mins_before` is set but not both
        if announcement.time is None and announcement.mins_before is None:
            raise ValueError("Either 'time' or 'mins_before' must be set")
        if announcement.time is not None and announcement.mins_before is not None:
            raise ValueError("Both 'time' and 'mins_before' cannot be set simultaneously")
        
        # Set worker type
        if announcement.time is not None:
            self.type = 'time'
        else:
            self.type = 'mins_before'

        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

        self.id = announcement.id
        self.text = announcement.text
        self.time = announcement.time
        self.mins_before = announcement.mins_before
        self.banana_time = appState.banana_time
        self.selected_days = appState.selected_days

    def calculate_alert_time(self):
        """Calculates the alert time using the object's data"""

        if self.type == 'time':
            return datetime.datetime.combine(datetime.date.today(), self.time)
        else:
            normalised_time = datetime.datetime.combine(datetime.date.today(), self.banana_time)
            return normalised_time - datetime.timedelta(minutes = self.mins_before)

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