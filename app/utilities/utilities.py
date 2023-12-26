import datetime
import time
import requests

from models import Announcement, AnnouncementWorker, AppState
import logging

# Use FastAPI's default logger
logger = logging.getLogger("uvicorn")
logger.name = 'utilities'



def start():
    """Creates all the workers using the data from announcements. Returns True if successful"""

    app_state = AppState.get_instance()

    if app_state.workers:
        logger.warning("Found running workers when attempting to create workers. Expected 'app_state.workers' to be empty")
        return False

    for announcement in app_state.announcements.values():
            worker = AnnouncementWorker(announcement)
            app_state.workers[worker.id] = worker
            app_state.workers[worker.id].start()

    return True


def stop():
    """Stop all running workers. Returns True if successful"""

    app_state = AppState.get_instance()

    # Check if the workers dictionary is empty
    if not app_state.workers:
        logger.warning("Tried to stop workers when no workers exist")
        return False

    for key in app_state.workers:
        app_state.workers[key].stop_event.set()
    
    app_state.workers = {}
    return True


def update():
    """Stops and re-creates all workers so they are updated with the latest system changes"""

    app_state = AppState.get_instance()
    
    if app_state.active:
        logger.debug("Updating workers")
        stop()
        start()


def initial_setup():
    """Runs the initial setup for the app after the config has been loaded"""

    app_state = AppState.get_instance()

    if app_state.active:
        logger.info('BananaBot is ACTIVE. Starting workers')
        start()


def toggle_status():
    """Toggles the status of the system (active). Returns the new value of active"""

    app_state = AppState.get_instance()

    if not app_state.active:
        app_state.active = True
        start()
        logger.info("BananaBot is now ACTIVE")
    else:
        app_state.active = False
        stop()
        logger.info("BananaBot is now INACTIVE")
    
    AppState.save_state(AppState)


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

    app_state = AppState.get_instance()

    json_data = {
        'text': text
    }

    # POST Request to send message
    logger.info(f"Sending request with message: {text}")
    requests.post(app_state.url, json=json_data, verify=False)


def add_worker(announcement: Announcement):
    app_state = AppState.get_instance()

    if app_state.active:
        worker = AnnouncementWorker(announcement)
        app_state.workers[worker.id] = worker
        app_state.workers[worker.id].start()


def remove_announcement(id: str):
    """Removes the announcement with the given id. Returns True if successful"""

    if id == 'banana_time':
        logger.warning("Attempted to remove the banana time announcement. This action is not permitted")
        return False

    app_state = AppState.get_instance()
    
    if id not in app_state.announcements:
        logger.warning("Attempted to remove a non-existent announcement")
        return False

    app_state.announcements.pop(id)

    if app_state.active:
        logger.info(f"Terminating worker with ID {id}")
        app_state.workers[id].stop_event.set()
        app_state.workers.pop(id)

    logger.info(f"Announcement with ID {id} has been removed")
    AppState.save_state(AppState)
    return True