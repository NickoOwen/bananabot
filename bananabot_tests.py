# import pytest
from bananabot import app # Flask instance of the API
from bananabot import *

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
    def test_string_to_time(self):
        result = string_to_time("15:30")
        assert type(result) == datetime.time

    def test_set_banana_time(self):
        assert Announcement.banana_time == datetime.time(15, 30, 0)
        set_banana_time("11:45")
        assert Announcement.banana_time == datetime.time(11, 45, 0)

    def test_add_announcement(self):
        announcement_id = add_announcement("9:03", "Test at 9:03 AM")
        assert announcement_id in announcements
        assert announcements[announcement_id].time == datetime.time(9, 3, 0)
        assert announcements[announcement_id].text == "Test at 9:03 AM"

    def test_add_mins_before_announcement(self):
        announcement_id = add_mins_before_announcement("24", "Test at 24 minutes before")
        assert announcement_id in announcements
        assert announcements[announcement_id].mins_before == 24
        assert announcements[announcement_id].text == "Test at 24 minutes before"

    def test_remove_announcement(self):
        announcement_id = add_announcement("9:00", "Test remove_announcement()")
        assert announcement_id in announcements
        remove_announcement(announcement_id)
        assert (announcement_id in announcements) == False

    def test_removing_banana_time_announcement(self):
        assert "banana_time" in announcements
        assert remove_announcement("banana_time") == False
        assert "banana_time" in announcements

    # Test activates multiprocessing Process objects which seems to cause errors
    # Will need to look into this more
    # def test_toggle_status(self):
    #     assert active == False
    #     toggle_status()
    #     assert active == True

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

class TestRoutes:
    def test_home_route(self):
        response = app.test_client().get('/')
        assert response.status_code == 200

    def test_about_route(self):
        response = app.test_client().get('/about')
        assert response.status_code == 200

    def test_admin_route(self):
        response = app.test_client().get('/admin')
        assert response.status_code == 401 # Unauthorised

    def test_unknown_route(self):
        response = app.test_client().get('/unknown-route')
        assert response.status_code == 404 # Not Found