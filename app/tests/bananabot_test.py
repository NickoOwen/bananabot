import os
from models.app_state import AppState

# Remove any config file to avoid any interference with tests
if os.path.exists(AppState._configuration_file):
    os.remove(AppState._configuration_file)

from main import *
from models import *
from utilities import *
from api.endpoints import *
from fastapi.testclient import TestClient

import pytest
import datetime

@pytest.fixture(autouse=True)
def cleanup():
    # Reset AppState class variables
    AppState.active = False
    AppState.banana_time = datetime.time(15, 30, 0)
    AppState.announcements: Dict[str, Announcement] = {}
    AppState.selected_days = {
        "monday": True,
        "tuesday": True,
        "wednesday": True,
        "thursday": True,
        "friday": True,
        "saturday": False,
        "sunday": False
    }
    AppState.username = 'admin'
    AppState.password = b'12345'
    AppState.salt = 'salt'
    AppState.workers = {}
    AppState._instance = None

    # Call get_instance to ensure default config is loaded
    AppState.get_instance()

    yield # Test runs here

    # Ensure config file is deleted and any workers are stopped
    stop()
    if os.path.exists(AppState._configuration_file):
        os.remove(AppState._configuration_file)


class TestDefaultConfig():
    def test_banana_time_announcement_exists(self):
        app_state = AppState.get_instance()
        assert "banana_time" in app_state.announcements

    def test_default_announcements_exist(self):
        app_state = AppState.get_instance()
        assert len(app_state.announcements) == 5

    def test_default_announcements_values(self):
        app_state = AppState.get_instance()
        assert any(announcement.time == datetime.time(10, 0, 0) for announcement in app_state.announcements.values()), "An announcement with time equal to 10:00 does not exist"
        assert any(announcement.time == datetime.time(15, 30, 0) for announcement in app_state.announcements.values()), "An announcement with time equal to 15:30 does not exist"

        assert any(announcement.mins_before == 10 for announcement in app_state.announcements.values()), "An announcement with mins_before equal to 10 does not exist"
        assert any(announcement.mins_before == 30 for announcement in app_state.announcements.values()), "An announcement with mins_before equal to 30 does not exist"
        assert any(announcement.mins_before == 60 for announcement in app_state.announcements.values()), "An announcement with mins_before equal to 60 does not exist"

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

        app_state = AppState.get_instance()
        assert app_state.selected_days == expected

    def test_app_banana_time_is_set(self):
        app_state = AppState.get_instance()
        assert app_state.banana_time == datetime.time(15, 30, 0)

    def test_username_is_correct(self):
        app_state = AppState.get_instance()
        assert app_state.username == b'admin'

    def test_salt_and_password_are_randomly_generated(self):
        app_state = AppState.get_instance()
        assert app_state.password is not None
        assert app_state.salt is not None
        assert app_state.password != b'12345' and app_state.password != ''
        assert app_state.salt != 'salt' and app_state.salt != ''

    def test_active_is_false_by_default(self):
        app_state = AppState.get_instance()
        assert app_state.active == False

    def test_workers_is_empty(self):
        app_state = AppState.get_instance()
        assert app_state.workers == {}


