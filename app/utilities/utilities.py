import datetime
import time
import requests

from models import Announcement, AnnouncementWorker, appState, workers, saveConfig
from logger import get_logger

logger = get_logger()


def start():
    """Creates all the workers using the data from announcements. Returns True if successful"""

    if workers:
        logger.warning("Found running workers when attempting to create workers. Expected 'workers' to be empty")
        return False

    for announcement in appState.announcements.values():
            worker = AnnouncementWorker(announcement)
            workers[worker.id] = worker
            workers[worker.id].start()

    return True


def stop():
    """Stop all running workers. Returns True if successful"""

    # Check if the workers dictionary is empty
    if not workers:
        logger.warning("Tried to stop workers when no workers exist")
        return False

    for key in workers:
        workers[key].stop_event.set()
    
    workers = {}
    return True


def update():
    """Stops and re-creates all workers so they are updated with the latest system changes"""
    
    if appState.active:
        logger.debug("Updating workers...")
        stop()
        start()


def toggle_status():
    """Toggles the status of the system (active). Returns the new value of active"""

    if not appState.active:
        appState.active = True
        start()
        logger.info("BananaBot is now ACTIVE")
    else:
        appState.active = False
        stop()
        logger.info("BananaBot is now INACTIVE")
    
    saveConfig(appState)


def string_to_time(new_time: str):
    """Takes a string as input and returns a datetime.time object"""

    t = time.strptime(new_time, "%H:%M")
    return datetime.time(hour = t.tm_hour, minute = t.tm_min)


def send_message(text: str):
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
    requests.post(appState.url, json=json_data, verify=False)


def add_worker(announcement: Announcement):
    if appState.active:
        worker = AnnouncementWorker(announcement)
        workers[worker.id] = worker
        workers[worker.id].start()


def remove_announcement(id: str):
    """Removes the announcement with the given id. Returns True if successful"""

    if id == 'banana_time':
        logger.warning("Attempted to remove the banana time announcement. This action is not permitted")
        return False
    
    if id not in appState.announcements:
        logger.warning("Attempted to remove a non-existent announcement")
        return False

    appState.announcements.pop(id)

    if appState.active:
        logger.info(f"Terminating worker with ID {id}")
        workers[id].stop_event.set()
        workers.pop(id)

    logger.info(f"Announcement with ID {id} has been removed")
    saveConfig(appState)
    return True