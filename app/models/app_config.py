import random
import string
import yaml
import os
import datetime
import time
import bcrypt
from typing import Dict

from .announcement import Announcement, serialiseAnnouncement
from logger import get_logger

logger = get_logger()
logger.name = 'app_config'

class AppConfig:
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

configuration_file = './config/state.yaml'

def saveConfig(config):
    logger.debug('Saving config')

    # Serialise announcements
    yaml_announcements = []

    for announcement in config.announcements.values():
        yaml_announcements.append(serialiseAnnouncement(announcement))


    # Create a dictionary with the variables
    serialisedConfig = {
        'banana_time': config.banana_time.strftime('%H:%M'),
        'url': config.url,
        'active': config.active,
        'announcements': yaml_announcements,
        'selected_days': config.selected_days,
        'username': config.username,
        'password': config.password,
        'salt': config.salt
    }

    # Save the configuration to the YAML file
    with open(configuration_file, 'w') as file:
        yaml.dump(serialisedConfig, file)


def string_to_time(new_time: str):
    """Takes a string as input and returns a datetime.time object"""

    t = time.strptime(new_time, "%H:%M")
    return datetime.time(hour = t.tm_hour, minute = t.tm_min)


def generateDefaultConfig():
    logger.debug('Generating default configuration...')
    app_config = AppConfig
    app_config.active = False
    app_config.username = b'admin'

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
        app_config.announcements[announcement.id] = announcement

    # Generate credentials
    app_config.password = ''.join(random.choice(string.ascii_letters) for i in range(10))
    logger.info(f'Admin Password: {app_config.password}')
    app_config.salt = bcrypt.gensalt()
    app_config.password = bcrypt.hashpw(app_config.password.encode("utf8"), app_config.salt)


    # Create the config directory if it doesn't exist and save config
    os.makedirs(os.path.dirname('./config/'), exist_ok=True)
    saveConfig(app_config)

    return app_config


def loadConfig():
    if os.path.exists(configuration_file):
        logger.debug("Configuration file exists")

        try:
            with open(configuration_file, 'r') as file:
                config = yaml.safe_load(file)

            if config is not None:
                # Use try to catch any exceptions if the config is not valid
                try:
                    app_config = AppConfig
                    app_config.banana_time = string_to_time(config.get('banana_time', ''))
                    app_config.url = config.get('url', '')

                    app_config.active = config.get('active', False)
                    app_config.selected_days = config.get('selected_days')

                    app_config.username = config.get('username', '')
                    app_config.password = config.get('password', '')
                    app_config.salt = config.get('salt', '')

                    announcements_data = config.get('announcements', {})
                    app_config.announcements = {}

                    for announcement in announcements_data:
                        text = announcement['text']
                        time = datetime.datetime.strptime(announcement['time'], '%H:%M:%S').time() if announcement['time'] else None
                        mins_before = announcement['mins_before'] if 'mins_before' in announcement else None

                        new_announcement = Announcement(text, time=time, mins_before=mins_before)
                        new_announcement.id = announcement['id']

                        app_config.announcements[new_announcement.id] = new_announcement

                    logger.info('Configuration loaded successfully')
                    return app_config
                except:
                    logger.error('An error occurred while loading the configuration')
            else:
                logger.error('Configuration file was found and loaded but was empty')
        except:
            logger.error('An error occurred while loading the configuration file (possibly malformed YAML)')
    else:
        logger.info("No configuration file detected. Performing first time setup")
        return generateDefaultConfig()
    
    # Return default configuration if an error occurs while loading or reading the configuration / file
    logger.warning('An error occurred while attempting to load or read the configuration file. Performing first time setup to recover')
    return generateDefaultConfig()

        
    
# Global Variables
appState: AppConfig = loadConfig()
workers = {}