class TestConfigFunctions():
    def test_save_state_succeeds(self):
        try:
            AppState.save_state(AppState)
        except Exception as e:
            assert False, f"save_state failed: {e}"
        else:
            assert True, "save_state succeeded without any exceptions"

    def test_load_state_succeeds(self):
        try:
            test_state = AppState._load_state()
            assert test_state is not None
        except Exception as e:
            assert False, f"_load_state failed: {e}"
        else:
            assert True, "_load_state succeeded without any exceptions"


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
        app_state: AppState = AppState.get_instance()
        assert app_state.banana_time == datetime.time(15, 30, 0)
        assert app_state.announcements["banana_time"].time == datetime.time(15, 30, 0)

        banana_time_data = BananaTimeData(time='11:30')
        post_banana_time(banana_time_data)

        assert app_state.banana_time == datetime.time(11, 30, 0)
        assert app_state.announcements["banana_time"].time == datetime.time(11, 30, 0)

    def test_set_banana_text(self):
        app_state: AppState = AppState.get_instance()
        assert app_state.announcements["banana_time"].text == "@HERE Banana Time!"

        banana_text_data = BananaTimeData(text='Test text')
        post_banana_text(banana_text_data)
        assert app_state.announcements["banana_time"].text == 'Test text'

    def test_add_announcement(self):
        app_state: AppState = AppState.get_instance()
        announcement_data = AnnouncementData(type='time', text="Test announcement", time='11:11')
        new_announcement = post_announcement(announcement_data)
        assert new_announcement.id in app_state.announcements
        assert app_state.announcements[new_announcement.id].time == datetime.time(11, 11, 0)
        assert app_state.announcements[new_announcement.id].text == 'Test announcement'

    def test_add_mins_before_announcement(self):
        app_state: AppState = AppState.get_instance()
        announcement_data = AnnouncementData(type='mins_before', text="Test announcement", mins_before=7)
        new_announcement = post_announcement(announcement_data)
        assert new_announcement.id in app_state.announcements
        assert app_state.announcements[new_announcement.id].mins_before == 7
        assert app_state.announcements[new_announcement.id].text == 'Test announcement'

    def test_remove_announcement(self):
        app_state: AppState = AppState.get_instance()
        announcement_data = AnnouncementData(type='time', text="Test announcement", time='11:11')
        new_announcement = post_announcement(announcement_data)
        assert new_announcement.id in app_state.announcements
        
        remove_announcement(new_announcement.id)
        assert (new_announcement.id in app_state.announcements) == False

    def test_toggle_status(self):
        app_state: AppState = AppState.get_instance()
        assert app_state.active == False

        toggle_status()
        assert app_state.active == True
        toggle_status()
        assert app_state.active == False

    def test_removing_banana_time_announcement(self):
        app_state: AppState = AppState.get_instance()
        assert "banana_time" in app_state.announcements
        assert remove_announcement("banana_time") == False
        assert "banana_time" in app_state.announcements

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
        app_state: AppState = AppState.get_instance()
        assert app_state.selected_days == expected
        
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
        assert app_state.selected_days == expected


