from bananabot import *
from fastapi.testclient import TestClient

class TestDefaultConfig:
    def test_default_announcements_exist(self):
        assert "banana_time" in announcements # ID of banana time announcement
        assert 1 in announcements # ID of 10:00 announcement
        assert 2 in announcements # ID of 60 mins before announcement
        assert 3 in announcements # ID of 30 mins before announcement
        assert 4 in announcements # ID of 10 mins before announcement

    def test_default_banana_time(self):
        assert "banana_time" in announcements
        assert Announcement.banana_time == datetime.time(15, 30, 0)
        assert announcements["banana_time"].time == datetime.time(15, 30, 0)
        assert announcements["banana_time"].text == "# @HERE Banana Time!"

    def test_default_active_value(self):
        assert active == False


class TestFunctions:
    def test_start(self, mocker):
        mocker.patch('bananabot.workers', {"1": 1, "2": 2})

        assert start() == False

    def test_stop(self, mocker):
        mocker.patch('bananabot.workers', {})

        assert stop() == False

    def test_string_to_time(self):
        result = string_to_time("15:30")
        assert type(result) == datetime.time

    def test_set_banana_time(self):
        # Ensure banana_time is set to the default value
        Announcement.banana_time = datetime.time(15, 30, 0)
        assert Announcement.banana_time == datetime.time(15, 30, 0)

        set_banana_time("11:45")
        assert Announcement.banana_time == datetime.time(11, 45, 0)

    def test_add_announcement(self, mocker):
        mocker.patch('bananabot.active', False)

        announcement_id = add_time_announcement("9:03", "Test at 9:03 AM")
        assert announcement_id in announcements
        assert announcements[announcement_id].time == datetime.time(9, 3, 0)
        assert announcements[announcement_id].text == "Test at 9:03 AM"

    def test_add_mins_before_announcement(self, mocker):
        mocker.patch('bananabot.active', False)

        announcement_id = add_mins_before_announcement("24", "Test at 24 minutes before")
        assert announcement_id in announcements
        assert announcements[announcement_id].mins_before == 24
        assert announcements[announcement_id].text == "Test at 24 minutes before"

    def test_remove_announcement(self):
        announcement_id = add_time_announcement("9:00", "Test remove_announcement()")
        assert announcement_id in announcements
        
        remove_announcement(announcement_id)
        assert (announcement_id in announcements) == False

    def test_toggle_status(self, mocker):
        # Mock functions
        mocker.patch('bananabot.start', return_value=True)
        mocker.patch('bananabot.stop', return_value=False)

        assert toggle_status() == True
        assert toggle_status() == False

    def test_removing_banana_time_announcement(self):
        assert "banana_time" in announcements
        assert remove_announcement("banana_time") == False
        assert "banana_time" in announcements

    def test_update_selected_days(self):
        expected = {
            "monday": True,
            "tuesday": True,
            "wednesday": True,
            "thursday": True,
            "friday": True,
            "saturday": False,
            "sunday": False
        }
        assert Announcement.selected_days == expected
        expected["sunday"] = True
        update_selected_days(expected)
        assert Announcement.selected_days == expected
        assert Announcement.selected_days["sunday"] == True


# Mock function for authentication
client = TestClient(app)

def mock_get_current_user():
    return

class TestApiEndpoints:
    def test_toggle_status(self, mocker):
        # Mock functions
        mocker.patch('bananabot.start', return_value=True)
        mocker.patch('bananabot.stop', return_value=False)
        mocker.patch('bananabot.active', False)

        app.dependency_overrides[get_current_user] = mock_get_current_user

        response = client.post("/toggle-status")
        assert response.status_code == 200
        assert response.json() == True

        response = client.post("/toggle-status")
        assert response.status_code == 200
        assert response.json() == False
        app.dependency_overrides = {}
        

    def test_get_banana_time(self):
        Announcement.banana_time = datetime.time(15, 30, 0)
        response = client.get("/banana-time")
        assert response.status_code == 200
        assert response.json() == "15:30:00"


    def test_post_banana_time(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user
        Announcement.banana_time = datetime.time(15, 30, 0)

        response = client.post(
            "/banana-time",
            headers={},
            json={"time": "17:30"},
        )

        assert response.status_code == 200
        assert response.json() == "17:30:00"
        app.dependency_overrides = {}


    def test_post_banana_text(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user
        announcements['banana_time'].text = "Test"

        response = client.post(
            "/banana-text",
            headers={},
            json={"text": "test post banana text"},
        )

        assert response.status_code == 200
        assert response.json() == "test post banana text"
        app.dependency_overrides = {}


    def test_get_selected_days(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user
        response = client.get("/selected-days")
        assert response.status_code == 200
        assert response.json() == Announcement.selected_days
        app.dependency_overrides = {}


    def test_post_selected_days(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user
        Announcement.selected_days = {
            "monday": True,
            "tuesday": True,
            "wednesday": True,
            "thursday": True,
            "friday": True,
            "saturday": False,
            "sunday": False
        }

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
        mocker.patch('announcement.Announcement.send_message', return_value=True)
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


    def test_delete_announcement(self):
        app.dependency_overrides[get_current_user] = mock_get_current_user

        id = add_time_announcement("10:00", "test")

        assert id in announcements
        response = client.delete(f"/announcements/{id}")
        assert response.status_code == 200
        assert id not in announcements
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