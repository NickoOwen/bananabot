from main import *
from models import *
from models.app_config import generateDefaultConfig, configuration_file, saveConfig, loadConfig, workers, appState
from utilities import *
from api.endpoints import *

import pytest
import datetime
import os
import copy

from fastapi.testclient import TestClient

defaultAppState = copy.copy(appState)

# Function to remove the config directory after each test
@pytest.fixture(autouse=True)
def cleanup():
    global appState
    appState = copy.copy(defaultAppState)
    yield

    # Ensure config file is deleted and any workers are stopped
    stop()
    if os.path.exists(configuration_file):
        os.remove(configuration_file)


class TestDefaultConfig():
    def test_config_issues(self):
        appState.announcements['testID'] = Announcement('test', mins_before=10)
        assert True

    def test_default_announcements_exist(self):
        appState = copy.copy(defaultAppState)
        assert len(appState.announcements) == 5
    
    def test_banana_time_announcement_exists(self):
        assert "banana_time" in appState.announcements

    def test_default_announcements_values(self):
        assert any(announcement.time == datetime.time(10, 0, 0) for announcement in appState.announcements.values()), "An announcement with time equal to 10:00 does not exist"
        assert any(announcement.time == datetime.time(15, 30, 0) for announcement in appState.announcements.values()), "An announcement with time equal to 15:30 does not exist"
        
        assert any(announcement.mins_before == 10 for announcement in appState.announcements.values()), "An announcement with mins_before equal to 10 does not exist"
        assert any(announcement.mins_before == 30 for announcement in appState.announcements.values()), "An announcement with mins_before equal to 30 does not exist"
        assert any(announcement.mins_before == 60 for announcement in appState.announcements.values()), "An announcement with mins_before equal to 60 does not exist"

    def test_default_selected_days(self):
        expected = {
            "monday": True,
            "tuesday": True,
            "wednesday": True,
            "thursday": True,
            "friday": True,
            "saturday": False,
            "sunday": False
        }
        assert appState.selected_days == expected

    def test_app_banana_time_is_set(self):
        assert appState.banana_time == datetime.time(15, 30, 0)

    def test_username_is_correct(self):
        assert appState.username == b'admin'

    def test_salt_and_password_are_randomly_generated(self):
        assert appState.password is not None
        assert appState.salt is not None
        assert appState.password != b'12345' and appState.password != ''
        assert appState.salt != 'salt' and appState.salt != ''

    def test_active_is_false_by_default(self):
        assert appState.active == False

    def test_workers_is_empty(self):
        assert workers == {}


class TestConfigFunctions():
    def test_save_config_succeeds(self):
        # Test saveConfig
        try:
            saveConfig(appState)
        except Exception as e:
            assert False, f"saveConfig failed: {e}"
        else:
            assert True, "saveConfig succeeded without any exceptions"

    def test_load_config_succeeds(self):
        # Test loadConfig
        try:
            dummyState = loadConfig()
            assert dummyState is not None
        except Exception as e:
            assert False, f"loadConfig failed: {e}"
        else:
            assert True, "loadConfig succeeded without any exceptions"