# Mock function for authentication
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
        mocker.patch('utilities.utilities.start', return_value=True)
        mocker.patch('utilities.utilities.stop', return_value=False)

        app.dependency_overrides[get_current_user] = mock_get_current_user

        response = client.post("/toggle-status")
        assert response.status_code == 200
        assert response.json() == True

        response = client.post("/toggle-status")
        assert response.status_code == 200
        assert response.json() == False
        app.dependency_overrides = {}
        
    def test_get_banana_time(self):
        app_state: AppState = AppState.get_instance()
        assert app_state.banana_time == datetime.time(15, 30, 0)
        response = client.get("/banana-time")
        assert response.status_code == 200
        assert response.json() == "15:30:00"


    def test_post_banana_time(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user
        app_state: AppState = AppState.get_instance()
        assert app_state.banana_time == datetime.time(15, 30, 0)

        response = client.post(
            "/banana-time",
            headers={},
            json={"time": "17:30"},
        )

        assert response.status_code == 200
        assert response.json() == "17:30:00"
        assert app_state.banana_time == datetime.time(17, 30, 0)
        app.dependency_overrides = {}


    def test_post_banana_time_without_time(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user

        response = client.post(
            "/banana-time",
            headers={},
            json={"text": "Testing without the time"},
        )

        assert response.status_code == 422
        app.dependency_overrides = {}


    def test_post_banana_text(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user
        app_state: AppState = AppState.get_instance()
        app_state.announcements['banana_time'].text = "Test"
        assert app_state.announcements['banana_time'].text == "Test"

        response = client.post(
            "/banana-text",
            headers={},
            json={"text": "test post banana text"},
        )

        assert response.status_code == 200
        assert response.json() == "test post banana text"
        app_state.announcements['banana_time'].text == "test post banana text"
        app.dependency_overrides = {}

    
    def test_post_banana_text_without_text(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user

        response = client.post(
            "/banana-text",
            headers={},
            json={"time": "15:30:00"},
        )

        assert response.status_code == 422
        app.dependency_overrides = {}


    def test_get_selected_days(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user
        response = client.get("/selected-days")
        assert response.status_code == 200
        app_state: AppState = AppState.get_instance()
        assert response.json() == app_state.selected_days
        app.dependency_overrides = {}


    def test_post_selected_days(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user
        # Confirm default selected days
        defaults = {
            "monday": True,
            "tuesday": True,
            "wednesday": True,
            "thursday": True,
            "friday": True,
            "saturday": False,
            "sunday": False
        }
        app_state: AppState = AppState.get_instance()
        assert app_state.selected_days == defaults

        response = client.post(
            "/selected-days",
            headers={},
            json={
                "tuesday": "on",
                "wednesday": "on",
                "thursday": "on",
                "friday": "on",
                "saturday": "on",
                "sunday": "on"
            },
        )

        expected = {
            "monday": False,
            "tuesday": True,
            "wednesday": True,
            "thursday": True,
            "friday": True,
            "saturday": True,
            "sunday": True
        }

        assert response.status_code == 200
        assert response.json() == expected
        assert app_state.selected_days == expected
        app.dependency_overrides = {}


    def test_get_announcements(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user
        response = client.get("/announcements")
        assert response.status_code == 200
        app.dependency_overrides = {}


    def test_post_time_announcement(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user

        response = client.post(
            "/announcements",
            headers={},
            json={
                "type": "time",
                "time": "15:30",
                "text": "test"
            },
        )

        assert response.status_code == 201
        app.dependency_overrides = {}


    def test_post_mins_before_announcement(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user

        response = client.post(
            "/announcements",
            headers={},
            json={
                "type": "mins_before",
                "mins_before": "15",
                "text": "test"
            },
        )

        assert response.status_code == 201
        app.dependency_overrides = {}


    def test_post_instant_announcement(self, mocker):
        # Mock send_message function
        mocker.patch('utilities.utilities.send_message', return_value=True)
        app.dependency_overrides[get_current_user] = mock_get_current_user

        response = client.post(
            "/announcements",
            headers={},
            json={
                "type": "instant",
                "text": "test"
            },
        )

        assert response.status_code == 201
        app.dependency_overrides = {}


    def test_post_unknown_type_announcement(self):
        # Mock send_message function
        app.dependency_overrides[get_current_user] = mock_get_current_user

        response = client.post(
            "/announcements",
            headers={},
            json={
                "type": "unknown",
                "text": "test"
            },
        )

        assert response.status_code == 400
        app.dependency_overrides = {}


    def test_delete_announcement(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user

        id = add_announcement(AnnouncementData(type="mins_before", text="test", mins_before=10)).id

        app_state: AppState = AppState.get_instance()

        assert id in app_state.announcements
        response = client.delete(f"/announcements/{id}")
        assert response.status_code == 200
        assert id not in app_state.announcements
        app.dependency_overrides = {}

    
    def test_delete_non_existent_announcement(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user
        app_state: AppState = AppState.get_instance()
        assert "9999" not in app_state.announcements
        response = client.delete(f"/announcements/9999")
        assert response.status_code == 400
        app.dependency_overrides = {}


    def test_home(self):
        response = client.get("/")
        assert response.status_code == 200


    def test_admin(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user
        response = client.get("/admin")
        assert response.status_code == 200
        app.dependency_overrides = {}


    def test_admin_unauthorised(self):
        response = client.get('/admin')
        assert response.status_code == 401 # Unauthorised


    def test_unknown_endpoint(self):
        response = client.get('/unknown-route')
        assert response.status_code == 404 # Not Found