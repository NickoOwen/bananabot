# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

#### Added
- The ability to set the password via the administrator interface
- A cool animation on the BananaBot home page when it reaches banana time

## [4.2.1] - 2024-03-04

#### Fixed
- Updated Python packages to address security issues

## [4.2.0] - 2024-01-02

#### Added
- Implemented storing the application state to enable persistence between restarts, recovery from failure etc.
- Some small quality of life improvements in the admin UI

#### Fixed
- Fixed requirement conflicts introduced in the 4.1.1 release
- Major refactor of the code structure to make it more readable and maintainable
- Addressed security issues with Python dependencies

## [4.1.0] - 2023-06-01
- Updated the admin user interface
- Added a side navigation bar to the admin UI
- Content in the admin UI is now dynamically loaded and only loads the options a user is currently editing (based on the category selected in the sidebar)
- Added descriptions for further clarification of each setting in the admin UI and additional feedback for the user when making changes

## [4.0.0] - 2023-03-09

#### Added
- Switched from Flask to use FastAPI as the framework was better suited for BananaBot
- Implemented AJAX requests to make the UI experience smoother, more robust, and eliminate the need to refresh the page when a change is made
- Added a new and improved home page UI designed by [@BasilDimopoulos](https://github.com/BasilDimopoulos) which features a timer that counts down to banana time
- Improved security by storing the hashed and salted password
- Added the MIT license
- Switched the `AnnouncementWorker` class to inherit from `Thread` instead of `Process` due to issues relating to [this GitHub issue](https://github.com/tiangolo/fastapi/issues/1487)

## [3.3.0] - 2023-02-15

#### Added
- Added instant messaging feature to the admin page where an admin can instantly send a message

## [3.2.1] - 2023-01-26

#### Added
- Unit tests using `pytest`
- Modified the project structure to make it easier to maintain and allow unit tests to import easily
- Additional logging throughout the application to make debugging potential issues easier

#### Fixed
- Fixed a bug where setting the banana time message would not take immediate effect

## [3.2.0] - 2023-01-10

#### Added
- The ability to configure which days of the week announcements are sent
- Updated the readme to provide a bit more context around BananaBot's intended purpose
- Switched the `AnnouncementWorker` classes to take an `Announcement` object 

## [3.1.0] - 2022-11-26

#### Added
- Re-worked the backend `Announcement` classes and changed how they were stored to reduce complexity
- Switched to use snake_case to conform with Python standards
- Modified the admin page to work with the new backend changes and made it more user-friendly
- Added a Dockerfile and changelog file

## [3.0.0] - 2022-10-07

#### Added
- This was the first release which came before the changelog file was added
- It involved completely redesigning and rewriting Banana Bot to make it less complex and easily configurable without needing to redeploy
- It added the user interface with an admin page for adding and removing announcements

## [2.0.0] - 2022-07-XX

#### Added
- Old version of the bot not tracked by git

## [1.0.0] - 2022-04-XX
- Old version of the bot not tracked by git