class TestFunctions:
    def test_start(self):
        start()
        assert start() == False

    def test_stop(self):
        assert stop() == False

    def test_string_to_time(self):
        result = string_to_time("15:30")
        assert type(result) == datetime.time

    def test_set_banana_time(self):
        assert appState.banana_time == datetime.time(15, 30, 0)
        assert appState.announcements["banana_time"].time == datetime.time(15, 30, 0)

        banana_time_data = BananaTimeData(time='11:30')
        post_banana_time(banana_time_data)

        assert appState.banana_time == datetime.time(11, 30, 0)
        assert appState.announcements["banana_time"].time == datetime.time(11, 30, 0)

    def test_set_banana_text(self):
        assert appState.announcements["banana_time"].text == "@HERE Banana Time!"

        banana_text_data = BananaTimeData(text='Test text')
        post_banana_text(banana_text_data)
        assert appState.announcements["banana_time"].text == 'Test text'

    def test_add_announcement(self):
        announcement_data = AnnouncementData(type='time', text="Test announcement", time='11:11')
        new_announcement = post_announcement(announcement_data)
        assert new_announcement.id in appState.announcements
        assert appState.announcements[new_announcement.id].time == datetime.time(11, 11, 0)
        assert appState.announcements[new_announcement.id].text == 'Test announcement'

    def test_add_mins_before_announcement(self):
        announcement_data = AnnouncementData(type='mins_before', text="Test announcement", mins_before=7)
        new_announcement = post_announcement(announcement_data)
        assert new_announcement.id in appState.announcements
        assert appState.announcements[new_announcement.id].mins_before == 7
        assert appState.announcements[new_announcement.id].text == 'Test announcement'

    def test_remove_announcement(self):
        announcement_data = AnnouncementData(type='time', text="Test announcement", time='11:11')
        new_announcement = post_announcement(announcement_data)
        assert new_announcement.id in appState.announcements
        
        remove_announcement(new_announcement.id)
        assert (new_announcement.id in appState.announcements) == False

    def test_toggle_status(self):
        assert appState.active == False

        toggle_status()
        assert appState.active == True
        toggle_status()
        assert appState.active == False

    def test_removing_banana_time_announcement(self):
        assert "banana_time" in appState.announcements
        assert remove_announcement("banana_time") == False
        assert "banana_time" in appState.announcements

    def test_update_selected_days(self):
        # Confirm default selected days
        expected = {
            "monday": True,
            "tuesday": True,
            "wednesday": True,
            "thursday": True,
            "friday": True,
            "saturday": False,
            "sunday": False
        }
        assert appState.selected_days == expected
        
        # Update selected days
        selected_days_data = SelectedDaysData(
            monday = 'on',
            tuesday = 'on',
            wednesday = 'on',
            thursday = 'on',
            friday = 'on',
            saturday = 'off',
            sunday = 'on'
        )
        post_selected_days(selected_days_data)

        # Check current selected_days
        expected["sunday"] = True
        assert appState.selected_days == expected


# # Mock function for authentication
client = TestClient(app)

def mock_get_current_user():
    return

class TestApiEndpoints:
    def test_get_favicon(self):
        response = client.get("/favicon.ico")
        assert response.status_code == 200

    def test_get_profile_picture(self):
        response = client.get("/profile-picture")
        assert response.status_code == 200

    def test_toggle_status(self, mocker):
        # Mock functions
        mocker.patch('utilities.start', return_value=True)
        mocker.patch('utilities.stop', return_value=False)

        app.dependency_overrides[get_current_user] = mock_get_current_user

        response = client.post("/toggle-status")
        assert response.status_code == 200
        assert response.json() == True

        response = client.post("/toggle-status")
        assert response.status_code == 200
        assert response.json() == False
        app.dependency_overrides = {}
        
    def test_get_banana_time(self):
        assert appState.banana_time == datetime.time(15, 30, 0), str(appState.banana_time)
        response = client.get("/banana-time")
        assert response.status_code == 200
        assert response.json() == "15:30:00"


#     def test_post_banana_time(self):
#         app.dependency_overrides[get_current_user] = mock_get_current_user
#         Announcement.banana_time = datetime.time(15, 30, 0)

#         response = client.post(
#             "/banana-time",
#             headers={},
#             json={"time": "17:30"},
#         )

#         assert response.status_code == 200
#         assert response.json() == "17:30:00"
#         app.dependency_overrides = {}


#     def test_post_banana_time_without_time(self):
#         app.dependency_overrides[get_current_user] = mock_get_current_user

#         response = client.post(
#             "/banana-time",
#             headers={},
#             json={"text": "Testing without the time"},
#         )

#         assert response.status_code == 422
#         app.dependency_overrides = {}


#     def test_post_banana_text(self):
#         app.dependency_overrides[get_current_user] = mock_get_current_user
#         announcements['banana_time'].text = "Test"

#         response = client.post(
#             "/banana-text",
#             headers={},
#             json={"text": "test post banana text"},
#         )

#         assert response.status_code == 200
#         assert response.json() == "test post banana text"
#         app.dependency_overrides = {}

    
#     def test_post_banana_text_without_text(self):
#         app.dependency_overrides[get_current_user] = mock_get_current_user

#         response = client.post(
#             "/banana-text",
#             headers={},
#             json={"time": "15:30:00"},
#         )

