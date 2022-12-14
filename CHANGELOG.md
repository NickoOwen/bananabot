# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

#### Added
- AJAX requests to make the UI experience smoother, more robust, and eliminate the need to refresh the page when a change is made
- The ability to send a message instantly from the admin UI

## [3.2.0]

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