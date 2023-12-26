import random
import string
import yaml
import os
import datetime
import time
import bcrypt
from typing import Dict

from .announcement import Announcement, serialiseAnnouncement
import logging

# Use FastAPI's default logger
logger = logging.getLogger("uvicorn")
logger.name = 'utilities'

def string_to_time(new_time: str):
    """Takes a string as input and returns a datetime.time object"""

    t = time.strptime(new_time, "%H:%M")
    return datetime.time(hour = t.tm_hour, minute = t.tm_min)

class AppState:
    # Properties
    banana_time = datetime.time(15, 30, 0)
    url = 'http://your.endpoint.here'

    active: bool = False
    announcements: Dict[str, Announcement] = {}
    selected_days = {
        "monday": True,
        "tuesday": True,
        "wednesday": True,
        "thursday": True,
        "friday": True,
        "saturday": False,
        "sunday": False
    }

    # Just class defaults. These are overridden in the setup
    username = 'admin'
    password = b'12345'
    salt = 'salt'

    # Workers dictionary
    workers = {}

    # Internal class variables
    _instance = None
    _configuration_file = './config/state.yaml'

    # Methods
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._load_state()
            cls.save_state(cls)

        return cls._instance
    

    @classmethod
    def _load_state(cls):
        if os.path.exists(cls._configuration_file):
            logger.info("Configuration file exists")

            try:
                with open(cls._configuration_file, 'r') as file:
                    config = yaml.safe_load(file)

                if config is not None:
                    # Get values from the config
                    app_state: AppState = AppState
                    app_state.banana_time = string_to_time(config.get('banana_time', ''))
                    app_state.url = config.get('url', '')

                    app_state.active = config.get('active', False)
                    app_state.selected_days = config.get('selected_days')

                    app_state.username = config.get('username', '')
                    app_state.password = config.get('password', '')
                    app_state.salt = config.get('salt', '')

                    announcements_data = config.get('announcements', {})
                    app_state.announcements = {}

                    # Build announcements from the data in the config
                    for announcement in announcements_data:
                        text = announcement.get('text', '')
                        time = datetime.datetime.strptime(announcement.get('time', ''), '%H:%M:%S').time() if announcement.get('time') else None
                        mins_before = announcement.get('mins_before') if 'mins_before' in announcement else None
                        new_announcement = Announcement(text, time=time, mins_before=mins_before)
                        new_announcement.id = announcement.get('id')
                        app_state.announcements[new_announcement.id] = new_announcement

                    logger.info('Configuration loaded successfully')
                    return app_state
                else:
                    logger.error('Configuration file was found and loaded but was empty')
                    logger.info("Performing first time setup to recover")
                    return cls._set_default_config(cls)
            except Exception as e:
                logger.error(f'An error occurred while loading the configuration: {e}')
                logger.info("Performing first time setup to recover")
                return cls._set_default_config(cls)
        else:
            logger.info("No configuration file detected. Performing first time setup")
            return cls._set_default_config(cls)


    def _set_default_config(cls):
        logger.info('Using default configuration')
        # Remove old config file if it exists
        if os.path.exists(cls._configuration_file):
            os.remove(cls._configuration_file)

        app_state: AppState = AppState
        app_state.active = False
        app_state.username = b'admin'

        # Create the banana time announcement
        banana_time_announcement = Announcement("@HERE Banana Time!", time=datetime.time(15, 30, 0))
        banana_time_announcement.id = "banana_time"

        # Create the default announcements
        default_announcements = [
            banana_time_announcement,
            Announcement("Banana time is at 15:30 today!", time=datetime.time(10, 0, 0)),
            Announcement("Banana time is in 60 minutes!", mins_before=60),
            Announcement("Banana time is in 30 minutes!", mins_before=30),
            Announcement("Banana time is in 10 minutes!", mins_before=10)
        ]

        # Add the default announcements to the announcements dictionary
        for announcement in default_announcements:
            app_state.announcements[announcement.id] = announcement

        # Generate credentials
        app_state.password = ''.join(random.choice(string.ascii_letters) for i in range(10))
        logger.info(f'Admin Password: {app_state.password}')
        app_state.salt = bcrypt.gensalt()
        app_state.password = bcrypt.hashpw(app_state.password.encode("utf8"), app_state.salt)

        return app_state


    def save_state(cls):
        logger.debug('Saving the app state')
        app_state = cls._instance

        # Serialise announcements
        yaml_announcements = []

        for announcement in app_state.announcements.values():
            yaml_announcements.append(serialiseAnnouncement(announcement))


        # Create a dictionary with the variables
        serialised_config = {
            'banana_time': app_state.banana_time.strftime('%H:%M'),
            'url': app_state.url,
            'active': app_state.active,
            'announcements': yaml_announcements,
            'selected_days': app_state.selected_days,
            'username': app_state.username,
            'password': app_state.password,
            'salt': app_state.salt
        }

        # Create config directory if it does not exist
        os.makedirs(os.path.dirname('./config/'), exist_ok=True)

        # Save the configuration to the YAML file
        with open(cls._configuration_file, 'w') as file:
            yaml.dump(serialised_config, file)