#         assert response.status_code == 422
#         app.dependency_overrides = {}


#     def test_get_selected_days(self):
#         app.dependency_overrides[get_current_user] = mock_get_current_user
#         response = client.get("/selected-days")
#         assert response.status_code == 200
#         assert response.json() == Announcement.selected_days
#         app.dependency_overrides = {}


#     def test_post_selected_days(self):
#         app.dependency_overrides[get_current_user] = mock_get_current_user
#         Announcement.selected_days = {
#             "monday": True,
#             "tuesday": True,
#             "wednesday": True,
#             "thursday": True,
#             "friday": True,
#             "saturday": False,
#             "sunday": False
#         }

#         response = client.post(
#             "/selected-days",
#             headers={},
#             json={
#                 "tuesday": "on",
#                 "wednesday": "on",
#                 "thursday": "on",
#                 "friday": "on",
#                 "saturday": "on",
#                 "sunday": "on"
#             },
#         )

#         expected = {
#             "monday": False,
#             "tuesday": True,
#             "wednesday": True,
#             "thursday": True,
#             "friday": True,
#             "saturday": True,
#             "sunday": True
#         }

#         assert response.status_code == 200
#         assert response.json() == expected
#         app.dependency_overrides = {}


#     def test_get_announcements(self):
#         app.dependency_overrides[get_current_user] = mock_get_current_user
#         response = client.get("/announcements")
#         assert response.status_code == 200
#         app.dependency_overrides = {}


#     def test_post_time_announcement(self):
#         app.dependency_overrides[get_current_user] = mock_get_current_user

#         response = client.post(
#             "/announcements",
#             headers={},
#             json={
#                 "type": "time",
#                 "time": "15:30",
#                 "text": "test"
#             },
#         )

#         assert response.status_code == 201
#         app.dependency_overrides = {}


#     def test_post_mins_before_announcement(self):
#         app.dependency_overrides[get_current_user] = mock_get_current_user

#         response = client.post(
#             "/announcements",
#             headers={},
#             json={
#                 "type": "mins_before",
#                 "mins_before": "15",
#                 "text": "test"
#             },
#         )

#         assert response.status_code == 201
#         app.dependency_overrides = {}


#     def test_post_instant_announcement(self, mocker):
#         # Mock send_message function
#         mocker.patch('announcement.Announcement.send_message', return_value=True)
#         app.dependency_overrides[get_current_user] = mock_get_current_user

#         response = client.post(
#             "/announcements",
#             headers={},
#             json={
#                 "type": "instant",
#                 "text": "test"
#             },
#         )

#         assert response.status_code == 201
#         app.dependency_overrides = {}


#     def test_post_unknown_type_announcement(self):
#         # Mock send_message function
#         app.dependency_overrides[get_current_user] = mock_get_current_user

#         response = client.post(
#             "/announcements",
#             headers={},
#             json={
#                 "type": "unknown",
#                 "text": "test"
#             },
#         )

#         assert response.status_code == 400
#         app.dependency_overrides = {}


#     def test_delete_announcement(self):
#         app.dependency_overrides[get_current_user] = mock_get_current_user

#         id = add_time_announcement("10:00", "test")

#         assert id in announcements
#         response = client.delete(f"/announcements/{id}")
#         assert response.status_code == 200
#         assert id not in announcements
#         app.dependency_overrides = {}

    
#     def test_delete_non_existent_announcement(self):
#         app.dependency_overrides[get_current_user] = mock_get_current_user
#         assert 9999 not in announcements
#         response = client.delete(f"/announcements/{9999}")
#         assert response.status_code == 400
#         app.dependency_overrides = {}


#     def test_home(self):
#         response = client.get("/")
#         assert response.status_code == 200


#     def test_admin(self):
#         app.dependency_overrides[get_current_user] = mock_get_current_user
#         response = client.get("/admin")
#         assert response.status_code == 200
#         app.dependency_overrides = {}


#     def test_admin_unauthorised(self):
#         response = client.get('/admin')
#         assert response.status_code == 401 # Unauthorised


#     def test_unknown_endpoint(self):
#         response = client.get('/unknown-route')
#         assert response.status_code == 404 # Not Found