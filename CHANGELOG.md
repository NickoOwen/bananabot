# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

#### Added
- The ability to store state to enable persistence across container / app reboots

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
