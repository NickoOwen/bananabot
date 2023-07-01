import yaml
import os
import datetime
import bcrypt
from typing import Dict

from .announcement import Announcement, serialiseAnnouncement

class AppConfig:
    banana_time = datetime.time(15, 30, 0) # TODO this needs to be "serialised" for saving/loading
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

    username = 'admin'
    password = '12345'
    salt = 'saaaltyy'

state_file = './config/state.yaml'

def saveConfig(config: AppConfig):
    print('Saving config')

    # Serialise announcements
    yaml_announcements = []

    for announcement in config.announcements.values():
        yaml_announcements.append(serialiseAnnouncement(announcement))


    # Create a dictionary with the variables
    serialisedConfig = {
        'banana_time': str(config.banana_time),
        'url': config.url,
        'active': config.active,
        'announcements': yaml_announcements,
        'selected_days': config.selected_days,
        'username': config.username,
        'password': config.password,
        'salt': config.salt
    }

    # Save the configuration to the YAML file
    with open(state_file, 'w') as file:
        yaml.dump(serialisedConfig, file)

def loadConfig():
    if os.path.exists(state_file):
        print("App state exists")

        try:
            with open(state_file, 'r') as file:
                config = yaml.safe_load(file)

            if config is not None:
                app_config = AppConfig

                app_config.active = config.get('active', False)
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

                print('Config loaded successfully')

                return app_config
            else:
                # TODO proper logging / errors
                print('No saved configuration found')

        except FileNotFoundError:
            print('No saved configuration found')
        except Exception as e:
            print('An error occurred while loading the configuration:', str(e))
    
    else:
        print("App state does not exist")

        # Return default AppConfig
        app_config = AppConfig
        app_config.active = False
        app_config.username = 'admin'

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
        # password = ''.join(random.choice(string.ascii_letters) for i in range(10))
        app_config.password = '12345' # TODO make this random
        print(f'Admin Password: ', app_config.password)
        app_config.salt = bcrypt.gensalt()
        app_config.password = bcrypt.hashpw(app_config.password.encode("utf8"), app_config.salt)


        # Create the config directory if it doesn't exist
        os.makedirs(os.path.dirname('./config'), exist_ok=True)
        saveConfig(app_config)
        return app_config

